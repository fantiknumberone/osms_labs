#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <stdint.h>


#define D_BITS 33          
#define POLY 0xB5             //x^7 + x^5 + x^4 + x^3 + x^2 + 1 = 10110101 = 0xB5
#define CRC_B 7            

void print_bits(uint64_t data, int bits) {
    for (int i = bits - 1; i >= 0; i--) {
        printf("%d", (data >> i) & 1);
    }
}


uint32_t calculate_crc(uint64_t data, int data_bits) {
    uint64_t mdata = data << CRC_B;     
    for (int i = data_bits + CRC_B - 1; i >= CRC_B; i--) {
        if (mdata & ((uint64_t)1 << i)) {
            mdata ^= ((uint64_t)POLY << (i - CRC_B));
        }
    }
    return (uint32_t)(mdata & ((1 << CRC_B) - 1));
}


int check_packet(uint64_t pack, int total_b) {
    uint64_t mdata = pack;
    
    for (int i = total_b - 1; i >= CRC_B; i--) {
        if (mdata & ((uint64_t)1 << i)) {
            mdata ^= ((uint64_t)POLY << (i - CRC_B));
        }
    }
    
    // Если остаток = 0, ошибок нет
    return (mdata == 0);
}

uint64_t generate_data() {
    uint64_t data = 0;
    for (int i = 0; i < D_BITS; i++) {
        data |= ((uint64_t)(rand() % 2) << i);
    }
    return data;
}

int main() {
    srand(time(NULL));
    
    
    
    printf("1.Передатчик:\n");
    uint64_t data = generate_data();
    printf(" Данные:");
    print_bits(data, D_BITS);
    printf("\n");
    
    uint32_t crc = calculate_crc(data, D_BITS);
    printf("   Вычисление CRC: ");
    print_bits(crc, CRC_B);
    printf("\n");
    
    
    uint64_t pack = (data << CRC_B) | crc;
    printf("   Отправленный пакет: ");
    print_bits(pack, D_BITS + CRC_B);
    printf("\n\n");
    
    
    printf("2. Приёмник(без ошибки):\n");
    printf("   Отправленый пакет:");
    print_bits(pack, D_BITS + CRC_B);
    printf("\n");
    
    if (check_packet(pack, D_BITS + CRC_B)) {
        printf(" Успешно \n");
    } else {
        printf(" Ошибка \n");
    }
    printf("\n");
    
    
    printf("3. Приемник с ошибкой:\n");
    int error_pos = rand() % (D_BITS + CRC_B);
    uint64_t errror_packet = pack ^ ((uint64_t)1 << error_pos);
    
    printf("   Сгенерировал ошибку на бите: %d\n", error_pos);
    printf("   Отправил     ");
    print_bits(errror_packet, D_BITS + CRC_B);
    printf("\n");
    
    if (check_packet(errror_packet, D_BITS + CRC_B)) {
        printf("   Успешно( \n");
    } else {
        printf("   ОШИБКА ОБНАРУЖЕНА\n");
    }
    
    return 0;
}