def ascii_decoder(bits):
    if len(bits) % 8 != 0:
        print(f"Предупреждение: количество бит ({len(bits)}) не кратно 8")
    
    chars = []
    for i in range(0, len(bits), 8):
        byte_bits = bits[i:i+8]
        if len(byte_bits) < 8:
            break
        char_code = 0
        for bit in byte_bits:
            char_code = (char_code << 1) | bit
        chars.append(chr(char_code))
    
    return ''.join(chars)