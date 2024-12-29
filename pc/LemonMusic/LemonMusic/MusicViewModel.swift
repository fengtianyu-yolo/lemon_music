//
//  MusicViewModel.swift
//  LemonMusic
//
//  Created by 冯天宇 on 2024/12/17.
//

import Foundation
import AVFoundation
import Alamofire

class ViewModel: ObservableObject {
    
    @Published var data: [SongModel] = []
    
    @Published var selectedSong: SongModel? {
        didSet {
            self.play()
        }
    }
    
    var audioPlayer: AVAudioPlayer?
    
    @Published var playing: Bool = false
        
    init() {
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
}
