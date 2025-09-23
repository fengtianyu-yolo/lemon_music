//
//  TagListView.swift
//  LemonMusic
//
//  Created by fengtianyu on 2025/9/23.
//

import Foundation
import SwiftUI

struct TagListView: View {
    var body: some View {
        VStack(alignment: .leading, spacing: 0) {
            TagListHeaderView()
            Divider()
            TagListContentView()
        }
    }
}

struct TagListHeaderView: View {
    var body: some View {
        Text("Tag")
            .font(Font.system(size: 44, weight: Font.Weight.bold))
            .padding(.horizontal, 20)
            .padding(.vertical, 16.0)
    }
}

struct TagListContentView: View {
    var body: some View {
        HStack(spacing: 0) {
            // Left side: artist/tags list
            List {
                ForEach(["陈慧娴", "凤凰传奇", "江珊", "刘可", "任夏"], id: \.self) { name in
                    Text(name)
                        .frame(height: 36)
                        .padding(.vertical, 4)
                        .listRowInsets(EdgeInsets())
                }
            }
            .frame(maxWidth: 200)
//            .background(Color.gray.opacity(0.1))
            .background(Color.orange)
            .listStyle(.plain) // 让分隔线从左到右

            Divider()

            // Right side: songs list
            List {
                Text("凤凰传奇")
                    .font(.title2)
                    .padding(.bottom, 8)
                ForEach([
                    ("山河图", "3:47"),
                    ("我从草原来", "3:40"),
                    ("最炫民族风", "4:20")
                ], id: \.0) { song, duration in
                    HStack {
                        Rectangle()
                            .fill(Color.gray)
                            .frame(width: 50, height: 50)
                            .cornerRadius(4)
                        VStack(alignment: .leading) {
                            Text(song)
                                .font(.body)
                            Text(duration)
                                .font(.caption)
                                .foregroundColor(.secondary)
                        }
                        Spacer()
                    }
                }
            }
            .padding(.horizontal)
        }
    }
}
