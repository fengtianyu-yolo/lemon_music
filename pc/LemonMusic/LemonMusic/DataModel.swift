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

enum AudioQuality: String, Codable, Hashable {
    case HQ = "HQ"
    case SQ = "SQ"
}

struct SongFile: Codable, Hashable {
    var filePath: String
    var quality: AudioQuality
    
    enum CodingKeys: String, CodingKey {
        case filePath = "file"
        case quality = "quality"
    }
}

struct SongModel: Equatable, Identifiable, Codable, Hashable {
    
    var id: String {
        return songName + artists.joined(separator: ",")
    }
    
    var songName: String
    var duration: Int
    var artists: [String]
    var articsName: String {
        return artists.count > 1 ? artists.joined(separator: ",") : artists.first ?? ""
    }
    var playCount: Int
    var cover: String?
    var audioFiles: [SongFile]
                
    var formattedDuration: String {
        let minute = duration / 60
        let second = duration % 60
        return String(format: "%02d:%02d", minute, second)
    }
    
    enum CodingKeys: String, CodingKey {
        case songName = "title"
        case artists = "artists"
        case duration = "duration"
        case cover = "cover"
        case audioFiles = "audio_files"
        case playCount = "play_count"
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
