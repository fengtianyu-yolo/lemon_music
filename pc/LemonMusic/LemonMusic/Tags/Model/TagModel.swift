//
//  TagModel.swift
//  LemonMusic
//
//  Created by 冯天宇 on 2025/10/4.
//

import Foundation
import Combine
import SwiftUI

struct QueryTagsResponsedModel: Codable {
    var data: [TagModel]
}

struct TagModel: Codable, Hashable, Identifiable {
    var tagName: String
    var id: Int
    var color: Color = Color.random()            
    enum CodingKeys: String, CodingKey {
        case tagName = "name"
        case id = "id"
    }
}
