//
//  MusicViewModel.swift
//  LemonMusic
//
//  Created by 冯天宇 on 2024/12/17.
//

import Foundation
import AVFoundation
import Alamofire

class ViewModel: NSObject, ObservableObject {
    
    @Published var data: [SongModel] = []
    
    @Published var selectedSong: SongModel? {
        didSet {
            self.requestSongStream()
        }
    }
    
    var audioPlayer: AVAudioPlayer?
    var player: AVPlayer?
    
    @Published var playing: Bool = false
        
    override init() {
        super.init()
        requestSongList()
    }
        
    /// 暂停播放
    func pause() {
        player?.pause()
        self.playing = false
    }
        
    /// 继续播放
    func resume() {
        player?.play()
        self.playing = true
    }
    
    func play(url: String) {
        guard let url = URL(string: url) else {
            return
        }
        player = AVPlayer(url: url)
        player?.currentItem?.addObserver(self, forKeyPath: "status", options: [.new], context: nil)
        playing = true
    }
    
    override func observeValue(forKeyPath keyPath: String?, of object: Any?, change: [NSKeyValueChangeKey : Any]?, context: UnsafeMutableRawPointer?) {
        if keyPath == "status" {
            let playerItem = object as? AVPlayerItem
            if playerItem?.status == .readyToPlay {
                player?.play()
                playing = true
            } else if playerItem?.status == .failed {
                if let error = playerItem?.error {
                    print("播放出错: \(error)")
                }
            }
        }
    }
    
    func next() {
        guard let currentSong = selectedSong else { return }
        guard let idx = data.firstIndex(of: currentSong) else { return }
        
        if idx == data.count {
            self.selectedSong = data.first
        } else {
            let nextIdx = data.index(after: idx)
            selectedSong = data[nextIdx]
        }
        
    }
    
    func pre() {
        guard let currentSong = selectedSong else { return }
        guard let idx = data.firstIndex(of: currentSong) else { return }
        
        if idx == 0 {
            self.selectedSong = data.last
        } else {
            let preIdx = data.index(before: idx)
            selectedSong = data[preIdx]
        }
    }
    
    // MARK: - Load Data
    
    func requestSongStream() {
        let song = selectedSong ?? data.first
        guard let song = song else {
            return
        }
        requestM3u8File(filepath: song.sqFilePath)
    }
        
    /// 请求歌曲列表
    func requestSongList() {
        if !data.isEmpty {
            return
        }
        self.data = MusciLib.shared.data
    }
    
    /// 请求m3u8文件
    func requestM3u8File(filepath: String) {
        let urlstring = "http://127.0.0.1:5566/stream"
        let params = [
            "filepath": filepath
        ]
        guard let url = URL(string: urlstring) else {
            print("播放失败 \(urlstring)")
            return
        }
        AF.request(url, parameters: params).responseDecodable(of: M3u8Model.self) { response in
            switch response.result {
            case .success(let responseModel):
                self.play(url: responseModel.url)
            case .failure(let error):
                print(error)
            }
        }
  
    }
}

extension ViewModel: AVAudioPlayerDelegate {

    func audioPlayerDidFinishPlaying(_ player: AVAudioPlayer, successfully flag: Bool) {
        selectedSong = data.randomElement()
    }

    
    func audioPlayerDecodeErrorDidOccur(_ player: AVAudioPlayer, error: (any Error)?) {
        
    }
}
