#include "c_utils.h"
#include <stdlib.h>

int intArray2Bool(int * arr, int size, int bit_len, int * dst_arr){
        for(int idx = 0; idx < size; idx++){
                int2Bool(arr[idx], dst_arr, bit_len);
                dst_arr += bit_len;
        }
        return 0;
}


void int2Bool(int num, int * buffer, int buffer_len){
        buffer += (buffer_len-1);
        for(int i = 0; i<buffer_len; i++){
                *buffer = num&1;
                buffer--;
                num >>= 1;
        }
}

int biArray2B64Str(int * bi_arr, char * dst_arr, int bi_size){
        for(int i=0; i< bi_size; i += 6){
                bi6Digit2Char(bi_arr+i, dst_arr + i/6);
        }
        return 0;
}

void bi6Digit2Char(int * bi_arr, char * buffer){
        // conver 6 digits binary code into decimal
        static int operator[6] = {32, 16, 8, 4, 2, 1};
        int decimal = 0;
        for(int i=0; i < 6; i++){
                decimal += bi_arr[i]*operator[i];
        }
        // convert to char
        static char b64_table[64] = { 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '/' };
        * buffer = b64_table[decimal];
}

