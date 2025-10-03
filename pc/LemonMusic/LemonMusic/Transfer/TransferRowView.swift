//
//  TransferRowView.swift
//  LemonMusic
//
//  Created by 冯天宇 on 2025/2/1.
//

import SwiftUI

struct TransferRowView: View {
    
    @StateObject var model: TransferInfoModel
    @Binding var isOn: Bool
    
    var body: some View {
        VStack {
            HStack(spacing: 0) {
                Toggle(isOn: $isOn) {
                    EmptyView()
                }
                Text(model.song.songName)
                    .foregroundColor(Color.black)
                    .font(Font.system(size: 14.0, weight: .regular))
                    .frame(width: 300, alignment: .leading)
                    .padding(.leading, 24)
                Text("\(model.song.formattedDuration)")
                    .foregroundColor(Color("cell_text"))
                    .font(Font.system(size: 14.0, weight: .regular))
                    .frame(width: 60, alignment: .leading)
                Spacer()
                Text(model.song.articsName)
                    .foregroundColor(Color("cell_text"))
                    .font(Font.system(size: 14.0, weight: .regular))
                    .frame(width: 120, alignment: .leading)                
                Text("0")
                    .foregroundColor(Color("cell_text"))
                    .font(Font.system(size: 14.0, weight: .regular))
                    .frame(width: 120, alignment: .leading)
                
                Spacer()
                if model.hasTransfered {
                    Image(systemName: "externaldrive.badge.checkmark")
                        .imageScale(.large)
                        .symbolRenderingMode(.hierarchical)
                        .foregroundStyle(.green)
                } else {
                    Image(systemName: "externaldrive.badge.xmark")
                        .imageScale(.large)
                        .symbolRenderingMode(.hierarchical)
                        .foregroundStyle(.red)
                }
                
                    
            }
//            .padding(.horizontal, 12)
            Divider()
        }
        
    }
}
