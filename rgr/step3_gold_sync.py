import matplotlib.pyplot as plt

def gen_gold_seq():
    x_reg = 0b01101
    y_reg = 0b10100
    gold_seq = []
    
    for _ in range(31):
        new_x_bit = ((x_reg >> 4) & 1) ^ ((x_reg >> 3) & 1)
        x_reg = ((x_reg << 1) & 0b11111) | new_x_bit
        x_out = (x_reg >> 4) & 1
        
        new_y_bit = ((y_reg >> 2) & 1) ^ ((y_reg >> 4) & 1)
        y_reg = ((y_reg << 1) & 0b11111) | new_y_bit
        y_out = (y_reg >> 4) & 1
        
        gold_seq.append(x_out ^ y_out)
    
    return gold_seq

def add_gold_sync(data_with_crc):
    gold_seq = gen_gold_seq()
    full_sequence = gold_seq + data_with_crc
    return full_sequence, gold_seq

def visual_seq(full_seq, gold_len, filename=None):
    plt.figure(figsize=(12, 3))
    plt.step(range(len(full_seq)), full_seq, where='post')
    plt.title('Полная последовательность: Голд + данные + CRC')
    plt.xlabel('Номер бита')
    plt.ylabel('Значение')
    plt.grid(True)
    plt.axvline(x=gold_len-0.5, color='r', linestyle='--', label='Начало данных')
    plt.legend()
    if filename:
        plt.savefig(filename, dpi=100)
        print(f"График сохранён как {filename}")
    plt.close()