//
//  TransferViewModel.swift
//  LemonMusic
//
//  Created by fengtianyu on 2025/1/23.
//

import Foundation
import Alamofire
import AppKit
import Combine

/*
 1. 查找所有的无损音乐
 2. 从服务区查找已经拷贝过的音乐列表
 3. 将无损音乐进行去重，得到未听过的无损音乐列表
 2. 将无损音乐转移至指定目录
 3. 将本次转移的无损音乐上报给服务器
 */


class TransferViewModel: ObservableObject {
    
    private var deviceId = "" {
        didSet {
            fetchHistory()
        }
    }
    @Published var deviceName = ""
    private var devicePath = ""
    private var deviceAvailableCapacity = 0
    private var transferHistory: [String] = [] {
        didSet {
            sortData()
        }
    }
    private var cancellables = Set<AnyCancellable>()

    var data = [TransferInfoModel]()
    
    @Published var transfering: Bool = false
    
    init() {
        // 获取设备
        setupVolumeMonitor()
        tryFetchDeviceId()
        // 初始化数据
        dataInit()
    }
    
    func dataInit() {
        data = MusciLib.shared.data.map({ TransferInfoModel(song: $0, hasTransfered: false, selected: false) })
        MusciLib.shared.$data.sink { songs in
            self.data = songs.map({ TransferInfoModel(song: $0, hasTransfered: false, selected: false) })
        }
        .store(in: &cancellables)
    }
        
    /// 数据排序: 已经转移过的音乐放在前面,播放次数高的音乐放在前面
    func sortData() {
        data.forEach { model in
            if transferHistory.contains("\(model.song.songId)") {
                model.hasTransfered = true
            }
        }
        data.sort { !$0.hasTransfered && $1.hasTransfered }
//        data.sort { $0.song.playCount > $1.song.playCount }
    }

    func getFileSize(filePath: String) -> Int64 {
        let fileManager = FileManager.default
        do {
            let attr = try fileManager.attributesOfItem(atPath: filePath)
            return attr[FileAttributeKey.size] as! Int64
        } catch {
            print("Error: \(error)")
        }
        return 0
    }
    
    // 将无损音乐转移至指定目录
    func transfer() {
        DispatchQueue.main.async { [weak self] in
            self?.transfering = true
        }
        /*
        var songIds: [String] = []
        var totalSize: Int64 = 0
        deviceAvailableCapacity = 1 * 1024 * 1024 * 1024
        for song in data {
            guard totalSize < deviceAvailableCapacity else {
                print("U盘空间不足")
                break
            }
            guard !song.song.sqFilePath.isEmpty else {
                continue
            }
            do {
                try FileManager.default.copyItem(atPath: song.song.sqFilePath, toPath: self.devicePath + "/" + song.song.sqFileName)
                songIds.append("\(song.song.songId)")
                DispatchQueue.main.async {
                    song.hasTransfered = true
                }
                totalSize += getFileSize(filePath: song.song.sqFilePath)
                print("[Transfer]: 同步 - \(song.song.songName), 使用空间 - \(Double(totalSize) / 1024.0 / 1024.0)MB")
            } catch {
                print("Error: \(error)")
            }
        }
        DispatchQueue.main.async { [weak self] in
            self?.transfering = false
        }
        reportTransferList(songIds: songIds)
         */
    }
    
}

// MARK: - Network

extension TransferViewModel {
    
    /// 获取设备的同步记录
    func fetchHistory() {
        
        guard !deviceId.isEmpty else {
            print("Device id is empty.")
            return
        }
        let params = [
            "device_id": deviceId
        ]
        AF.request("http://127.0.0.1:5566/device", parameters: params).responseDecodable(of: TransferHistoryResponseModel.self) { response in
            switch response.result {
            case .success(let responseModel):
                self.transferHistory = responseModel.data ?? []
                print("Transfer history fetched successfully. \(self.transferHistory)")
            case .failure(let error):
                print(error)
            }
        }
    }

    // 将转移的无损音乐列表上报至服务器
    func reportTransferList(songIds: [String]) {
        let parameters: [String: Any] = ["song_ids": songIds, "device_id": deviceId]
        AF.request("http://127.0.0.1:5566/device", method: .post, parameters: parameters, encoding: JSONEncoding.default).responseDecodable(of: TransferHistoryResponseModel.self) { response in
            switch response.result {
            case .success(let responseModel):
                print("Transfer history fetched successfully. \(responseModel)")
            case .failure(let error):
                print(error)
            }
        }
    }
}

// MARK: - U盘相关

extension TransferViewModel {
    
    /// 获取U盘的UUID
    func tryFetchDeviceId() {
        // 获取所有挂载的卷
        
        let mountedVolumes = FileManager.default.mountedVolumeURLs(includingResourceValuesForKeys: [.volumeUUIDStringKey], options: [])
        
        if let volumes = mountedVolumes {
            for volume in volumes {
                if let values = try? volume.resourceValues(forKeys: [.volumeUUIDStringKey, .volumeLocalizedNameKey, .volumeIsRemovableKey, .volumeIsInternalKey, .pathKey, .volumeAvailableCapacityKey]) {
                    if let removable = values.volumeIsRemovable, removable, let internalDevice = values.volumeIsInternal, !internalDevice, let path = values.path {
                        print("U盘 UUID = " + (values.volumeUUIDString ?? "is nil"))
                        print("U盘 name = " + (values.volumeLocalizedName ?? "is nil"))
                        print("U盘 isRemovable = " + (values.volumeIsRemovable?.description ?? "is nil"))
                        print("U盘 isInternal = " + (values.volumeIsInternal?.description ?? "is nil"))
                        print("U盘 path = " + (values.path ?? "is nil"))
                        print("U盘 availableCapacity = " + (values.volumeAvailableCapacity?.description ?? "is nil"))
                        deviceId = values.volumeUUIDString ?? ""
                        deviceName = values.volumeLocalizedName ?? ""
                        devicePath = path
                        deviceAvailableCapacity = values.volumeAvailableCapacity ?? 0
                    }
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
    
}

class TransferInfoModel: ObservableObject, Hashable, Equatable {
            
    var song: SongModel
    @Published var hasTransfered: Bool = false
    @Published var selected: Bool = false
    
    init(song: SongModel, hasTransfered: Bool, selected: Bool) {
        self.song = song
        self.hasTransfered = hasTransfered
        self.selected = selected
    }
    
    static func == (lhs: TransferInfoModel, rhs: TransferInfoModel) -> Bool {
        return lhs.song.songId == rhs.song.songId
    }
    
    func hash(into hasher: inout Hasher) {
        hasher.combine(song.songId)
    }
    
}
