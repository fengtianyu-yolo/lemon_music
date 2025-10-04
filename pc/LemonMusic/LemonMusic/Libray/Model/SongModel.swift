//
//  SongModel.swift
//  LemonMusic
//
//  Created by 冯天宇 on 2025/10/4.
//

import Foundation

struct SongListResponseModel: Codable {
    var data: [SongModel]
}

struct SongModel: Equatable, Identifiable, Codable, Hashable {
    
    var id: String {
        return "\(songId)"
    }
    
    var songId: Int
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
        case songId = "id"
        case songName = "title"
        case artists = "artists"
        case duration = "duration"
        case cover = "cover"
        case audioFiles = "audio_files"
        case playCount = "play_count"
    }
}

