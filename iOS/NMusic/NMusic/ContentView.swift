//
//  ContentView.swift
//  NMusic
//
//  Created by 冯天宇 on 2025/2/1.
//

import SwiftUI

struct ContentView: View {
    var body: some View {
        VStack {
            Image(systemName: "globe")
                .imageScale(.large)
                .foregroundStyle(.tint)
            Text("Hello, world!")
        }
        .padding()
    }
}

#Preview {
    ContentView()
}

class ViewModel {
    func registerObservers() {
        NotificationCenter.default.addObserver(self, selector: #selector(handleNotification), name: .someNotification, object: nil)
    }
}
