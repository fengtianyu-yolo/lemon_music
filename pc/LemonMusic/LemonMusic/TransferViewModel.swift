//
//  TransferViewModel.swift
//  LemonMusic
//
//  Created by fengtianyu on 2025/1/23.
//

import Foundation
import Alamofire

/*
 1. 查找所有的无损音乐
 2. 从服务区查找已经拷贝过的音乐列表
 3. 将无损音乐进行去重，得到未听过的无损音乐列表
 2. 将无损音乐转移至指定目录
 3. 将本次转移的无损音乐上报给服务器
 */


class TransferViewModel {
    
    var data: [SongModel] = []
    var destinationPath: String = ""
    
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
