//
//  UnRecognizedViewModel.swift
//  LemonMusic
//
//  Created by 冯天宇 on 2025/10/3.
//

import Foundation
import Combine
import SwiftUI
import Alamofire

class UnRecognizedViewModel: ObservableObject {
    
    @Published var data: [UnRecognizedDataModel] = []
    @Published var selectedFile: UnRecognizedDataModel?
    
    init() {
        self.request()
    }
    
    func request() {
        AF.request("http://127.0.0.1:5566/unknows").responseDecodable(of: UnRecognizedResponsedModel.self) { response in
            switch response.result {
            case .success(let responseModel):
                self.data = responseModel.data
            case .failure(let error):
                print(error)
            }
        }
    }
    
    func update(songName: String, artistName: String, filePath: String?) {
        guard let filePath = filePath else {
            ToastManager.shared.show("缺少filePath参数")
            return
        }
        var params = Parameters()
        params["title"] = songName
        params["artists"] = artistName
        params["filepath"] = filePath
        AF.request("http://127.0.0.1:5566/update", method: .post, parameters: params).responseDecodable(of: UpdateSongResponsedModel.self) { respose in
            print(respose)
            
            switch respose.result {
            case .success(let dataModel):
                if dataModel.success ?? false {
                    ToastManager.shared.show(dataModel.message ?? "操作成功")
                } else {
                    ToastManager.shared.show(dataModel.error ?? "未知错误")
                }
            case .failure(let error):
                print(error)
                ToastManager.shared.show(error.localizedDescription)
            }
        }
    }
}

struct UnRecognizedResponsedModel: Codable {
    var data: [UnRecognizedDataModel]
}

struct UnRecognizedDataModel: Codable, Hashable {
    var fileName: String
    var text1: String
    var text2: String
    var filePath: String
    
    enum CodingKeys: String, CodingKey {
        case fileName = "filename"
        case text1 = "text1"
        case text2 = "text2"
        case filePath = "file_path"
    }
}

struct UpdateSongResponsedModel: Codable {
    var success: Bool?
    var error: String?
    var message: String?
}
