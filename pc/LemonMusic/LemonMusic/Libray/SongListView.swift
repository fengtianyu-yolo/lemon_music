//
//  SongListView.swift
//  LemonMusic
//
//  Created by 冯天宇 on 2025/6/29.
//

import SwiftUI
struct Playlist: Identifiable, Hashable {
    let id: UUID
    var name: String
    var songCount: Int
}

struct SongListView: View {
    
    @StateObject private var viewModel = ViewModel()
    @State var showTagList = false
    
    @State private var playlists: [Playlist] = [
            Playlist(id: UUID(), name: "Favorites", songCount: 15),
            Playlist(id: UUID(), name: "Workout", songCount: 22),
            Playlist(id: UUID(), name: "Chill Vibes", songCount: 18),
            Playlist(id: UUID(), name: "Road Trip", songCount: 30),
            Playlist(id: UUID(), name: "Party Mix", songCount: 25)
        ]
        
    func loadImage(from imageName: String) -> NSImage? {
        
        if let path = Bundle.main.path(forResource: imageName, ofType: nil) {
            return NSImage(contentsOfFile: path)
        }
        return nil
    }
    
    var body: some View {
        VStack(alignment: .leading, spacing: 0) {
            
            Text("My Playlist")
                .font(Font.system(size: 44, weight: Font.Weight.bold))
                .padding(.horizontal, 20)
                .padding(.vertical, 16.0)
                        
//            ZStack(alignment: .trailing) {
            SongListDetail(viewModel: viewModel)
                .contextMenu {
                    Menu {
                        // 二级菜单的内容：列出播放列表
                        ForEach(playlists) { playlist in
                            Button(playlist.name) {
                                // 添加到这个播放列表
                            }
                        }
                    } label: {
                        Label("Add to Playlist", systemImage: "text.badge.plus")
                    }
                    
                    Divider()
                    
                    Button(action: {  }) {
                        Label("显示简介", systemImage: "info.circle")
                    }
                    
                }
//                if showTagList {
//                    VStack {
//                        Text("日出BGM")
//                            .padding(.horizontal, 6.0)
//                            .padding(.vertical, 4.0)
//                            .background(RoundedRectangle(cornerRadius: 4.0))
//                    }
//                    .frame(width: 180, height: 220)
//                    .background(Color.white)
//                    
//                }
//            }
//            .padding(.top, 24.0)
            
            LibraryHeaderView()
            /*
            // 毛玻璃效果实现
            ZStack {
                MacBlurView(material: .windowBackground)
                VStack {
                    
                    HStack {
                        Spacer()
                        Button(action: {
                            viewModel.pre()
                        }) {
                            Image("pre_song")  // 替换为你的图片名称
                                .resizable()
                                .scaledToFit()
                                .frame(width: 20, height: 20)  // 根据需要调整图片大小
                        }
                        .frame(width: 32, height: 32) // 按钮大小
                        .background(Circle().strokeBorder(Color.clear, lineWidth: 2)) // 圆形边框
                        .contentShape(Circle()) // 确保点击区域为圆形
                        .buttonStyle(.plain)
                        
                        Button(action: {
                            if viewModel.playing {
                                viewModel.pause()
                            } else {
                                viewModel.resume()
                            }
                        }) {
                            Image(viewModel.playing ? "pause" : "play")  // 替换为你的图片名称
                                .resizable()
                                .scaledToFit()
                                .frame(width: 36, height: 36)  // 根据需要调整图片大小
                        }
                        .frame(width: 36, height: 36) // 按钮大小
                        .background(Circle().strokeBorder(Color.clear, lineWidth: 2)) // 圆形边框
                        .contentShape(Circle()) // 确保点击区域为圆形
                        .buttonStyle(.plain)
                        
                        
                        Button(action: {
                            viewModel.next()
                        }) {
                            Image("next_song")  // 替换为你的图片名称
                                .resizable()
                                .scaledToFit()
                                .frame(width: 20, height: 20)  // 根据需要调整图片大小
                        }
                        .frame(width: 32, height: 32) // 按钮大小
                        .background(Circle().strokeBorder(Color.clear, lineWidth: 2)) // 圆形边框
                        .contentShape(Circle()) // 确保点击区域为圆形
                        .buttonStyle(.plain)
                        Spacer()
                    }
                    
                    HStack(alignment: .center, spacing: 12) {
                        Text("0:11")
                        Rectangle()
                            .frame(height: 2)
                            .background(Color("background"))
                        Text("2:33")
                    }
                    .clipShape(RoundedRectangle(cornerRadius: 1))
                    .padding(.horizontal, 20)
                }
            }
            .frame(height: 80)
            .clipShape(RoundedRectangle(cornerRadius: 15))
            .padding(.horizontal, 80)
             */
        }
        .padding(.bottom, 0)
    }
}

struct LibraryHeaderView: View {
    
    @State var isRotating = false
    
    func loadImage(from imageName: String) -> NSImage? {
        
        if let path = Bundle.main.path(forResource: imageName, ofType: nil) {
            return NSImage(contentsOfFile: path)
        }
        return nil
    }

    var body: some View {
        HStack {
            Image(nsImage: loadImage(from: "cover.JPG")!)
                .resizable()
                .scaledToFill()
                .frame(width: 44.0, height: 44.0)
                .background(Color.red)
                .clipShape(Circle())
                .rotationEffect(.degrees(isRotating ? 360 : 0))
                .animation(
                    Animation.linear(duration: 2.0)
                        .repeatForever(autoreverses: false),
                    value: isRotating
                )
                .onAppear {
                    isRotating = true
                }
            
            VStack(alignment: .leading, spacing: 4.0) {
                Text("我们的歌")
                Text("周杰伦")
            }
            .padding(.leading, 6.0)
            Spacer()
            
            HStack {
                Button {
                    
                } label: {
                    Image(systemName: "play")
                }
                .buttonStyle(.plain)

            }
            Spacer()
        }
        .padding(.horizontal, 16.0)
        .padding(.vertical, 16.0)
//        .background(Color.red)
//        .frame(height: 22.0)
    }
}

struct SongListDetail: View {
            
    @StateObject var viewModel: ViewModel

    // 跟踪选中的行ID
    @State private var selectedItemID: Int? = nil
    @State private var lastSelectedItemID: Int? = nil
    @State private var showSelectionIndicator = true
    

    var body: some View {
        /*
        List(viewModel.data, id: \.songId) { song in
            SongItemRow(song: song, selected: viewModel.selectedSong?.songId == song.songId)
                .frame(height: viewModel.selectedSong?.songId == song.songId ? 44: 44)
                .onTapGesture {
                    viewModel.selectedSong = song
                }
                .listRowInsets(EdgeInsets())
                .listRowSeparator(.hidden) // 隐藏分隔线

        }
        .listStyle(PlainListStyle())
        .scrollContentBackground(.hidden)
        .onAppear {
        }
        */
        Table(viewModel.data) {
            TableColumn("名称", value: \.songName)
            TableColumn("时长", value: \.formattedDuration)
            TableColumn("歌手", value: \.artistName)
        }
        .onTapGesture {
            // 处理单击事件
            if let selected = selectedItemID {
                if lastSelectedItemID == selected {
                    // 双击同一行，可以触发不同操作
                    withAnimation(.spring()) {
                        // 添加脉冲动画效果
                        showSelectionIndicator = false
                        DispatchQueue.main.asyncAfter(deadline: .now() + 0.1) {
                            showSelectionIndicator = true
                        }
                    }
                    print("Double-clicked: \(viewModel.data.first(where: { $0.id == selected })?.songName ?? "")")
                } else {
                    // 点击不同行
                    lastSelectedItemID = selectedItemID
                }
            }
        }
        // 行高亮效果
        .overlay(selectionIndicator)
        // 键盘导航支持
        .onKeyPress(.downArrow) {
            moveSelection(by: 1)
            return .handled
        }
        .onKeyPress(.upArrow) {
            moveSelection(by: -1)
            return .handled
        }
        .onKeyPress(.return) {
            if let selected = selectedItemID, let item = viewModel.data.first(where: { $0.songId == selected }) {
                print("执行操作: \(item.songName)")
            }
            return .handled
        }
        // 默认选择第一行
        .onAppear {
            if viewModel.data.count > 0 {
                selectedItemID = viewModel.data[0].songId
            }
        }
    }
    
    
    // 选择指示器（高亮效果）
    private var selectionIndicator: some View {
        Group {
            if showSelectionIndicator, let selectedID = selectedItemID,
               let index = viewModel.data.firstIndex(where: { $0.songId == selectedID }) {
                Rectangle()
                    .fill(Color.accentColor.opacity(0.2))
                    .border(Color.accentColor.opacity(0.5), width: 1)
                    .frame(height: 22)
                    .padding(.horizontal, -1) // 扩展到列边缘
                    .offset(y: CGFloat(index) * 30 - 1) // 计算行位置
                    .allowsHitTesting(false) // 不影响正常点击
                    .zIndex(-1) // 在内容下方
            }
        }
    }
    
    // 键盘移动选择
    private func moveSelection(by offset: Int) {
        guard let current = selectedItemID,
              let index = viewModel.data.firstIndex(where: { $0.songId == current }) else {
            return
        }
        
        let newIndex = index + offset
        guard newIndex >= 0 && newIndex < viewModel.data.count else {
            return
        }
        
        selectedItemID = viewModel.data[newIndex].id
        lastSelectedItemID = selectedItemID
    }
}

// 增强的表格行点击处理
struct TableRowClickModifier: ViewModifier {
    let action: () -> Void
    @State private var lastClickTime: Date? = nil
    
    func body(content: Content) -> some View {
        content
            .contentShape(Rectangle())
            .onTapGesture(count: 1) {
                let now = Date()
                if let lastTime = lastClickTime, now.timeIntervalSince(lastTime) < 0.4 {
                    // 检测双击
                    lastClickTime = nil
                    print("Double click detected")
                } else {
                    // 单击
                    action()
                    lastClickTime = now
                }
            }
    }
}

extension View {
    func onRowClick(_ action: @escaping () -> Void) -> some View {
        modifier(TableRowClickModifier(action: action))
    }
}
struct SongItemRow: View {
    
    var song: SongModel
    
    var selected: Bool
    
    var body: some View {
        
        VStack {
            HStack(spacing: 12) {
                Text(song.songName)
//                    .foregroundColor( selected ? Color("cell_text_selected") : Color("cell_text"))
                    .foregroundStyle(Color.black)
                    .font(Font.system(size: 14.0, weight: selected ? .bold : .regular))
                    .frame(width: 300, alignment: .leading)
                    .padding(.leading, 24)
                
                Text("\(song.formattedDuration)")
//                    .foregroundColor( selected ? Color("cell_text_selected") : Color("cell_text"))
                    .foregroundStyle(Color.black)
                    .font(Font.system(size: 14.0, weight: selected ? .bold : .regular))
                    .frame(width: 60, alignment: .leading)
                Spacer()
                Text(song.artists.first?.artistName ?? "")
//                    .foregroundColor( selected ? Color("cell_text_selected") : Color("cell_text"))
                    .foregroundStyle(Color.black)
                    .font(Font.system(size: 14.0, weight: selected ? .bold : .regular))
                    .frame(width: 120, alignment: .leading)
            }
            .padding(.horizontal, 12)
            .contentShape(Rectangle())
            
            Divider()
        }
        .padding(4)
    }
}

#Preview {
    SongListView()
}
