//
//  ContentView.swift
//  LemonMusic
//
//  Created by 冯天宇 on 2023/10/18.
//

import SwiftUI
import Alamofire
import AVFoundation

struct ContentView: View {
    let categoies = [
        "音乐库",
        "歌手"
    ]
    
    @State private  var selectedItem: String? = nil
        
    var body: some View {
        
        NavigationSplitView {
            HStack {
                Text("Music")
                Spacer()
            }
            .padding()
            
            List {
                Section("音乐库") {

                    NavigationLink {
                        SongListView()
                            .onAppear {
//                                let workspace = NSWorkspace.shared
//                                if let url = URL(string: "x - apple.systempreferences:com.apple.preference.security?Privacy_FullDiskAccess") {
//                                    workspace.open(url)
//                                    print("请求权限")
//                                } else {
//                                    print("没有请求权限")
//                                }
                            }
                    } label: {
                        Text("歌曲")
                            .frame(height: 20)
                    }
                    NavigationLink {
                    } label: {
                        Text("歌曲")
                            .frame(height: 20)
                    }
                }
                
                Section("设备") {
                    NavigationLink {
                    } label: {
                        Text("U盘")
                            .frame(height: 20)
                    }
                }
            }
            .listStyle(SidebarListStyle())
            .toolbar(.hidden)
        } detail: {
            Text("detail")
        }
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}

struct SongListView: View {
    
    private var viewModel = ViewModel()
    
    var body: some View {
        VStack(spacing: 0) {
            HeaderView(viewModel: viewModel)
                .frame(height: 60)
                .background(Color.white)
                .ignoresSafeArea(.all) // 忽略安全区域，从窗口顶部开始布局

            SongListDetail(viewModel: viewModel)

            Spacer()
        }
    }
}

struct HeaderView: View {
    
    @StateObject var viewModel: ViewModel
    
    var body: some View {
        
        HStack(spacing: 22) {
            Image("")
                .frame(width: 40, height: 40)
                .background(Color.red)
            
            VStack(alignment: .leading) {
                Text(viewModel.selectedSong?.songName ?? "")
                Text(viewModel.selectedSong?.artistName ?? "")
            }
            
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
                    .frame(width: 20, height: 20)  // 根据需要调整图片大小
              }
              .frame(width: 32, height: 32) // 按钮大小
              .background(Circle().strokeBorder(Color.green, lineWidth: 2)) // 圆形边框
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
        .padding(12)
    }
}

struct SongListDetail: View {
    
    var songList: [SongModel] = []
        
    @StateObject var viewModel: ViewModel


    var body: some View {
        List(viewModel.data, id: \.songId) { song in
            Row(song: song)
                .frame(height: 40)
                .background(viewModel.selectedSong?.songId == song.songId ? Color.blue : Color.clear)
                .onTapGesture {
                    print("\(song.songName)")
                    viewModel.selectedSong = song
                    
                }
                .listRowInsets(EdgeInsets())
            
        }
        .listStyle(PlainListStyle())
        .scrollContentBackground(.hidden)
    }
}

struct Row: View {
    
    var song: SongModel
    
    var body: some View {
        HStack(spacing: 0) {
            Text(song.songName)
                .frame(width: 120, height: 40)
            
            Text("\(song.duration)")
                .frame(width: 40, height: 40)
            
            Text(song.artists.first?.artistName ?? "")
                .frame(width: 80, height: 40)
            
            Spacer()
        }
        .contentShape(Rectangle())
    }
}

struct SongListResponseModel: Codable {
    var data: [SongModel]
}

struct SongModel: Equatable, Codable {
    var songId: Int
    var songName: String
    var duration: Int
    var mediaType: Int
    var sqFileName: String
    var sqFilePath: String
    var hqFileName: String
    var hqFilePath: String
    var coverPath: String
    var addedTime: String?
    var updatedTime: String?
    var artists: [ArtistModel]
    
    var artistName: String {
        if artists.isEmpty {
            return ""
        } else {
            return artists.map { $0.artistName }.joined(separator: "&")
        }
    }
    
    enum CodingKeys: String, CodingKey {
        case songId = "song_id"
        case songName = "song_name"
        case duration = "duration"
        case mediaType = "media_type"
        case sqFileName = "sq_file_name"
        case hqFileName = "hq_file_name"
        case sqFilePath = "sq_file_path"
        case hqFilePath = "hq_file_path"
        case coverPath = "cover_path"
        case addedTime = "added_time"
        case updatedTime = "updated_time"
        case artists = "artists"
    }
}

struct ArtistModel: Equatable, Codable {
    var artistName: String
    var artistId: Int
    
    enum CodingKeys: String, CodingKey {
        case artistName = "artist_name"
        case artistId = "artist_id"
    }
}
