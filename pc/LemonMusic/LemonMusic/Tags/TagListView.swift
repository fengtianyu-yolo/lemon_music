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
    @State private var inputText = ""
    @StateObject var viewModel = TagViewModel()
    
    var body: some View {
        
        ZStack {
            HStack(spacing: 0) {
                // Left side: artist/tags list
                
                VStack() {
                    TextField("创建新标签", text: $inputText)
                        .padding(.leading, 8.0)
                        .frame(height: 36.0)
                        .textFieldStyle(.plain)
                        .background(content: {
                            RoundedRectangle(cornerRadius: 0)
                                .fill(.gray.opacity(0.2))
                        })
                        .padding(.horizontal, 4.0)
                        .padding(.top, 4.0)
                        .onSubmit {
                            viewModel.create(tagName: inputText)
                        }
                    
                    Button("+", action: {
                        viewModel.create(tagName: inputText)
                    })
                    .buttonStyle(.plain)
                    .frame(width: 200, height: 24)
                    
                    Divider()
   
                    List {
                        ForEach(viewModel.tagList, id: \.self) { tag in
                            Text(tag.tagName)
                                .frame(height: 36)
                                .padding(.vertical, 4)
                                .listRowInsets(EdgeInsets())
                                .listRowBackground(tag.id == viewModel.selectedTag?.id ? Color.accentColor.opacity(0.2) : Color.white)
                                .contentShape(Rectangle())
                                .onTapGesture {
                                    print("click \(tag.tagName)")
                                    viewModel.selectedTag = tag
                                }
                        }
                    }
                    .frame(maxWidth: 200)
                    .background(Color.orange)
                    .listStyle(.plain) // 让分隔线从左到右
                }
                .frame(maxWidth: 200)
                
                Divider()
                
                // Right side: songs list
                List {
                    Text(viewModel.selectedTag?.tagName ?? "")
                        .font(.title2)
                        .bold()
                        .padding(.bottom, 8)
                    ForEach(viewModel.songs) { song in
                        HStack {
                            Rectangle()
                                .fill(Color.gray)
                                .frame(width: 50, height: 50)
                                .cornerRadius(4)
                            VStack(alignment: .leading) {
                                Text(song.songName)
                                    .font(.body)
                                Text(song.formattedDuration)
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
}

struct CreatePlaylistDialog: View {
    @Binding var isPresented: Bool
    @State private var title: String = ""
    @State private var description: String = ""
    @State private var selectedCover: Int = 0
    
    var body: some View {
        ZStack {
            // 半透明遮罩
            Color.black.opacity(0.1)
                .ignoresSafeArea()
                .onTapGesture { isPresented = false }
            
            VStack(spacing: 20) {
                Text("新建播放列表")
                    .font(.headline)
                
                
                // 输入框
                VStack(spacing: 12) {
                    TextField("播放列表标题", text: $title)
                        .textFieldStyle(.roundedBorder)
                    
                    TextField("描述（可选）", text: $description)
                        .textFieldStyle(.roundedBorder)
                }
                .padding(.horizontal)
                
                // 底部按钮
                HStack {
                    Button("取消") {
                        isPresented = false
                    }
                    .keyboardShortcut(.cancelAction)
                    
                    Spacer()
                    
                    Button("创建") {
                        // TODO: 保存逻辑
                        isPresented = false
                    }
                    .keyboardShortcut(.defaultAction)
                    .disabled(title.isEmpty)
                }
                .padding(.horizontal)
            }
            .padding(20)
            .frame(width: 320)
            .background(.white)
            .cornerRadius(12)
            .shadow(radius: 10)
        }
    }
}
