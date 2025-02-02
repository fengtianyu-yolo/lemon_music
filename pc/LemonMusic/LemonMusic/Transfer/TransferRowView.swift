//
//  TransferRowView.swift
//  LemonMusic
//
//  Created by 冯天宇 on 2025/2/1.
//

import SwiftUI

struct TransferRowView: View {
    
    var song: SongModel
    var selected = false
    @Binding var isOn: Bool
    
    var body: some View {
        HStack(spacing: 12) {
            Toggle(isOn: $isOn) {
                EmptyView()
            }
            
            Text(song.songName)
                .foregroundColor( selected ? Color("cell_text_selected") : Color("cell_text"))
                .font(Font.system(size: 14.0, weight: selected ? .bold : .regular))
                .frame(width: 300, alignment: .leading)
                .padding(.leading, 24)
            
            Text("\(song.formattedDuration)")
                .foregroundColor( selected ? Color("cell_text_selected") : Color("cell_text"))
                .font(Font.system(size: 14.0, weight: selected ? .bold : .regular))
                .frame(width: 60, alignment: .leading)
            Spacer()
            Text(song.artists.first?.artistName ?? "")
                .foregroundColor( selected ? Color("cell_text_selected") : Color("cell_text"))
                .font(Font.system(size: 14.0, weight: selected ? .bold : .regular))
                .frame(width: 120, alignment: .leading)
            
            Spacer()
            
            Image(systemName: "externaldrive.badge.xmark")
                .imageScale(.large)
                .symbolRenderingMode(.hierarchical)
                .foregroundStyle(.red)
            
//            Image(systemName: "externaldrive.badge.checkmark")
//                .imageScale(.large)
//                .symbolRenderingMode(.hierarchical)
//                .foregroundStyle(.green)
                
        }
        .padding(.horizontal, 12)
    }
}
