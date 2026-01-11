import numpy as np

def gen_gold_sample(N=10):
    from step3_gold_sync import gen_gold_seq
    gold_bits = gen_gold_seq()  
    gold_samples = []
    for bit in gold_bits:
        gold_samples.extend([bit] * N)
    return gold_samples


def corr_receiver(noisy_signal, gold_samples):
    gold_len = len(gold_samples)
    signal_len = len(noisy_signal)
    
    # Вычисляем корреляцию скользящим окном
    correlations = []
    for i in range(signal_len - gold_len + 1):
        segment = noisy_signal[i:i + gold_len]
        corr = np.dot(segment, gold_samples)  # скалярное произведение
        correlations.append(corr)
    
    # Находим индекс максимальной корреляции
    start_index = np.argmax(correlations)
    max_corr = correlations[start_index]
    
    return start_index, correlations, max_corr


def remove_before_sync(noisy_signal, start_index):
    return noisy_signal[start_index:]



def visual_corr(correlations, start_index, filename=None):
    import matplotlib.pyplot as plt
    plt.figure(figsize=(12, 4))
    plt.plot(correlations, color='blue', alpha=0.7)
    plt.axvline(x=start_index, color='red', linestyle='--', label=f'Начало синхросигнала (отсчёт {start_index})')
    plt.title('Корреляция между сигналом и последовательностью Голда')
    plt.xlabel('Сдвиг (отсчёты)')
    plt.ylabel('Корреляция')
    plt.grid(True)
    plt.legend()
    if filename:
        plt.savefig(filename, dpi=100)
        print(f"График сохранён как {filename}")
    plt.close()