//
//  DataModel.swift
//  LemonMusic
//
//  Created by 冯天宇 on 2024/12/29.
//

import Foundation

struct M3u8Model: Codable {
    var url: String
    
    enum CodingKeys: String, CodingKey {
        case url = "m3u8_url"
    }
}

struct TransferHistoryResponseModel: Codable {
    var code: Int?
    var message: String?
    var data: [String]?
}

struct TransferHistoryModel: Codable {
    var songId: String
    
    enum CodingKeys: String, CodingKey {
        case songId = "song_id"
    }
}
