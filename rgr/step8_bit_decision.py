def decode_bits_from_samples(synced_signal, N, total_bits, P=None):
    # Если порог не задан, вычисляем автоматически
    if P is None:
        # Среднее значение сигнала (у нас есть 0 и 1 + шум)
        # Можно взять среднее между минимальным и максимальным
        min_val = min(synced_signal[:N*10])  # первые 10 бит для оценки
        max_val = max(synced_signal[:N*10])
        P = (min_val + max_val) / 2
    
    bits = []
    for i in range(0, len(synced_signal), N):
        if len(bits) >= total_bits:
            break 
        segment = synced_signal[i:i+N]
        avg = sum(segment) / len(segment)
        bit = 1 if avg > P else 0
        bits.append(bit)
    
    return bits, P

def visual_decoded(original_bits, decoded_bits, filename=None):

    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(2, 1, figsize=(12, 6))
    
    axes[0].step(range(len(original_bits)), original_bits, where='post', color='blue', label='Оригинал')
    axes[0].set_title('Оригинальные биты')
    axes[0].set_xlabel('Номер бита')
    axes[0].set_ylabel('Значение')
    axes[0].grid(True)
    axes[0].legend()
    
    axes[1].step(range(len(decoded_bits)), decoded_bits, where='post', color='orange', label='Декодировано')
    axes[1].set_title('Декодированные биты')
    axes[1].set_xlabel('Номер бита')
    axes[1].set_ylabel('Значение')
    axes[1].grid(True)
    axes[1].legend()
    
    plt.tight_layout()
    if filename:
        plt.savefig(filename, dpi=100)
        print(f"График сохранён как {filename}")
    plt.close()