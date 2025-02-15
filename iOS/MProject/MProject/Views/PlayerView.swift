import SwiftUI

struct PlayerView: View {
    @StateObject private var musicPlayer = MusicPlayer()
    
    var body: some View {
        NavigationView {
            VStack {
                // 播放列表
                List(musicPlayer.playlist) { song in
                    SongRow(song: song)
                        .onTapGesture {
                            musicPlayer.play(song)
                        }
                }
                
                // 当前播放信息
                if let currentSong = musicPlayer.currentSong {
                    VStack(spacing: 10) {
                        Text(currentSong.title)
                            .font(.headline)
                        Text(currentSong.artist)
                            .font(.subheadline)
                            .foregroundColor(.secondary)
                    }
                    .padding()
                }
                
                // 播放控制
                HStack(spacing: 20) {
                    Button(action: {
                        if musicPlayer.isPlaying {
                            musicPlayer.pause()
                        } else {
                            musicPlayer.resume()
                        }
                    }) {
                        Image(systemName: musicPlayer.isPlaying ? "pause.circle.fill" : "play.circle.fill")
                            .resizable()
                            .frame(width: 44, height: 44)
                    }
                    
                    Button(action: {
                        musicPlayer.stop()
                    }) {
                        Image(systemName: "stop.circle.fill")
                            .resizable()
                            .frame(width: 44, height: 44)
                    }
                }
                .padding()
            }
            .navigationTitle("音乐播放器")
            .task {
                do {
                    try await musicPlayer.fetchPlaylist()
                } catch {
                    print("Error fetching playlist: \(error)")
                }
            }
        }
    }
}

struct SongRow: View {
    let song: Song
    
    var body: some View {
        VStack(alignment: .leading) {
            Text(song.title)
                .font(.headline)
            Text(song.artist)
                .font(.subheadline)
                .foregroundColor(.secondary)
        }
        .padding(.vertical, 4)
    }
}

#Preview {
    PlayerView()
}