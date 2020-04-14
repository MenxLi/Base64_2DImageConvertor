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
