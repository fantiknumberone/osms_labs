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

int  check_packet(const unsigned char* packet_bits) {
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
    
   
    printf("1. Передатчик:\n");
    
    
    generate_data(data_bits);
    printf("   Данные (%d бит):\n   ", D_BITS);
    print_bits(data_bits, D_BITS);
    printf("\n");
    
   
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
    print_bits(packet_bits, TOTAL_BITS);
    printf("\n   [первые %d бит: данные, последние %d бит: CRC]\n\n", D_BITS, CRC_B);
    
  
    printf("2. Приемник (без ошибок):\n");
    if ( check_packet(packet_bits)) {
        printf("   CRC проверка пройдена\n");
    } else {
        printf("   Ошибка в пакете\n");
    }
    printf("\n");
    
   
    printf("3. Приемник (с ошибкой):\n");
    unsigned char error_packet[TOTAL_BITS];
    for (int i = 0; i < TOTAL_BITS; i++) {
        error_packet[i] = packet_bits[i];
    }
    
    int error_pos = rand() % TOTAL_BITS;
    error_packet[error_pos] ^= 1; 
    
    printf("   Внесена ошибка в бит №%d\n", error_pos);
    printf("   Ошибочный пакет:\n   ");
    print_bits(error_packet, TOTAL_BITS);
    printf("\n");
    
   
    if ( check_packet(error_packet)) {
        printf(" Ошибка не найдена \n ");
        
    } else {
        printf(" Ошибка обнаружена CRC\n");
    }
    
    return 0;
}