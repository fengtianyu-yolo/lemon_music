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
                .font(Font.custom("Chalkboard SE", size: 44.0))
                .padding(.horizontal, 20)
                .padding(.vertical, 16.0)
                        
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

//            LibraryHeaderView()
            HorizontalScrollableGrid(viewModel: viewModel)
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
    }
}

struct SongListDetail: View {
            
    @StateObject var viewModel: ViewModel

    // 定义列宽，这是最关键的部分，需要手动调整
    let colWidth1: CGFloat = 300 // 标题
    let colWidth2: CGFloat = 80  // 时长
    let colWidth3: CGFloat = 200 // 歌手
    let colWidth4: CGFloat = 150 // 专辑
    
    var body: some View {
        
        VStack(spacing: 0) { // 使用 VStack 容纳列头和列表，并移除默认间距
            // MARK: - 列头
            HStack {
                // Checkbox 占位符
                Image(systemName: "checkmark.circle")
                    .frame(width: 20)
                    .opacity(0) // 隐藏，只用于占位
                
                // 播放图标占位
                Image(systemName: "play.fill")
                    .frame(width: 20)
                    .opacity(0) // 隐藏，只用于占位
                
                Text("标题")
                    .font(.subheadline)
                    .frame(width: colWidth1, alignment: .leading)
                Text("时长")
                    .font(.subheadline)
                    .frame(width: colWidth2, alignment: .leading)
                Text("歌手")
                    .font(.subheadline)
                    .frame(width: colWidth3, alignment: .leading)
                Spacer() // 推开剩余空间
            }
            .padding(.horizontal, 16) // 列头与行内容保持一致的水平内边距
            .padding(.vertical, 5)
            .background(Color.secondary.opacity(0.1)) // 列头背景色
            
            // MARK: - 歌曲列表
            List {
                ForEach(Array(viewModel.data.enumerated()), id: \.element.id) { index, song in
                    SongListRow(song: song,
                                isPlaying: viewModel.playingSong == song,
                                isSelected: viewModel.selectedSong == song,
                                colWidth1: colWidth1,
                                colWidth2: colWidth2,
                                colWidth3: colWidth3,
                                colWidth4: colWidth4,
                                rowIndex: index,
                                onSingleTap: { song in
                        print("select song \(song.songName)")
                        viewModel.selectedSong = song
                    }, onDoubleTap: { song in
                        print("play song \(song.songName)")
                        viewModel.playingSong = song
                    }
                    )
                    .listRowSeparator(.hidden) // 隐藏 List 默认分隔线
                    .listRowInsets(EdgeInsets(top: 0, leading: 0, bottom: 0, trailing: 0)) // 移除默认行内边距
                    .listRowBackground(Color.clear)
                }
                
            }
            .listStyle(.plain) // 使用 PlainListStyle 移除默认列表样式
        }
    }
}

// 自定义行视图
struct SongListRow: View {
    let song: SongModel
    let isPlaying: Bool
    let isSelected: Bool
    let colWidth1: CGFloat
    let colWidth2: CGFloat
    let colWidth3: CGFloat
    let colWidth4: CGFloat
    let rowIndex: Int
    let onSingleTap: (SongModel) -> Void // 新增：单击闭包
    let onDoubleTap: (SongModel) -> Void
        
    var body: some View {
        let singleTap = TapGesture(count: 1)
            .onEnded {
                onSingleTap(song)
            }
        
        let doubleTap = TapGesture(count: 2)
            .onEnded {
                onDoubleTap(song)
            }
        HStack {
            // Checkbox (占位符)
            Image(systemName: "checkmark.circle")
                .frame(width: 20)
                .opacity(0) // 隐藏，或者根据你的数据决定是否显示
            
            // 播放图标
            Image(systemName: isPlaying ? "play.fill" : "music.note")
                .foregroundColor(isPlaying ? .accentColor : .secondary)
                .frame(width: 20)
            
            Text(song.songName)
                .frame(width: colWidth1, alignment: .leading)
            Text(song.formattedDuration)
                .frame(width: colWidth2, alignment: .leading)
            Text(song.articsName)
                .frame(width: colWidth3, alignment: .leading)
                .lineLimit(1)
                .truncationMode(.tail)
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
        .gesture(doubleTap) // 先定义双击手势
        .simultaneousGesture(singleTap) // 使用 simultaneousGesture 允许单击手势同时发生，但会优先完成
    }
}

struct HorizontalScrollableGrid: View {

    @ObservedObject var viewModel: ViewModel

    var body: some View {
        // 2. ScrollView 设置为横向滚动
        ScrollView(.horizontal, showsIndicators: true) {
            // 3. Grid 负责布局
            Grid(alignment: .leading, horizontalSpacing: 10, verticalSpacing: 8) { // 调整间距
                // 4. GridRow 用于创建行。这里我们只创建一行，所有按钮都在这一行里。
                // 如果你想多行排列，需要更复杂的逻辑，例如使用 LazyHGrid 或手动分组
                GridRow {
                    ForEach(DataCenter.shared.tagList) { tag in
                        // 5. 可点击的 Button
                        Button {
                            viewModel.addTag(tag: tag)
                            print("点击了标签: \(tag.tagName)")
                        } label: {
                            Text(tag.tagName)
                                .font(.subheadline)
                                .padding(.horizontal, 12)
                                .padding(.vertical, 4)
                                .background(viewModel.selectedTags.map({ $0.id }).contains(tag.id) ? tag.color : tag.color.opacity(0.3))
                                .foregroundColor(.white)
                                .cornerRadius(4)
                        }
                        .buttonStyle(.plain) // macOS 上，为了自定义按钮样式，通常用 .plain
                    }
                }
            }
            .padding(.horizontal) // 为整个 Grid 添加水平内边距，使其不贴边
        }
        .frame(height: 50) // 给 ScrollView 一个固定的高度，以便它能横向滚动
        .background(Color.white) // 可以给滚动视图一个背景色
    }
}

#Preview {
    SongListView()
}
