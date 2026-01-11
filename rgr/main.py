import matplotlib.pyplot as plt
import step1_ascii_encode as step1
import step2_crc as step2
import step3_gold_sync as step3
import step4_time_samples as step4
import step5_insert_signal as step5
import step6_add_noise as step6
import step7_correlation_receiver as step7
import step8_bit_decision as step8
import step9_remove_gold as step9
import step10_check_crc as step10
import step11_ascii_decoder as step11
import step12_spectrum_analysis as step12


def main():
    print(" Шаг 1: Ввод имени и ASCII-кодирование")
    name = input("Введите имя и фамилию латиницей: ")
    bits = step1.asc_enc(name)
    L = len(bits)
    print(f"Биты ASCII ({L} бит):")
    print(''.join(str(b) for b in bits))
    step1.visual_bits(bits, "Битовая последовательность (ASCII)", "graphics/step1_ascii_bits.png")
    
    
    print("\n Шаг 2: Вычисление CRC-8 ")
    data_with_crc = step2.add_crc_to_data(bits)
    M = 8
    print(f"Данные + CRC ({len(data_with_crc)} бит):")
    print(''.join(str(b) for b in data_with_crc))
    
    
    print("\n Шаг 3: Добавление последовательности Голда ")
    full_sequence, gold_seq = step3.add_gold_sync(data_with_crc)
    G = len(gold_seq)
    total_bits = L + M + G
    print(f"Последовательность Голда ({G} бит):")
    print(''.join(str(b) for b in gold_seq))
    print(f"Полная последовательность ({len(full_sequence)} бит):")
    print(''.join(str(b) for b in full_sequence))
    step3.visual_seq(full_sequence, len(gold_seq), "graphics/step3_full_sequence.png")
    
    
    print("\n Шаг 5: Преобразование битов во временные отсчёты ")
    N = 10
    samples = step4.bits_to_samples(full_sequence, N)
    print(f"Длина временных отсчётов: {len(samples)} (N={N})")
    step4.visual_sample(samples, "Временные отсчёты сигнала ", "graphics/step5_time_samples.png")
    
    
    print("\n Шаг 6: Создание массива Signal ")
    signal, offset = step5.create_signal(samples, total_bits, N)
    print(f"Длина массива Signal: {len(signal)} отсчётов")
    step5.visual_signal(signal, offset, "graphics/step6_signal.png")
    
    
    print("\n Шаг 7: Добавление шума ")
    sigma = float(input("Введите sigma (стандартное отклонение шума): "))
    noisy_signal, _ = step6.add_noise(signal, sigma)
    print(f"Шум добавлен (sigma={sigma})")
    step6.visual_noise_sig(signal, noisy_signal, offset, sigma, "graphics/step7_noisy_signal.png")
    
    
    print("\n Шаг 8: Корреляционный приём ")
    gold_samples = step7.gen_gold_sample(N)
    start_index, correlations, max_corr = step7.corr_receiver(noisy_signal, gold_samples)
    print(f"Начало синхросигнала (отсчёт): {start_index}")
    print(f"Максимальная корреляция: {max_corr:.2f}")
    step7.visual_corr(correlations, start_index, "graphics/step8_correlation.png")
    synced_signal = step7.remove_before_sync(noisy_signal, start_index)
    print(f"Длина сигнала после синхронизации: {len(synced_signal)} отсчётов")
    
    
    print("\n Шаг 9: Восстановление битов ")
    decoded_bits, P = step8.decode_bits_from_samples(synced_signal, N, total_bits)
    print(f"Автоматический порог P = {P:.3f}")
    print(f"Декодировано битов: {len(decoded_bits)}")
    print(f"Декодированные биты: {''.join(str(b) for b in decoded_bits)}")
    step8.visual_decoded(full_sequence, decoded_bits, "graphics/step9_decoded_bits.png")
    
    
    print("\n Шаг 10: Удаление синхросигнала ")
    data_with_crc_received = step9.remove_gold(decoded_bits, G)
    print(f"Биты после удаления Голда ({len(data_with_crc_received)} бит):")
    print(''.join(str(b) for b in data_with_crc_received))
    
    
    print("\n Шаг 11: Проверка CRC ")
    data_bits, received_crc, computed_crc, error = step10.check_crc(data_with_crc_received)
    print(f"Полученный CRC: {received_crc:08b} ({received_crc:02X}h)")
    print(f"Вычисленный CRC: {computed_crc:08b} ({computed_crc:02X}h)")
    if error:
        print("Ошибка: CRC не совпадает!")
    else:
        print("CRC совпадает — ошибок нет.")
        
        print("\n Шаг 12: ASCII-декодер ")
        text = step11.ascii_decoder(data_bits)
        print(f"Восстановленный текст: {text}")
    
    
    print("\n Шаг 13: Спектральный анализ ")
    fs = 1000  # частота дискретизации
    signal_short, signal_medium, signal_long, Ns = step12.gen_sig_diff_N(full_sequence, N_base=N)
    print(f"Длительности символов: N={Ns[0]}, {Ns[1]}, {Ns[2]}")
    
    # Спектр передаваемого сигнала (без шума)
    step12.plot_spectr(signal_short, signal_medium, signal_long, fs, "graphics/step13_spectrum_transmitted.png")
    
    # Спектр принимаемого сигнала (с шумом)
    noisy_short, _, _, _ = step12.gen_sig_diff_N(full_sequence, N_base=Ns[0])
    noisy_medium, _, _, _ = step12.gen_sig_diff_N(full_sequence, N_base=Ns[1])
    noisy_long, _, _, _ = step12.gen_sig_diff_N(full_sequence, N_base=Ns[2])
    
    # Добавляем шум к каждому
    import numpy as np
    noisy_short = [s + np.random.normal(0, sigma) for s in noisy_short]
    noisy_medium = [s + np.random.normal(0, sigma) for s in noisy_medium]
    noisy_long = [s + np.random.normal(0, sigma) for s in noisy_long]
    
    step12.plot_spectr(noisy_short, noisy_medium, noisy_long, fs, "graphics/step13_spectrum_received.png")
    
if __name__ == "__main__":
    main()