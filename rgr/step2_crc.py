def crc8(bits):
    poly = 0xB5  # 10111101
    crc = 0
    
    for bit in bits:
        crc ^= (bit << 7)
        for _ in range(8):
            if crc & 0x80:
                crc = (crc << 1) ^ poly
            else:
                crc <<= 1
            crc &= 0xFF
    
    
    crc_bits = [(crc >> (7 - i)) & 1 for i in range(8)]
    return crc_bits

def add_crc_to_data(data_bits):
    crc_bits = crc8(data_bits)
    return data_bits + crc_bits