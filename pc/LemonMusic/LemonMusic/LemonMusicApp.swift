//
//  LemonMusicApp.swift
//  LemonMusic
//
//  Created by 冯天宇 on 2023/10/18.
//

import SwiftUI

@main
struct LemonMusicApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
                .frame(width: 1200, height: 800)
        }
        .windowStyle(.hiddenTitleBar)
        .windowResizability(.contentSize)
    }
}

/*
 优化侧边栏效果
 3 添加进度条
 列表添加标题行
 */
