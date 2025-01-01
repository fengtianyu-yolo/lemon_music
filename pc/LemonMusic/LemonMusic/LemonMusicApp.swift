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
 1 加个icon
 2 顶部加个卡片
 3 添加进度条
 4 优化修改列表样式
 */
