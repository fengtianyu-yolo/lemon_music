//
//  MusciLib.swift
//  LemonMusic
//
//  Created by 冯天宇 on 2025/2/1.
//

import Foundation
import Alamofire

class MusciLib: ObservableObject {
    @Published var data: [SongModel] = []
    
    static let shared = MusciLib()
    
    init() {
        requestSongList()
    }
    
    func requestSongList() {
        if !data.isEmpty {
            return
        }
        
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
