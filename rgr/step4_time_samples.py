import matplotlib.pyplot as plt

def bits_to_samples(bits, N):
    samples = []
    for bit in bits:
        samples.extend([bit] * N)  # повторяем бит N раз
    return samples

def visual_sample(samples, title, filename=None):
    plt.figure(figsize=(12, 3))
    plt.plot(samples, drawstyle='steps-post')
    plt.title(title)
    plt.xlabel('Номер отсчёта')
    plt.ylabel('Амплитуда')
    plt.grid(True)
    if filename:
        plt.savefig(filename, dpi=100)
        print(f"График сохранён как {filename}")
    plt.close()