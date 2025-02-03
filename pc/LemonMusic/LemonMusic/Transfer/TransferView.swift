//
//  TransferView.swift
//  LemonMusic
//
//  Created by 冯天宇 on 2025/2/1.
//

import SwiftUI

struct TransferView: View {
    @State private var isOn = false
    
    private var viewModel = TransferViewModel()
    
    var body: some View {
        VStack {
            HStack {
                Button(action: {
                }) {
                    Text("开始同步")
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
                ForEach(Array(viewModel.data.enumerated()), id: \.element) { index, model in
                    TransferRowView(song: model.song, selected: false, isOn: $isOn)
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
