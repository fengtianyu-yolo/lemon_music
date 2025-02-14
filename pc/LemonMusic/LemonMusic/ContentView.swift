//
//  ContentView.swift
//  LemonMusic
//
//  Created by 冯天宇 on 2023/10/18.
//

import SwiftUI
import Alamofire
import AVFoundation
import AppKit

struct ContentView: View {

    let categoies = [
        "音乐库",
        "歌手"
    ]
    
    @State private  var selectedItem: String? = nil
        
    var body: some View {
        
        ZStack(alignment: .leading) {
            NavigationSplitView {
                VStack {
                    HStack(spacing: 0) {
                        Text("Lemon")
                            .font(Font.custom("Chalkboard SE", size: 18.0))
                            .foregroundStyle(Color.yellow)
                        Text(".Music")
                            .font(Font.custom("Chalkboard SE", size: 18.0))
                            .foregroundStyle(Color.black)
                        Spacer()
                    }
                    .frame(height: 24)
                    .padding()
                    .background(Color.white)
                    
                    
                    List {
                        Section("音乐库") {
                            NavigationLink {
                                SongListView()
                                    .background(Color("background"))
                                    .onAppear {
                                    }
                            } label: {
                                HStack {
                                    Image( selectedItem == "songList" ? "song_list_selected" : "song_list")
                                        .resizable()
                                        .scaledToFill()
                                        .frame(width: 24.0, height: 24.0)
                                    
                                    Text("歌曲")
                                }
                                .frame(height: 36)
                            }
                            .listRowBackground(Color.clear)
                            
                            NavigationLink {
                            } label: {
                                HStack {
                                    Image("song_list")
                                        .resizable()
                                        .scaledToFill()
                                        .frame(width: 24.0, height: 24.0)
                                    
                                    Text("歌曲")
                                }
                                .frame(height: 36)
                                
                            }
                            .listRowInsets(.init(top: 8, leading: 8, bottom: 8, trailing: 8))
                            .listRowBackground(Color.clear)
                        }
                        .listRowInsets(.init(top: 8, leading: 8, bottom: 8, trailing: 8))
                        
                        Section("设备") {
                            NavigationLink {
                                TransferView()
                            } label: {
                                Text("U盘")
                                    .frame(height: 20)
                            }
                        }
                    }
                    .listStyle(SidebarListStyle())
                    .toolbar(.hidden)
                    .background(Color.white)
                }
                .frame(width: 220)
                .background(Color.white)
            } detail: {
            }
            .background(Color("background"))
            
            Rectangle()
                .frame(width: 8)
                .foregroundStyle(.white)
                .offset(x: 216)
                .edgesIgnoringSafeArea(.all)
        }
        
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}

struct SongListView: View {
    
    @StateObject private var viewModel = ViewModel()
    
    func loadImage(from imageName: String) -> NSImage? {
        
        if let path = Bundle.main.path(forResource: imageName, ofType: nil) {
            return NSImage(contentsOfFile: path)
        }
        return nil
    }
    
    var body: some View {
        VStack(alignment: .leading, spacing: 20) {
            Text("My Playlist")
                .font(Font.system(size: 44, weight: Font.Weight.bold))
                .padding(.horizontal, 20)
            
            ZStack {
                if let image = loadImage(from: "cover.JPG") {
                    Image(nsImage: image)
                        .resizable()
                        .scaledToFill()
                }
                HStack {
                    VStack(alignment: .leading, spacing: 12.0) {
                        Text("正在播放")
                            .font(Font.system(size: 12.0))
                            .foregroundStyle(.gray)
                        
                        Text("富士山下")
                            .font(Font.system(size: 32, weight: .heavy))
                            .padding(.bottom, 16)
                        
                        Button {
                            print("回到这首歌曲")
                        } label: {
                            Text("回到这里")
                                .font(Font.system(size: 12.0))
                                .foregroundStyle(.white)
                        }
                        .frame(width: 88, height: 32) // 按钮大小
                        .background(Color.black) // 圆形边框
                        .foregroundStyle(.white)
                        .clipShape(
                            RoundedRectangle(cornerSize: CGSize(width: 16, height: 16))
                        )
                        .buttonStyle(.plain)
                    }
                    Spacer()
                    VStack {
                        Text("正在搜索歌词 ...")
                            .foregroundStyle(.white)
                    }
                }.padding(40)
            }
            .frame(height: 200)
            .clipShape(
                RoundedRectangle(cornerSize: CGSize(width: 12, height: 12))
            )
            .padding(.horizontal, 40)

            SongListDetail(viewModel: viewModel)
                .padding(.horizontal, 20)
            
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
        }
        .padding(.bottom, 20)
    }
}

struct HeaderView: View {
    
    @StateObject var viewModel: ViewModel
    
    var body: some View {
        
        HStack(spacing: 22) {
            Image("music_placeholder")
                .resizable()
                .scaledToFit()
                .frame(width: 32, height: 32)
            
            VStack(alignment: .leading, spacing: 2.0) {
                Text(viewModel.selectedSong?.songName ?? "")
                    .font(Font.system(size: 14.0))
                    .foregroundColor(Color("title", bundle: nil))

                Text(viewModel.selectedSong?.artistName ?? "")
                    .font(Font.system(size: 12.0))
                    .foregroundColor(Color("subtitle", bundle: nil))

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
            
    @StateObject var viewModel: ViewModel


    var body: some View {
        
        List(viewModel.data, id: \.songId) { song in
            Row(song: song, selected: viewModel.selectedSong?.songId == song.songId)
                .frame(height: viewModel.selectedSong?.songId == song.songId ? 60: 48)
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
         
    }
}

struct Row: View {
    
    var song: SongModel
    
    var selected: Bool
    
    var body: some View {
        
        ZStack {
            if selected {
                // 背景和阴影
                RoundedRectangle(cornerRadius: 8)
                    .fill(Color.white)
                    .shadow(color: Color.black.opacity(0.1), radius: 5, x: 0, y: 2)
            }
            
            HStack(spacing: 12) {
                Text(song.songName)
                    .foregroundColor( selected ? Color("cell_text_selected") : Color("cell_text"))
                    .font(Font.system(size: 14.0, weight: selected ? .bold : .regular))
                    .frame(width: 300, alignment: .leading)
                    .padding(.leading, 24)
                
                Text("\(song.duration)")
                    .foregroundColor( selected ? Color("cell_text_selected") : Color("cell_text"))
                    .font(Font.system(size: 14.0, weight: selected ? .bold : .regular))
                    .frame(width: 60, alignment: .leading)
                Spacer()
                Text(song.artists.first?.artistName ?? "")
                    .foregroundColor( selected ? Color("cell_text_selected") : Color("cell_text"))
                    .font(Font.system(size: 14.0, weight: selected ? .bold : .regular))
                    .frame(width: 120, alignment: .leading)
            }
            .padding(.horizontal, 12)
            .contentShape(Rectangle())
        }
        .padding(4)
    }
}



struct MacBlurView: NSViewRepresentable {
    typealias NSViewType = NSVisualEffectView
    
    // 定义模糊效果的风格，可按需修改
    let material: NSVisualEffectView.Material

    func makeNSView(context: Context) -> NSVisualEffectView {
        let visualEffectView = NSVisualEffectView()
        visualEffectView.material = material
        visualEffectView.state = .active
        visualEffectView.appearance = NSAppearance(named: NSAppearance.Name.vibrantLight)
        return visualEffectView
    }
    
    func updateNSView(_ nsView: NSVisualEffectView, context: Context) {
    }
}
