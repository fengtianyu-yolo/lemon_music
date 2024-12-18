//
//  ContentView.swift
//  LemonMusic
//
//  Created by 冯天宇 on 2023/10/18.
//

import SwiftUI
import Alamofire

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
    var body: some View {
        VStack(spacing: 0) {
            HeaderView()
                .frame(height: 40)
                .background(Color.orange)
            SongListDetail()

            Spacer()
        }
    }
}

struct HeaderView: View {
    var body: some View {
        HStack {
            Text("Header")
            Spacer()
        }
    }
}

struct SongListDetail: View {
    
    var songList: [SongModel] = [
        SongModel(id: 1, name: "我的楼兰", duration: "5:30", artist: "云朵"),
        SongModel(id: 2, name: "我的楼兰", duration: "5:30", artist: "云朵"),
        SongModel(id: 3, name: "我的楼兰", duration: "5:30", artist: "云朵"),
        SongModel(id: 4, name: "我的楼兰", duration: "5:30", artist: "云朵"),
        SongModel(id: 5, name: "我的楼兰", duration: "5:30", artist: "云朵"),
    ]
    
    @State private var selectedSong: SongModel?
    
    var body: some View {
        List(songList, id: \.id) { song in
            Row(song: song)
                .frame(height: 40)
                .background(selectedSong?.id == song.id ? Color.blue : Color.clear)
                .onTapGesture {
                    print("\(song.name)")
                    selectedSong = song
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
            Text(song.name)
                .frame(width: 120, height: 40)
            
            Text(song.duration)
                .frame(width: 40, height: 40)
            
            Text(song.artist)
                .frame(width: 80, height: 40)
            
            Spacer()
        }
        .contentShape(Rectangle())
    }
}

struct Songs: Codable {
    var songs: [SongModel]
}

struct SongModel: Equatable, Codable {
    var id: Int
    var songName: String
    var mediaType: Int
    var duration: String
    var artist: String
    
}

struct ViewModel {
    func get() {
        AF.request("127.0.0.1:5566/songs").responseDecodable(of: SongModel.self) { response in
            
        }
    }
}
