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
        VStack(spacing: 0) {
            HStack {
                Text("设备管理")
                    .font(.custom("AlimamaDaoLiTi", size: 24.0))
                Spacer()
                
                Button(action: {
                }) {
                    HStack {
                        Text(viewModel.deviceName)
                            .font(.system(size: 14))
                            .foregroundColor(.black.opacity(0.8))
                        Image(systemName: "chevron.down")
                            .foregroundColor(.black.opacity(0.8))
                    }
                }
                .padding(12)
                .buttonStyle(PlainButtonStyle())
                .background(Color.white)
                .clipShape(RoundedRectangle(cornerRadius: 6))
                .overlay(
                    RoundedRectangle(cornerRadius: 6)
                        .stroke(Color.gray.opacity(0.2), lineWidth: 1)
                )
                
                
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
                            .foregroundColor(.white)
                            .frame(width: 80)
                    }
                }
                .frame(width: 88, height: 16)
                .padding(12)
                .buttonStyle(PlainButtonStyle())
                .background(Color.blue)
                .clipShape(RoundedRectangle(cornerRadius: 6))
            }
            .frame(height: 44)
            .padding(.horizontal, 12)
            .background(Color.white)
            
            HStack {
                HStack {
                    VStack(alignment: .leading) {
                        Text("使用空间")
                            .font(.system(size: 12))
                            .foregroundColor(.black.opacity(0.4))
                            .padding(.bottom, 10)
                        HStack {
                            Text("449 MB")
                                .font(.system(size: 24, weight: .bold))
                                .foregroundStyle(Color.black)
                            Spacer()
                            Text("65%")
                                .backgroundStyle(Color.green.opacity(0.3))
                                .foregroundStyle(Color.green.opacity(0.8))
                        }
                        .frame(width: 160)
                    }
                    .padding(.leading, 16)
                    .padding(.top, 16)
                    .padding(.bottom, 16)
                    .padding(.trailing, 44)
                    .background(Color.white)
                    .clipShape(RoundedRectangle(cornerRadius: 6))
                    .overlay(
                        RoundedRectangle(cornerRadius: 6)
                            .stroke(Color.gray.opacity(0.2), lineWidth: 1)
                    )
                    
                    VStack(alignment: .leading) {
                        Text("歌曲数量")
                            .font(.system(size: 12))
                            .foregroundColor(.black.opacity(0.4))
                            .padding(.bottom, 10)
                        HStack {
                            Text("449 MB")
                                .font(.system(size: 24, weight: .bold))
                                .foregroundStyle(Color.black)
                            Spacer()
                        }
                        .frame(width: 160)
                    }
                    .padding(.leading, 16)
                    .padding(.top, 16)
                    .padding(.bottom, 16)
                    .padding(.trailing, 44)
                    .background(Color.white)
                    .clipShape(RoundedRectangle(cornerRadius: 6))
                    .overlay(
                        RoundedRectangle(cornerRadius: 6)
                            .stroke(Color.gray.opacity(0.2), lineWidth: 1)
                    )
                    
                    Spacer()
                }
                .padding(12)
                .background(Color.cyan.opacity(0.1))
            }
            .padding(22)
            .background(Color.white)
            
            
            Divider()
            
            Text("歌曲列表")
            
            List {
                Section {
                    ForEach(Array(viewModel.data.enumerated()), id: \.element) { index, model in
                        TransferRowView(model: model, isOn: $isOn)
                            .listStyle(PlainListStyle())
                            .frame(height: 24)
                            .listRowInsets(EdgeInsets())
                            .listRowSeparator(.hidden) // 隐藏分隔线
                            .background( index % 2 == 0 ? Color.white : Color.gray.opacity(0.1))
                    }
                } header: {
                    HStack(spacing: 12) {
                        Toggle(isOn: $isOn) {
                            EmptyView()
                        }.hidden()
                        
                        Text("歌曲")
                            .foregroundColor(Color.black)
                            .font(Font.system(size: 14.0, weight: .regular))
                            .frame(width: 300, alignment: .leading)
                            .padding(.leading, 24)
                        
                        Text("时长")
                            .foregroundColor(Color("cell_text"))
                            .font(Font.system(size: 14.0, weight: .regular))
                            .frame(width: 60, alignment: .leading)
                        Spacer()
                        Text("歌手")
                            .foregroundColor(Color("cell_text"))
                            .font(Font.system(size: 14.0, weight: .regular))
                            .frame(width: 120, alignment: .leading)
                        
                        Spacer()
                        Text("状态")
                            .foregroundColor(Color("cell_text"))
                            .font(Font.system(size: 14.0, weight: .regular))
                            .frame(width: 120, alignment: .leading)
                    }
                    .padding(.horizontal, 12)
                } footer: {
                    
                }

                
            }
        }
    }
}

#Preview {
    TransferView()
}
