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
//            self.play()
            self.getSongStream()
        }
    }
    
    var audioPlayer: AVAudioPlayer?
    var player: AVPlayer?
    
    @Published var playing: Bool = false
        
    override init() {
        super.init()
        get()
    }
    
    func pause() {
        guard let player = self.audioPlayer else {
            return
        }
        player.pause()
        self.playing = player.isPlaying
    }
    
    func resume() {
        guard let player = self.audioPlayer else {
            return
        }
        player.play()
        self.playing = player.isPlaying
    }
    
    func play() {
        
        let song = selectedSong ?? data.first
        
        guard let song = song else {
            return
        }
        
        if !song.sqFilePath.isEmpty {
            print("path = \(song.sqFilePath)")
            let fileURL = URL(fileURLWithPath: song.sqFilePath)
            do {
                audioPlayer = try AVAudioPlayer(contentsOf: fileURL)
                audioPlayer?.delegate = self
                audioPlayer?.prepareToPlay()
                audioPlayer?.play()
                playing = true
            } catch {
                print("播放不了 \(error.localizedDescription)")
            }
        } else {
            print("没有无损音乐")
        }
    }
    
    func getSongStream() {
        let song = selectedSong ?? data.first
        guard let song = song else {
            return
        }
        self.getM3u8(filepath: song.sqFilePath)
    }
    
    func play(url: String) {
        guard let url = URL(string: url) else {
            return
        }
        do {
            player = AVPlayer(url: url)
            player?.play()
//            audioPlayer = try AVAudioPlayer(contentsOf: fileURL)
//            audioPlayer?.delegate = self
//            audioPlayer?.prepareToPlay()
//            audioPlayer?.play()
            playing = true
        } catch {
            print("播放不了 \(error.localizedDescription)")
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
    
    // MARK: - Data
    func get() {
        AF.request("http://127.0.0.1:5566/songs").responseDecodable(of: SongListResponseModel.self) { response in
            switch response.result {
            case .success(let responseModel):
                self.data = responseModel.data
            case .failure(let error):
                print(error)
            }
        }
    }
    
    func getM3u8(filepath: String) {
        
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
        /*
        AF.request(url, parameters: params, headers: ["Accept": "application/vnd.apple.mpegurl"]).responseData { response in
            switch response.result {
            case.success(let data):
                // 在这里处理成功获取到的数据
                if let mpegurlString = String(data: data, encoding:.utf8) {
                    
                }
            case.failure(let error):
                // 处理请求失败的情况
                print("请求出错: \(error)")
            }
        }
         */
    
    }
}

extension ViewModel: AVAudioPlayerDelegate {

    func audioPlayerDidFinishPlaying(_ player: AVAudioPlayer, successfully flag: Bool) {
        selectedSong = data.randomElement()
    }

    
    func audioPlayerDecodeErrorDidOccur(_ player: AVAudioPlayer, error: (any Error)?) {
        
    }
}
