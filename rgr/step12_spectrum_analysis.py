import numpy as np
import matplotlib.pyplot as plt

def compute_spectr(signal, fs=1000):
    
    n = len(signal)
    yf = np.fft.fft(signal)
    xf = np.fft.fftfreq(n, 1/fs)
    
    half_n = n // 2
    xf_one = xf[:half_n]
    yf_one = 2.0/n * np.abs(yf[:half_n])
    
    return xf_one, yf_one

def gen_sig_diff_N(bits, N_base=10):
    
    N_short = N_base // 2  # уменьшить в 2 раза
    N_medium = N_base      # оригинал
    N_long = N_base * 2    # увеличить в 2 раза
    
    signal_short = []
    signal_medium = []
    signal_long = []
    
    for bit in bits:
        signal_short.extend([bit] * N_short)
        signal_medium.extend([bit] * N_medium)
        signal_long.extend([bit] * N_long)
    
    return signal_short, signal_medium, signal_long, (N_short, N_medium, N_long)

def plot_spectr(signal_short, signal_medium, signal_long, fs=1000, filename=None):
    
    # Вычисляем спектры
    xf1, yf1 = compute_spectr(signal_short, fs)
    xf2, yf2 = compute_spectr(signal_medium, fs)
    xf3, yf3 = compute_spectr(signal_long, fs)
    
    plt.figure(figsize=(12, 6))
    plt.plot(xf1, yf1, label=f'Короткие символы (N={len(signal_short)//len(signal_medium)*10})', alpha=0.7)
    plt.plot(xf2, yf2, label=f'Средние символы (N=10)', alpha=0.7)
    plt.plot(xf3, yf3, label=f'Длинные символы (N=20)', alpha=0.7)
    
    plt.title('Спектры сигналов с разной длительностью символа')
    plt.xlabel('Частота (Гц)')
    plt.ylabel('Амплитуда')
    plt.grid(True)
    plt.legend()
    plt.xlim(0, fs/2)
    
    if filename:
        plt.savefig(filename, dpi=100)
        print(f"График сохранён как {filename}")
    plt.close()