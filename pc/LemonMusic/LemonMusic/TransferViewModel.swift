//
//  TransferViewModel.swift
//  LemonMusic
//
//  Created by fengtianyu on 2025/1/23.
//

import Foundation
import Alamofire
import AppKit

/*
 1. 查找所有的无损音乐
 2. 从服务区查找已经拷贝过的音乐列表
 3. 将无损音乐进行去重，得到未听过的无损音乐列表
 2. 将无损音乐转移至指定目录
 3. 将本次转移的无损音乐上报给服务器
 */


class TransferViewModel {
    
    private var data: [SongModel] = []
    private var destinationPath: String = ""
    private var deviceId = ""
    private var transferHistory: [TransferHistoryModel] = []
    
    init() {
//        super.init()
        setupVolumeMonitor()
        tryFetchDeviceId()
        fetchAllSong()
        fetchHistory()
    }
    
    /// 获取U盘的UUID
    func tryFetchDeviceId() {
        // 获取所有挂载的卷
        
        let mountedVolumes = FileManager.default.mountedVolumeURLs(includingResourceValuesForKeys: [.volumeUUIDStringKey], options: [])
        
        if let volumes = mountedVolumes {
            for volume in volumes {
                if let uuid = try? volume.resourceValues(forKeys: [.volumeUUIDStringKey]).volumeUUIDString {
                    deviceId = uuid
                    break
                }
            }
        }
    }

    private func setupVolumeMonitor() {
        NotificationCenter.default.addObserver(self, selector: #selector(receiveNotification(notification: )), name: NSWorkspace.didMountNotification, object: nil)
    }
        
    @objc func receiveNotification(notification: NSNotification) {
        tryFetchDeviceId()
    }
    
    func fetchAllSong() {
        AF.request("http://127.0.0.1:5566/songs").responseDecodable(of: SongListResponseModel.self) { response in
            switch response.result {
            case .success(let responseModel):
                self.data = responseModel.data
            case .failure(let error):
                print(error)
            }
        }
    }
    
    func fetchHistory() {
        
        let params = [
            "device_id": deviceId
        ]
        
        AF.request("http://127.0.0.1:5566/history", parameters: params).responseDecodable(of: TransferHistoryResponseModel.self) { response in
            switch response.result {
            case .success(let responseModel):
                self.transferHistory = responseModel.data
            case .failure(let error):
                print(error)
            }
        }
    }
    
    // 查找所有的无损音乐
    func getLosslessSongs() -> [SongModel] {
        var losslessSongs: [SongModel] = []
        for song in data {
            if song.mediaType == 2 {
                losslessSongs.append(song)
            }
        }
        return losslessSongs
    }
    
    // 将无损音乐转移至指定目录
    func transferLosslessSongs() {
        let losslessSongs = getLosslessSongs()
        for song in losslessSongs {
            let sourcePath = song.sqFilePath
            let destinationPath = self.destinationPath + "/" + song.sqFileName
            do {
                try FileManager.default.copyItem(atPath: sourcePath, toPath: destinationPath)
            } catch {
                print("Error: \(error)")
            }
        }
    }
    
    // 将转移的无损音乐列表写入文件
    func writeTransferList() {
        let losslessSongs = getLosslessSongs()
        var transferList: String = ""
        for song in losslessSongs {
            transferList += song.songName + "\n"
        }
        let filePath = self.destinationPath + "/transfer_list.txt"
        do {
            try transferList.write(toFile: filePath, atomically: true, encoding: .utf8)
        } catch {
            print("Error: \(error)")
        }
    }
    
    // 将转移的无损音乐列表上报至服务器
    func reportTransferList() {
        let losslessSongs = getLosslessSongs()
        var transferList: [String] = []
        for song in losslessSongs {
            transferList.append(song.songName)
        }
        let parameters: [String: Any] = ["transferList": transferList]
        AF.request("http://localhost:8080/transfer", method: .post, parameters: parameters, encoding: JSONEncoding.default).responseJSON { response in
            switch response.result {
            case .success:
                print("Transfer list reported successfully.")
            case .failure(let error):
                print("Error: \(error)")
            }
        }
    }
}

class UsedModels: Codable {
    
}
