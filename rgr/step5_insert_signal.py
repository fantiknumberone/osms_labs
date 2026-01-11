import matplotlib.pyplot as plt

def create_signal(samples, total_bits, N):
    """
    Создает нулевой массив длиной 2 * N * total_bits,
    вставляет samples со смещением offset.
    """
    total_samples = N * total_bits
    signal_length = 2 * total_samples
    signal = [0] * signal_length
    
    while True:
        try:
            offset = int(input(f"Введите offset (0-{total_samples}): "))
            if 0 <= offset <= total_samples:
                break
            else:
                print(f"Ошибка: введите число от 0 до {total_samples}")
        except ValueError:
            print("Ошибка: введите целое число")
    
    signal[offset:offset + len(samples)] = samples
    
    return signal, offset

def visual_signal(signal, offset, filename=None):
    plt.figure(figsize=(12, 4))
    plt.plot(signal, drawstyle='steps-post')
    plt.title(f'Сигнал (offset={offset})')
    plt.xlabel('Номер отсчёта')
    plt.ylabel('Амплитуда')
    plt.grid(True)
    plt.axvline(x=offset, color='r', linestyle='--', alpha=0.7, label='Начало вставки')
    plt.axvline(x=offset + len(signal)//2, color='g', linestyle='--', alpha=0.7, label='Конец вставки')
    plt.legend()
    if filename:
        plt.savefig(filename, dpi=100)
        print(f"График сохранён как {filename}")
    plt.close()