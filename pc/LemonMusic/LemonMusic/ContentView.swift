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
    private var viewModel = ViewModel()
    
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
    
    var songList: [SongModel] = []
    
    @State private var selectedSong: SongModel?
    
    var body: some View {
        List(songList, id: \.songId) { song in
            Row(song: song)
                .frame(height: 40)
                .background(selectedSong?.songId == song.songId ? Color.blue : Color.clear)
                .onTapGesture {
                    print("\(song.songName)")
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

class ViewModel {
    
    init() {
        get()
    }
    
    func get() {
        AF.request("http://127.0.0.1:5566/songs").responseDecodable(of: SongListResponseModel.self) { response in
            switch response.result {
            case .success(let responseModel):
                print(responseModel.data.first)
            case .failure(let error):
                print(error)
            }
        }
    }
}
