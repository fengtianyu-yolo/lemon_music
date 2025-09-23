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
                                    .ignoresSafeArea()
                            } label: {
                                HStack {
//                                    Image( selectedItem == "songList" ? "song_list_selected" : "song_list")
//                                        .resizable()
//                                        .scaledToFill()
//                                        .frame(width: 24.0, height: 24.0)
                                    
                                    Text("歌曲")
                                }
                                .frame(height: 18)
                            }
                            .listRowBackground(Color.clear)
                            
                            NavigationLink {
                            } label: {
                                HStack {
//                                    Image("song_list")
//                                        .resizable()
//                                        .scaledToFill()
//                                        .frame(width: 24.0, height: 24.0)
                                    
                                    Text("歌手")
                                }
                                .frame(height: 18)
                                
                            }
                            .listRowInsets(.init(top: 8, leading: 8, bottom: 8, trailing: 8))
                            .listRowBackground(Color.clear)
                            
                            NavigationLink {
                                TagListView()
                                    .ignoresSafeArea()
                            } label: {
                                HStack {
//                                    Image("song_list")
//                                        .resizable()
//                                        .scaledToFill()
//                                        .frame(width: 24.0, height: 24.0)
                                    
                                    Text("标签")
                                }
                                .frame(height: 18)
                                
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
            .background(Color.white)
            
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
