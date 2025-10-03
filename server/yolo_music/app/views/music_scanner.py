import os
from pathlib import Path
from mutagen.mp3 import MP3
from mutagen.id3 import ID3

from django.http import JsonResponse
from django.views import View
from django.core.files.base import ContentFile
import re
import difflib

from ..models import Song, Artist, AudioFile
from app.models import UnmatchedMusic

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
            mp3_file = next((f for f in files if f.suffix.lower() == ".mp3"), None)

            if mp3_file:
                metadata = self._parse_mp3(mp3_file)
                title = metadata.get("title") or key
                artist_field = metadata.get("artists")
                duration = metadata.get("duration")
                cover_data = metadata.get("cover")

                # 处理 artists 字段
                if artist_field:
                    if isinstance(artist_field, list):
                        artist_str = " ".join(artist_field)
                    else:
                        artist_str = artist_field

                    # 检查分隔符（&、/）
                    if re.search(r"[、&/]", artist_str):
                        artist_names = re.split(r"[、&/]", artist_str)
                    else:
                        artist_names = [artist_str]

                    artist_names = [a.strip() for a in artist_names if a.strip()]
                else:
                    artist_names = []

                # 如果没有歌手信息，跳过
                if not artist_names:
                    for file_path in files:
                        unprocessed_count += 1
                        UnmatchedMusic.objects.create(
                            file_path=str(file_path.resolve()),
                            file_name=key,
                            elem1=title,
                            elem2=""
                        )
                    continue
                
                # 如果已经存在该歌手的该歌曲 

                # 多人合唱，一条Song，关联所有歌手
                if len(artist_names) > 1:
                    song = Song.objects.create(title=title)                    
                    added += 1                    
                    if duration:
                        song.duration = duration
                    song.save()
                    for artist_name in artist_names:
                        artist, _ = Artist.objects.get_or_create(name=artist_name)
                        song.artists.add(artist)
                    if cover_data and not song.cover:
                        filename = f"{song.id}_cover.jpg"
                        song.cover.save(filename, ContentFile(cover_data), save=False)
                    for f in files:
                        processed_count += 1
                        quality = self._get_quality(f.suffix)
                        AudioFile.objects.get_or_create(
                            song=song,
                            file=str(f.resolve()),
                            defaults={
                                "quality": quality,
                                "size": f.stat().st_size
                            }
                        )
                else:
                    # 单人演唱或同名不同歌手各自演唱
                    for artist_name in artist_names:
                        song = Song.objects.create(title=title)                        
                        added += 1                        
                        if duration:
                            song.duration = duration
                        song.save()
                        artist, _ = Artist.objects.get_or_create(name=artist_name)
                        song.artists.add(artist)
                        if cover_data and not song.cover:
                            filename = f"{song.id}_cover.jpg"
                            song.cover.save(filename, ContentFile(cover_data), save=False)
                        for f in files:
                            processed_count += 1
                            quality = self._get_quality(f.suffix)
                            AudioFile.objects.get_or_create(
                                song=song,
                                file=str(f.resolve()),
                                defaults={
                                    "quality": quality,
                                    "size": f.stat().st_size
                                }
                            )
            else:
                # 没有MP3文件，用-分割文件名
                elem1, elem2 = self._parse_from_filename(key)
                # 检查分割后的字段是否包含分隔符
                def split_artists(text):
                    return [a.strip() for a in re.split(r"[、&/]", text) if a.strip()]
                ele1_artists = split_artists(elem1)
                ele2_artists = split_artists(elem2)
                ele1_str = ",".join(ele1_artists)
                ele2_str = ",".join(ele2_artists)
                for file_path in files:
                    unprocessed_count += 1
                    UnmatchedMusic.objects.create(
                        file_path=str(file_path.resolve()),
                        file_name=key,
                        elem1=ele1_str,
                        elem2=ele2_str
                    )
                continue

        return JsonResponse({
            "status": "ok",
            "added": added,
            "updated": updated,
            "total": added + updated
        })

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
                if "APIC:" in tags:
                    apic = tags["APIC:"]
                    result["cover"] = apic.data
        except Exception as e:
            print("解析 mp3 失败:", e)
        return result

    def _get_quality(self, suffix: str):
        ext = suffix.lower()
        if ext == ".mp3":
            return "SQ"
        elif ext in [".flac", ".wav", ".ape"]:
            return "HQ"
        return "UNKNOWN"

    def _parse_from_filename(self, filename: str):        
        parts = re.split(r"\s*[-—–]\s*", filename, maxsplit=1)
        if len(parts) == 2:
            title, artists_str = parts[0], parts[1]
        else:
            title, artists_str = filename, ""
        return title.strip(), artists_str
    
    def exist(self, title, artist, files) -> bool:
        """
        检查数据库中是否已存在该歌曲
        检查逻辑：
        1. 先按标题过滤
        2. 再比较歌手集合是否相等
        3. 最后检查文件路径是否已存在
        """
        # 先按标题过滤
        songs = Song.objects.filter(title=title)
        for song in songs:
            db_artist_names = list(song.artists.values_list('name', flat=True))
            db_artist_names_set = set(db_artist_names)
            # 比较两个集合是否相等 
            if db_artist_names_set == set(artist):
                # 进一步检查文件路径是否已存在
                existing_files = set(song.audiofile_set.values_list('file', flat=True))
                input_files = set(str(f.resolve()) for f in files)
                if existing_files & input_files:
                    return True
        return False


        