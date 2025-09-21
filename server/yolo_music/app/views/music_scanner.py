import os
from pathlib import Path
from mutagen import File as MutagenFile
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, TIT2, TPE1

from django.conf import settings
from django.http import JsonResponse
from django.views import View
from django.core.files.base import ContentFile
import re
import difflib

from ..models import Song, Artist, AudioFile
from app.models import UnmatchedMusic

LOG_FILE = "unmatched_songs.log"

class MusicScannerView(View):
    """扫描 /musics 文件夹并入库"""

    SUPPORTED_EXTS = [".mp3", ".flac", ".wav", ".ape"]

    def get(self, request):
        music_path = Path('/Volumes/Library/音乐库')
        if not music_path.exists():
            return JsonResponse({"error": "路径不存在"}, status=400)

        # 文件分组：{ "歌手 - 歌曲名": [文件路径们] }
        song_groups = {}
        count = 0
        processed_count = 0
        unprocessed_count = 0
        for file in music_path.glob("**/*"):
            
            if file.suffix.lower() in self.SUPPORTED_EXTS:
                count += 1
                key = file.stem  # 去掉后缀，作为归类依据
                song_groups.setdefault(key, []).append(file)
        

        added, updated = 0, 0

        for key, files in song_groups.items():
            # 优先找mp3文件
            mp3_file = next((f for f in files if f.suffix.lower() == ".mp3"), None)

            if mp3_file:
                metadata = self._parse_mp3(mp3_file)
                title = metadata.get("title") or key
                artist_names = metadata.get("artists") or []
                duration = metadata.get("duration")
                cover_data = metadata.get("cover")
            else:
                # 用文件名解析
                elem1, elem2 = self._parse_from_filename(key)
                title, valid_artists = self._process_parsed_elements(elem1, elem2, key)
                # title, artist_names = self._parse_from_filename(key)
                duration, cover_data = None, None
                if not valid_artists:
                    for file_path in files:
                        unprocessed_count += 1
                        UnmatchedMusic.objects.create(
                            file_path=str(file_path.resolve()),
                            file_name=key,
                            elem1=elem1,
                            elem2=elem2
                        )        
                    continue  # 跳过这首歌

            # 歌曲入库
            print(f"Processing song: {title}, Artists: {artist_names}")
            song, created = Song.objects.get_or_create(title=title)
            if created:
                added += 1
            else:
                updated += 1

            if duration:
                song.duration = duration
            song.save()

            # 处理歌手
            if artist_names:
                for artist_name in artist_names:
                    artist, _ = Artist.objects.get_or_create(name=artist_name.strip())
                    song.artists.add(artist)

            # 保存封面
            if cover_data and not song.cover:
                filename = f"covers/{song.id}_cover.jpg"
                song.cover.save(filename, ContentFile(cover_data), save=False)

            # 处理音质文件
            for f in files:
                processed_count += 1
                quality = self._get_quality(f.suffix)
                AudioFile.objects.get_or_create(
                    song=song,
                    file=str(f.resolve()),  # 使用绝对路径作为唯一标识
                    defaults={
                        "quality": quality,
                        "size": f.stat().st_size
                    }
                )             
        
        print(count)
        print(processed_count)
        print(unprocessed_count)
        return JsonResponse({
            "status": "ok",
            "added": added,
            "updated": updated,
            "total": added + updated
        })

    def _process_parsed_elements(self, elem1, elem2, key):
        """
        尝试判断两个元素中哪个是歌手，哪个是歌曲标题
        elem1, elem2: 从文件名解析得到的两个部分
        key: 文件名，用于日志
        """
        def split_artists(text):
            return [a.strip() for a in re.split(r"[、,&/]", text) if a.strip()]

        def check_artists(artist_text):
            """检查歌手字段，返回 (是否是歌手字段, 歌手对象列表)"""
            candidate_names = split_artists(artist_text)
            artist_objs = []
            existing_artists = []  # 存储已存在的歌手
            new_artists = []  # 存储待创建的歌手

            # 如果没有拆分出多个元素（即没有分隔符）
            if len(candidate_names) == 1:
                name = candidate_names[0]
                artist_obj = self._find_similar_artist(name)
                if artist_obj:
                    return True, [artist_obj]  # 找到匹配
                else:
                    return False, []           # 没有匹配，跳过

            for name in candidate_names:
                artist_obj = self._find_similar_artist(name)
                if artist_obj:
                    existing_artists.append(artist_obj)  # 存在的歌手
                else:
                    new_artists.append(name)  # 不存在的歌手

            # 如果有至少一个已存在的歌手，开始创建新的歌手
            if existing_artists:
                # 只有在已有歌手时才创建新歌手
                for name in new_artists:
                    new_artist, _ = Artist.objects.get_or_create(name=name)
                    artist_objs.append(new_artist)

                # 将所有存在的歌手添加到返回列表中
                artist_objs.extend(existing_artists)
                return True, artist_objs  # 确认是歌手字段

            return False, []  # 没有已存在歌手，跳过

        # --- 先尝试 elem1 ---
        is_artist, artist_objs = check_artists(elem1)
        if is_artist:  # elem1 确认是歌手
            title = elem2.strip()
            return title, artist_objs

        # --- 再尝试 elem2 ---
        is_artist, artist_objs = check_artists(elem2)
        if is_artist:  # elem2 确认是歌手
            title = elem1.strip()
            return title, artist_objs

        # --- 两个都不满足 ---
        msg = f"[跳过] 无法确定歌手字段，文件名={key}\n"
        print(msg.strip())
        return None, []

    def _parse_mp3(self, file_path: Path):
        """解析 MP3 文件的 meta 数据"""
        result = {}
        try:
            audio = MP3(file_path, ID3=ID3)
            result["duration"] = int(audio.info.length)
            tags = audio.tags

            if tags:
                if "TIT2" in tags:
                    result["title"] = tags["TIT2"].text[0]
                if "TPE1" in tags:
                    result["artists"] = tags["TPE1"].text
                if "APIC:" in tags:  # 封面图
                    apic = tags["APIC:"]
                    result["cover"] = apic.data  # 这是二进制数据
        except Exception as e:
            print("解析 mp3 失败:", e)
        return result

    def _get_quality(self, suffix: str):
        """根据后缀返回音质"""
        ext = suffix.lower()
        if ext == ".mp3":
            return "SQ"
        elif ext == ".flac":
            return "HQ"
        elif ext == ".wav":
            return "HQ"
        elif ext == ".ape":
            return "HQ"
        return "UNKNOWN"
   
    def _parse_from_filename(self, filename: str):
        """从文件名解析 歌曲名 和 歌手列表"""
        # 常见分隔符：- — – （可能有空格）
        parts = re.split(r"\s*[-—–]\s*", filename, maxsplit=1)
        if len(parts) == 2:
            title, artists_str = parts[0], parts[1]
        else:
            title, artists_str = filename, ""

        # 多个歌手分隔符：、 , & 和中文顿号
        # artist_names = re.split(r"[、,&，]", artists_str)
        # artist_names = [a.strip() for a in artist_names if a.strip()]

        return title.strip(), artists_str

    def _find_similar_artist(self, name: str, threshold: float = 0.7):
        """模糊匹配数据库里的歌手，如果相似度高则返回 Artist，否则 None"""
        all_artists = Artist.objects.values_list("name", flat=True)
        match = difflib.get_close_matches(name, all_artists, n=1, cutoff=threshold)
        if match:
            return Artist.objects.get(name=match[0])
        return None