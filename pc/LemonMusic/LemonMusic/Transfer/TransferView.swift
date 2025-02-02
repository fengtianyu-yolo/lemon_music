//
//  TransferView.swift
//  LemonMusic
//
//  Created by 冯天宇 on 2025/2/1.
//

import SwiftUI

struct TransferView: View {
    @State private var isOn = false
    var body: some View {
        VStack {
            HStack {
                Button(action: {
                }) {
                    Text("全部拷贝")
                        .font(.system(size: 14))
                        .foregroundColor(.black)
                }
                .padding(.leading, 12)

//                Toggle(isOn: $isOn) {
//                    EmptyView()
//                }
//                Text("选择全部")
//                    .font(.system(size: 14))
//                    .foregroundColor(.black)
//                    .padding(.leading, 12)
                Spacer()
            }
            List {
                ForEach(Array(MusciLib.shared.data.enumerated()), id: \.element) { index, song in
                    TransferRowView(song: song, selected: false, isOn: $isOn)
                        .listStyle(PlainListStyle())
                        .frame(height: 24)
                        .listRowInsets(EdgeInsets())
                        .listRowSeparator(.hidden) // 隐藏分隔线
                        .background( index % 2 == 0 ? Color.white : Color.gray.opacity(0.1))
                }
            }
        }
    }
}

#Preview {
    TransferView()
}
