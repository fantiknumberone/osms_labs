from step2_crc import crc8

def check_crc(data_with_crc_bits):
    if len(data_with_crc_bits) < 8:
        print("Ошибка: слишком мало бит для CRC")
        return [], 0, 0, True
    
    data_bits = data_with_crc_bits[:-8]
    received_crc_bits = data_with_crc_bits[-8:]
    

    received_crc = 0
    for bit in received_crc_bits:
        received_crc = (received_crc << 1) | bit
    
    
    computed_crc_bits = crc8(data_bits)
    computed_crc = 0
    for bit in computed_crc_bits:
        computed_crc = (computed_crc << 1) | bit
    
    error = (received_crc != computed_crc)
    
    return data_bits, received_crc, computed_crc, error