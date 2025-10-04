//
//  AudioFileModel.swift
//  LemonMusic
//
//  Created by 冯天宇 on 2025/10/4.
//

import Foundation

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

