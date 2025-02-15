import Foundation

struct Song: Identifiable, Codable {
    let id: UUID
    let title: String
    let artist: String
    let url: String
    
    init(id: UUID = UUID(), title: String, artist: String, url: String) {
        self.id = id
        self.title = title
        self.artist = artist
        self.url = url
    }
}