#ifndef C_UTIL_H
#define C_UTIL_H

int intArray2Bool(int * arr, int size, int bit_len, int * dst_arr);
/*
 Convert an array in to bit representation with given bit_len
  */

void int2Bool(int num, int * buffer, int buffer_len);
// Convert a integer into binary with length size.

int biArray2B64Str(int * bi_arr, char * dst_arr, int bi_size);

void bi6Digit2Char(int * bi_arr, char * buffer);

#endif
