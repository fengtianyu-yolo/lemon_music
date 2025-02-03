//
//  DataModel.swift
//  LemonMusic
//
//  Created by 冯天宇 on 2024/12/29.
//

import Foundation

struct SongListResponseModel: Codable {
    var data: [SongModel]
}

struct SongModel: Equatable, Identifiable, Codable, Hashable {
    
    var id: Int {
        return songId
    }
    
    var songId: Int
    var songName: String
    var duration: Int
    var mediaType: Int
    var sqFileName: String
    var sqFilePath: String
    var hqFileName: String
    var hqFilePath: String
    var coverPath: String
    var addedTime: String?
    var updatedTime: String?
    var artists: [ArtistModel]
    
    var formattedDuration: String {
        let minute = duration / 60
        let second = duration % 60
        return String(format: "%02d:%02d", minute, second)
    }
    
    var artistName: String {
        if artists.isEmpty {
            return ""
        } else {
            return artists.map { $0.artistName }.joined(separator: "&")
        }
    }
    
    enum CodingKeys: String, CodingKey {
        case songId = "song_id"
        case songName = "song_name"
        case duration = "duration"
        case mediaType = "media_type"
        case sqFileName = "sq_file_name"
        case hqFileName = "hq_file_name"
        case sqFilePath = "sq_file_path"
        case hqFilePath = "hq_file_path"
        case coverPath = "cover_path"
        case addedTime = "added_time"
        case updatedTime = "updated_time"
        case artists = "artists"
    }
}

struct ArtistModel: Equatable, Codable, Hashable {
    var artistName: String
    var artistId: Int
    
    enum CodingKeys: String, CodingKey {
        case artistName = "artist_name"
        case artistId = "artist_id"
    }
}

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
