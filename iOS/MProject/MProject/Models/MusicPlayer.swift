import Foundation
import AVFoundation
//import SMBClient

class MusicPlayer: ObservableObject {
    @Published var currentSong: Song?
    @Published var isPlaying: Bool = false
    @Published var playlist: [Song] = []
    
    private var player: AVPlayer?
//    private let smbClient: SMBClient
    
    init() {
//        self.smbClient = SMBClient()
    }
    
    func fetchPlaylist() async throws {
        // TODO: 实现从服务器获取播放列表
        // 示例数据
        playlist = [
            Song(title: "示例歌曲1", artist: "艺术家1", url: "smb://server/music/song1.mp3"),
            Song(title: "示例歌曲2", artist: "艺术家2", url: "smb://server/music/song2.mp3")
        ]
    }
    
    func play(_ song: Song) {
        guard let url = URL(string: song.url) else { return }
        
        // TODO: 通过SMB协议获取音乐文件
        // 临时使用直接URL播放
        let playerItem = AVPlayerItem(url: url)
        player = AVPlayer(playerItem: playerItem)
        player?.play()
        
        currentSong = song
        isPlaying = true
    }
    
    func pause() {
        player?.pause()
        isPlaying = false
    }
    
    func resume() {
        player?.play()
        isPlaying = true
    }
    
    func stop() {
        player?.pause()
        player = nil
        currentSong = nil
        isPlaying = false
    }
}
