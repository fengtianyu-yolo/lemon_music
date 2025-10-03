import SwiftUI

import Combine

final class ToastManager: ObservableObject {
    static let shared = ToastManager()
    
    @Published var message: String? = nil
    @Published var isVisible: Bool = false
    
    private var timer: AnyCancellable?
    
    private init() {}
    
    func show(_ message: String, duration: TimeInterval = 2.0) {
        self.message = message
        withAnimation(.easeInOut(duration: 0.3)) {
            self.isVisible = true
        }
        
        timer?.cancel()
        timer = Just(())
            .delay(for: .seconds(duration), scheduler: RunLoop.main)
            .sink { [weak self] _ in
                withAnimation(.easeInOut(duration: 0.3)) {
                    self?.isVisible = false
                }
            }
    }
}

struct ToastView: View {
    @ObservedObject var toast = ToastManager.shared
    
    var body: some View {
        Group {
            if toast.isVisible, let message = toast.message {
                VStack {
                    Spacer()
                    Text(message)
                        .font(.system(size: 14))
                        .padding(.horizontal, 16)
                        .padding(.vertical, 10)
                        .background(
                            RoundedRectangle(cornerRadius: 12)
                                .fill(Color.black.opacity(0.8))
                        )
                        .foregroundColor(.white)
                        .shadow(radius: 5)
                        .transition(.move(edge: .bottom).combined(with: .opacity))
                        .padding(.bottom, 40)
                    Spacer()
                }
                .frame(maxWidth: .infinity, maxHeight: .infinity)
                .zIndex(999)
                .animation(.easeInOut, value: toast.isVisible)
                .allowsHitTesting(false)
            }
        }
    }
}
