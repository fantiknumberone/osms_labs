import matplotlib.pyplot as plt

def asc_enc(name):
    bits = []
    for char in name:
        ascii_val = ord(char)
        bits.extend([int(b) for b in format(ascii_val, '08b')])
    return bits

def visual_bits(bits, title, filename=None):
    plt.figure(figsize=(10, 2))
    plt.step(range(len(bits)), bits, where='post')
    plt.title(title)
    plt.xlabel('Номер бита')
    plt.ylabel('Значение')
    plt.grid(True)
    if filename:
        plt.savefig(filename, dpi=100)
        print(f"График сохранён как {filename}")
    plt.close()  