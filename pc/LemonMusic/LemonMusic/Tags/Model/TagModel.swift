//
//  TagModel.swift
//  LemonMusic
//
//  Created by 冯天宇 on 2025/10/4.
//

import Foundation
import Combine

struct QueryTagsResponsedModel: Codable {
    var data: [TagModel]
}

struct TagModel: Codable, Hashable {
    var tagName: String
    var id: Int
    
    
    enum CodingKeys: String, CodingKey {
        case tagName = "name"
        case id = "id"
    }
}
