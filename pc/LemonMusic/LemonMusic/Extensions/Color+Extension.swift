//
//  Color+Extension.swift
//  LemonMusic
//
//  Created by 冯天宇 on 2025/10/4.
//

import Foundation
import SwiftUI

extension Color {
    static func random() -> Color {
        return Color(
            red: .random(in: 0...1),
            green: .random(in: 0...1),
            blue: .random(in: 0...1)
        )
    }
}
