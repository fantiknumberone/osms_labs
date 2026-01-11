#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>

#define D_BITS 250       
#define POLY 0xB5           //  10110101 (x^7 + x^5 + x^4 + x^3 + x^2 + 1)
#define CRC_B 7             
#define TOTAL_BITS (D_BITS + CRC_B)  


void print_bits(const unsigned char* bits, int count) {
    for (int i = count - 1; i >= 0; i--) {
        printf("%d", bits[i]);
        if (i % 8 == 0 && i != 0) printf(" ");
    }
}

void generate_data(unsigned char* data_bits) {
    for (int i = 0; i < D_BITS; i++) {
        data_bits[i] = rand() % 2;  
    }
}

void calculate_crc(const unsigned char* data_bits, unsigned char* crc_bits) {
    unsigned char temp[TOTAL_BITS];
    for (int i = 0; i < D_BITS; i++) {
        temp[i] = data_bits[i];
    }
    for (int i = 0; i < CRC_B; i++) {
        temp[D_BITS + i] = 0;
    }
    
  
    for (int i = 0; i < D_BITS; i++) {
        if (temp[i] == 1) {
            for (int j = 0; j <= CRC_B; j++) {
                int poly_bit = (POLY >> j) & 1;
                temp[i + j] ^= poly_bit;
            }
        }
    }
    for (int i = 0; i < CRC_B; i++) {
        crc_bits[i] = temp[D_BITS + i];
    }
}

int check_packet(const unsigned char* packet_bits) {
    unsigned char temp[TOTAL_BITS];
    
    
    for (int i = 0; i < TOTAL_BITS; i++) {
        temp[i] = packet_bits[i];
    }

    
    for (int i = 0; i < D_BITS; i++) {  
        if (temp[i] == 1) {
            for (int j = 0; j <= CRC_B; j++) {
                int poly_bit = (POLY >> j) & 1;
                temp[i + j] ^= poly_bit;
            }
        }
    }
    
    
    for (int i = 0; i < TOTAL_BITS; i++) {
        if (temp[i] != 0) {
            return 0;  
        }
    }
    return 1;  
}

int main() {
    srand(time(NULL));
    
    unsigned char data_bits[D_BITS];   
    unsigned char crc_bits[CRC_B];      
    unsigned char packet_bits[TOTAL_BITS]; 
    unsigned char test_packet[TOTAL_BITS];
    
    
    printf("1. Передатчик:\n");
    generate_data(data_bits);
    printf("   Данные (%d бит):\n   ", D_BITS);
    print_bits(data_bits, 40); 
    printf("...\n");
    calculate_crc(data_bits, crc_bits);
    printf("   Вычисленный CRC (%d бит):\n   ", CRC_B);
    print_bits(crc_bits, CRC_B);
    printf("\n");
    
    for (int i = 0; i < D_BITS; i++) {
        packet_bits[i] = data_bits[i];
    }
    for (int i = 0; i < CRC_B; i++) {
        packet_bits[D_BITS + i] = crc_bits[i];
    }
    
    printf("   Пакет для отправки (%d бит):\n   ", TOTAL_BITS);
    print_bits(packet_bits, 40);  
    printf("...\n");
    
   
    printf("2. Приемник (без ошибок):\n");
    if (check_packet(packet_bits)) {
        printf("    CRC проверка пройдена (пакет корректен)\n");
    } else {
        printf("   ✗Ошибка в пакете\n");
    }
    printf("\n");
    

    printf("3. Приемник (с одной ошибкой):\n");
    int error_pos = rand() % TOTAL_BITS;
    for (int i = 0; i < TOTAL_BITS; i++) {
        test_packet[i] = packet_bits[i];
    }
    test_packet[error_pos] ^= 1;
    printf("   Внесена ошибка в бит №%d\n", error_pos);
    if (check_packet(test_packet)) {
        printf("   CRC проверка пройдена\n");
    } else {
        printf("   Ошибка обнаружена CRC\n");
    }
    printf("\n");
    


    printf("4. Тестирование всех битов (от 0 до %d):\n", TOTAL_BITS - 1);
    int errors_detected = 0;   
    int errors_missed = 0;      
    
    
    for (int bit_pos = 0; bit_pos < TOTAL_BITS; bit_pos++) {
        for (int i = 0; i < TOTAL_BITS; i++) {test_packet[i] = packet_bits[i];}
        test_packet[bit_pos] ^= 1;
        if (check_packet(test_packet)) {

            errors_missed++;
            if (errors_missed <= 5) {  
                printf("   - Бите %d: ошибка НЕ обнаружена! ", bit_pos);
                if (bit_pos < D_BITS) {
                    printf("(бит данных)\n");
                } else {
                    printf("(бит CRC, позиция %d в CRC)\n", bit_pos - D_BITS);
                }
            }
        } else { errors_detected++;}
    }
    printf("   - Ошибок обнаружено: %d\n", errors_detected);
    printf("   - Ошибок не обнаружено: %d\n", errors_missed);
     if (errors_missed > 0) {
        double percentage_missed = (errors_missed * 100.0) / TOTAL_BITS;
        printf("   - Процент необнаруженных ошибок: %.2f%%\n", percentage_missed);}
    return 0;
}