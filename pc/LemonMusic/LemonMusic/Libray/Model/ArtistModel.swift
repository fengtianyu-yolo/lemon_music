//
//  ArtistModel.swift
//  LemonMusic
//
//  Created by 冯天宇 on 2025/10/4.
//

import Foundation

struct ArtistModel: Equatable, Codable, Hashable {
    var artistName: String
    var artistId: Int
    
    enum CodingKeys: String, CodingKey {
        case artistName = "artist_name"
        case artistId = "artist_id"
    }
}
