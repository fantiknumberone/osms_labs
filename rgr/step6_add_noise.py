import matplotlib.pyplot as plt
import numpy as np

def add_noise(signal, sigma):

    noise = np.random.normal(0, sigma, len(signal))
    noisy_signal = [s + n for s, n in zip(signal, noise)]
    return noisy_signal, noise

def visual_noise_sig(original, noisy, offset, sigma, filename=None):
    
    fig, axes = plt.subplots(3, 1, figsize=(12, 8))
    
    
    axes[0].plot(original, drawstyle='steps-post', color='blue', alpha=0.7)
    axes[0].set_title(f'Исходный сигнал (offset={offset})')
    axes[0].set_ylabel('Амплитуда')
    axes[0].grid(True)
    axes[0].axvline(x=offset, color='r', linestyle='--', alpha=0.5)
    
    
    noise = [n - o for n, o in zip(noisy, original)]
    axes[1].plot(noise, color='gray', alpha=0.7)
    axes[1].set_title(f'Шум (σ={sigma})')
    axes[1].set_ylabel('Амплитуда')
    axes[1].grid(True)
    
    
    axes[2].plot(noisy, drawstyle='steps-post', color='orange', alpha=0.8)
    axes[2].set_title('Зашумленный принятый сигнал')
    axes[2].set_xlabel('Номер отсчёта')
    axes[2].set_ylabel('Амплитуда')
    axes[2].grid(True)
    axes[2].axvline(x=offset, color='r', linestyle='--', alpha=0.5)
    
    plt.tight_layout()
    if filename:
        plt.savefig(filename, dpi=100)
        print(f"График сохранён как {filename}")
    plt.close()