//
//  SongListView.swift
//  LemonMusic
//
//  Created by 冯天宇 on 2025/6/29.
//

import SwiftUI

struct UnRecognizedListView: View {
    
    @StateObject private var viewModel = UnRecognizedViewModel()
    
    var body: some View {
        VStack(alignment: .leading, spacing: 0) {
            
            Text("UnRecognized List")
                .font(Font.custom("Chalkboard SE", size: 44.0))
                .padding(.horizontal, 20)
                .padding(.vertical, 16.0)
                        
            UnRecognizedListViewDetail(viewModel: viewModel)
            UpdateSongInfoView(text1: viewModel.selectedFile?.text1 ?? "", text2: viewModel.selectedFile?.text2 ?? "", filepath: viewModel.selectedFile?.filePath ?? "") { songName, artistName in
                print("set songname \(songName) artist = \(artistName)")
                viewModel.update(songName: songName, artistName: artistName, filePath: viewModel.selectedFile?.filePath)
            }
        }
        .padding(.bottom, 0)
    }
}

struct UnRecognizedListViewDetail: View {
            
    @StateObject var viewModel: UnRecognizedViewModel

    // 定义列宽，这是最关键的部分，需要手动调整
    let colWidth1: CGFloat = 300 // 标题
    let colWidth2: CGFloat = 80  // 时长
    let colWidth3: CGFloat = 200 // 歌手
    let colWidth4: CGFloat = 150 // 专辑
    
    var body: some View {
        
        VStack(spacing: 0) { // 使用 VStack 容纳列头和列表，并移除默认间距
            // MARK: - 列头
            HStack {
                Text("文件名")
                    .font(.subheadline)
                Spacer() // 推开剩余空间
            }
            .padding(.horizontal, 16) // 列头与行内容保持一致的水平内边距
            .padding(.vertical, 5)
            .background(Color.secondary.opacity(0.1)) // 列头背景色
            
            // MARK: - 歌曲列表
            List {
                ForEach(Array(viewModel.data.enumerated()), id: \.element) { index, file in
                    UnRecognizedListRow(fileModel: file, isSelected: viewModel.selectedFile == file, colWidth1: colWidth1, rowIndex: index, onSingleTap: { file in
                        viewModel.selectedFile = file
                    })
                    .listRowSeparator(.hidden) // 隐藏 List 默认分隔线
                    .listRowInsets(EdgeInsets(top: 0, leading: 0, bottom: 0, trailing: 0)) // 移除默认行内边距
                }
            }
            .listStyle(.plain) // 使用 PlainListStyle 移除默认列表样式
        }
    }
}

// 自定义行视图
struct UnRecognizedListRow: View {
    let fileModel: UnRecognizedDataModel
    let isSelected: Bool
    let colWidth1: CGFloat
    let rowIndex: Int
    let onSingleTap: (UnRecognizedDataModel) -> Void // 新增：单击闭包
        
    var body: some View {
        HStack {
            Text(fileModel.fileName)
            Spacer() // 推开剩余空间
        }
        .padding(.horizontal, 8)
        .padding(.vertical, 4) // 垂直内边距
        .background(
            Group {
                if isSelected {
                    Color.accentColor.opacity(0.2)
                } else if rowIndex % 2 == 0 { // 偶数行
                    Color.clear // 或者一个非常浅的颜色
                } else { // 奇数行
                    Color.secondary.opacity(0.1) // 稍微深一点的颜色
                }
            }
        )
        .contentShape(Rectangle()) // 使整行区域可点击
        .onTapGesture {
            onSingleTap(fileModel)
        }
    }
}

struct UpdateSongInfoView: View {
    
    var text1: String
    var text2: String
    let filepath: String
    @State var songName: String?
    @State var artistNames: String?
    var updateSongInfo: (String, String) -> Void
    
    var body: some View {
        HStack(alignment: .center, spacing: 22.0) {
            
            VStack(alignment: .leading, spacing: 12.0) {
                Text("🎵设置歌曲名")
                HStack {
                    Button {
                        songName = text1
                        artistNames = text2
                    } label: {
                        Text(text1)
                            .font(.subheadline)
                            .padding(.horizontal, 12)
                            .padding(.vertical, 4)
                            .background( songName == text1 ? Color.green : Color.green.opacity(0.3))
                            .foregroundColor(.white)
                            .cornerRadius(4)
                    }
                    .buttonStyle(.plain) // macOS 上，为了自定义按钮样式，通常用 .plain
                    
                    Button {
                        songName = text2
                        artistNames = text1
                    } label: {
                        Text(text2)
                            .font(.subheadline)
                            .padding(.horizontal, 12)
                            .padding(.vertical, 4)
                            .background(songName == text2 ? Color.yellow : Color.yellow.opacity(0.3))
                            .foregroundColor(.white)
                            .cornerRadius(4)
                    }
                    .buttonStyle(.plain) // macOS 上，为了自定义按钮样式，通常用 .plain
                }
            }
            Rectangle()
                .frame(width: 1.0, height: 24.0)
            VStack(alignment: .leading, spacing: 12.0) {
                Text("设置歌手")
                HStack {
                    Button {
                        artistNames = text1
                        songName = text2
                    } label: {
                        Text(text1)
                            .font(.subheadline)
                            .padding(.horizontal, 12)
                            .padding(.vertical, 4)
                            .background(artistNames == text1 ? Color.green : Color.green.opacity(0.3))
                            .foregroundColor(.white)
                            .cornerRadius(4)
                    }
                    .buttonStyle(.plain) // macOS 上，为了自定义按钮样式，通常用 .plain
                    
                    Button {
                        artistNames = text2
                        songName = text1
                    } label: {
                        Text(text2)
                            .font(.subheadline)
                            .padding(.horizontal, 12)
                            .padding(.vertical, 4)
                            .background(artistNames == text2 ? Color.yellow : Color.yellow.opacity(0.3))
                            .foregroundColor(.white)
                            .cornerRadius(4)
                    }
                    .buttonStyle(.plain) // macOS 上，为了自定义按钮样式，通常用 .plain
                }
            }
            Rectangle()
                .frame(width: 1.0, height: 24.0)
            VStack(alignment: .leading, spacing: 12.0) {
                Text("歌曲路径")
                Text(filepath)
                    .lineLimit(1)
                    .truncationMode(.head)
            }
            Spacer()
            
            Button {
                updateSongInfo(songName ?? "", artistNames ?? "")
            } label: {
                Image(systemName: "checkmark.circle")
                    .resizable()
                    .frame(width: 24.0, height: 24.0)
                    .foregroundStyle(Color.green)
            }
            .buttonStyle(.plain) // macOS 上，为了自定义按钮样式，通常用 .plain
            .padding(.trailing, 24.0)
            
        }
        .frame(height: 48.0)
        .padding(.leading, 22.0)
        .padding(.vertical, 22.0)
    }
}
