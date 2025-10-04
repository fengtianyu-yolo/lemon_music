//
//  TagViewModel.swift
//  LemonMusic
//
//  Created by 冯天宇 on 2025/10/3.
//

import Foundation
import Alamofire

class TagViewModel: ObservableObject {
    @Published var tagList: [TagModel] = []
    
    init() {
        requestTagList()
    }
    
    /// 请求歌曲列表
    func requestTagList() {
        if !tagList.isEmpty {
            return
        }
        self.tagList = DataCenter.shared.tagList
    }

    func create(tagName: String) {
        var params = Parameters()
        params["tag"] = tagName
        AF.request("http://127.0.0.1:5566/tag/create", method: .post, parameters: params).responseDecodable(of: CreateTagResponseModel.self) { respose in
            print(respose)
            
            switch respose.result {
            case .success(let dataModel):
                if dataModel.success{
                    ToastManager.shared.show(dataModel.message)
                    
                    if let name = dataModel.tag["name"], let idString = dataModel.tag["id"], let id = Int(idString)  {
                        let tagModel = TagModel(tagName: name, id: id)
                        self.tagList.append(tagModel)
                        ToastManager.shared.show("创建成功 🧨")
                    } else {
                        ToastManager.shared.show(dataModel.message)
                    }
                } else {
                    ToastManager.shared.show(dataModel.message)
                }
            case .failure(let error):
                print(error)
                ToastManager.shared.show(error.localizedDescription)
            }
        }
    }
}

struct CreateTagResponseModel: Codable {
    var success: Bool
    var message: String
    var tag: [String: String]
}
