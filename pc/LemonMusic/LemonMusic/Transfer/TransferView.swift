//
//  TransferView.swift
//  LemonMusic
//
//  Created by 冯天宇 on 2025/2/1.
//

import SwiftUI

struct TransferView: View {
    @State private var isOn = false
    
    @StateObject private var viewModel = TransferViewModel()
    
    var body: some View {
        VStack {
            HStack {
                Button(action: {
                    DispatchQueue.global().async {
                        viewModel.transfer()
                    }                    
                }) {
                    if viewModel.transfering {
                        ProgressView()
                            .progressViewStyle(CircularProgressViewStyle())
                            .scaleEffect(0.5)
                    } else {
                        Text("开始同步")
                            .font(.system(size: 14))
                            .foregroundColor(.black)
                    }
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
                    TransferRowView(model: model, isOn: $isOn)
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
