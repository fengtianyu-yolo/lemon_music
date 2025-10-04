//
//  ResponseModel.swift
//  LemonMusic
//
//  Created by 冯天宇 on 2025/10/4.
//

import Foundation

struct ResponseModel: Codable {
    var success: Bool
    var message: String?
    var error: String?
}
