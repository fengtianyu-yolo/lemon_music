//
//  DataCenter.swift
//  LemonMusic
//
//  Created by 冯天宇 on 2025/10/4.
//

import Foundation
import Combine
import Alamofire

class DataCenter: ObservableObject {
    static let shared = DataCenter()
    
    @Published var tagList: [TagModel] = []
    @Published var songList: [SongModel] = []

    init() {
        requestSongList()
        requestTags()
    }
    
    private func requestTags() {
        AF.request("http://127.0.0.1:5566/tags").responseDecodable(of: QueryTagsResponsedModel.self) { response in
            switch response.result {
            case .success(let responseModel):
                self.tagList = responseModel.data
            case .failure(let error):
                print(error)
            }
        }
    }
    
    
    func requestSongList() {
        if !songList.isEmpty {
            return
        }
        
        AF.request("http://127.0.0.1:5566/songs").responseDecodable(of: SongListResponseModel.self) { response in
            switch response.result {
            case .success(let responseModel):
                self.songList = responseModel.data
            case .failure(let error):
                print(error)
            }
        }
    }
}
