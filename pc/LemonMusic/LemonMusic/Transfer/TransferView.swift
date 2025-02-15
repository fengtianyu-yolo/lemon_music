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
    @State private var isAnimating = false
    
    var body: some View {
        ZStack {
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
                    HStack(spacing: 16.0) {
                        VStack(alignment: .leading) {
                            Text("可用空间")
                                .font(.system(size: 12))
                                .foregroundColor(.black.opacity(0.4))
                                .padding(.bottom, 10)
                            HStack {
                                Text("\(viewModel.deviceFormattedCapacity) GB")
                                    .font(.system(size: 24, weight: .bold))
                                    .foregroundStyle(Color.black)
                                Spacer()
                                Text("\(viewModel.deviceCapacityUsage)%")
                                    .padding(.horizontal, 8.0)
                                    .padding(.vertical, 4.0)
                                    .background(Color.green.opacity(0.2))
                                    .clipShape(RoundedRectangle(cornerRadius: 16.0))
                                    .overlay(content: {
                                        RoundedRectangle(cornerRadius: 16.0)
                                               .stroke(Color.green.opacity(0.8), lineWidth: 1)
                                    })
                                    .foregroundStyle(Color.green.opacity(0.8))
                            }
                            .frame(width: 160)
                        }
                        .padding(.leading, 16)
                        .padding(.top, 16)
                        .padding(.bottom, 16)
                        .padding(.trailing, 16)
                        .background(Color.white)
                        .clipShape(RoundedRectangle(cornerRadius: 12.0))
                        .overlay(
                            RoundedRectangle(cornerRadius: 12.0)
                                .stroke(Color.gray.opacity(0.2), lineWidth: 1)
                        )
                        
                        VStack(alignment: .leading) {
                            Text("歌曲数量")
                                .font(.system(size: 12))
                                .foregroundColor(.black.opacity(0.4))
                                .padding(.bottom, 10)
                            HStack {
                                Text("\(viewModel.transferSongsCount)")
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
                }
                .padding(22)
                .background(Color.white)
                
                HStack(spacing: 0) {
                    Toggle(isOn: $isOn) {
                        EmptyView()
                    }
                    
                    Text("歌曲")
                        .foregroundColor(Color("cell_text"))
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
                    Text("播放次数")
                        .foregroundColor(Color("cell_text"))
                        .font(Font.system(size: 14.0, weight: .regular))
                        .frame(width: 120, alignment: .leading)
                    Spacer()
                    Text("状态")
                        .foregroundColor(Color("cell_text"))
                        .font(Font.system(size: 14.0, weight: .regular))
                        .frame(width: 120, alignment: .leading)
                }
                .frame(height: 44.0)
                .padding(.horizontal, 14)
    //            .background(Color.gray.opacity(0.2))
                .background(Color.cyan.opacity(0.1))

                
                List {
                    let source = viewModel.transfering ? viewModel.usbDatas : viewModel.data
                    ForEach(Array(source.enumerated()), id: \.element) { index, model in
                        TransferRowView(model: model, isOn: $isOn)
                            .listStyle(PlainListStyle())
                            .frame(height: 44)
                            .listRowInsets(EdgeInsets(top: 0, leading: 0, bottom: 0, trailing: 0))
                            .listRowSeparator(.hidden) // 隐藏分隔线
                           // .background( index % 2 == 0 ? Color.white : Color.gray.opacity(0.1))
                            .background( Color.white)
                    }
                    
                }
                .padding(0)
            }
            .background(Color.white)
            
            if viewModel.transfering {
                RoundedRectangle(cornerRadius: 40)
                    .fill(Color.gray.opacity(0.1))
                    .frame(width: 400, height: 80)
                    .overlay(
                        HStack(spacing: 16) {
                            // 左侧图标
                            Image(systemName: "doc.fill")
                                .resizable()
                                .scaledToFit()
                                .frame(width: 40, height: 40)
                                .foregroundColor(.blue)
                                .padding(.leading, 24)
                            
                            VStack(alignment:.leading, spacing: 4) {
                                // 文件名
                                Text(viewModel.currentFile)
                                    .font(.headline)
                                    .foregroundColor(.primary)
                                //                                   .offset(y: isAnimating ? -80 : 0)
                                //                                   .animation(.easeInOut(duration: 0.3), value: isAnimating)
                                
                                // 文件大小
                                Text(viewModel.currentFileSize)
                                    .font(.subheadline)
                                    .foregroundColor(.secondary)
                                //                                   .offset(y: isAnimating ? -80 : 0)
                                //                                   .animation(.easeInOut(duration: 0.3), value: isAnimating)
                            }
                            Spacer()
                        }
                    )
                    .offset(y: 300)
            }
        }
        
    }
}

#Preview {
    TransferView()
}
