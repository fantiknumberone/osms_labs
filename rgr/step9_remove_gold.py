def remove_gold(decoded_bits, G):
    if len(decoded_bits) < G:
        print(f"Ошибка: декодированных битов ({len(decoded_bits)}) меньше G ({G})")
        return []
    return decoded_bits[G:]