import numpy as np

B64_TABLE = [
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",\
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",\
    "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "+", "/"
]

DECODE_DIC = {}
for i in range(len(B64_TABLE)):
    DECODE_DIC[B64_TABLE[i]] = i


class Base64_2DImageEncoder:
    OPERATOR = np.array([2**i for i in range(6)][::-1])
    CHANNEL_BYTE = 1
    BIT_BYTE = 1
    SIZE_BYTE_HALF = 3
    def __init__(self, img, bit_len = None):
        """
        @ bit_len: bit length of each pixel (for single channel)
        """
        if (img.astype(int) != img).any():
            raise Exception("Integer image is needed")
        if len(img.shape) == 2:
            self.channel = 1
        else: self.channel = img.shape[2]
        self.H = img.shape[0]
        self.W = img.shape[1]
        self.img = img
        if bit_len == None:
            max_value = np.max(img)
            max_log = np.log(max_value)/np.log(2)
            bit_len = int(np.floor(max_log) + 1)
            print("\'bit_len\' not given, using conjectural value: ", bit_len)
        self.bit = bit_len


    def calcHeader(self):
        channel_b64 = self.decimal2B64(self.channel, Base64_2DImageEncoder.CHANNEL_BYTE)
        bit_b64 = self.decimal2B64(self.bit, Base64_2DImageEncoder.BIT_BYTE)
        H_b64 = self.decimal2B64(self.H, Base64_2DImageEncoder.SIZE_BYTE_HALF)
        W_b64 = self.decimal2B64(self.W, Base64_2DImageEncoder.SIZE_BYTE_HALF)
        return channel_b64 + bit_b64 + H_b64 + W_b64

    def encode1Channel(self, im):
        """Encode one channel image"""
        # convert to binary
        bi_im = ""
        for px in im.flatten():
            bi_im += self.decimal2Binary(px, self.bit)
        bits = int(np.ceil(len(bi_im)/6))*6
        bi_im_append = bi_im + ''.join(["0"]*(bits - len(bi_im)))
        return self.binary2B64(bi_im_append)

    def run(self):
        if self.channel == 1:
            return self.calcHeader() + self.encode1Channel(self.img)
        elif self.channel >1:
            result = self.calcHeader()
            for i in range(self.channel):
                result += self.encode1Channel(self.img[:,:,i])
            return result

    def decimal2B64(self, decimal, b64byte_len):
        """calculate a decimal using given b64byte_len characters"""
        return self.binary2B64(self.decimal2Binary(decimal, b64byte_len*6))

    def binary2B64(self, binary):
        """calculate b64 characters from a binary of length being bultiples of 6"""
        if len(binary)%6 != 0:
            raise Exception("Binary served should be multiple of 6")
        b64 = []
        for i in range(0, len(binary), 6):
            b64.append(self.__binary6Digits2B64(binary[i:i+6]))
        return ''.join(b64)

    def decimal2Binary(self, decimal, bit_len = None):
        """
        convert a decimal number to binary with given bit length
        @ decimal: decimal number - int
        @ bit_len: - int
        returns a string of length bit_len
        """
        bi_raw = str(bin(decimal))[2:]
        if bit_len ==None:
            return bi_raw
        if bit_len < len(bi_raw):
            raise Exception("bit length can't hold given number")
        bi = ''.join(['0']*(bit_len-len(bi_raw))) + bi_raw
        return bi

    def __binary6Digits2B64(self, binary):
        """
        calculate b64 character from a 6 digit binary number
        @ binary: 6 digits binary - string
        """
        if len(binary) != 6 or not self.__checkBinary(binary):
            raise Exception("False format: 6 digit binary required")
        idx = self.__binary6Digits2Decimal(binary)
        return B64_TABLE[idx]

    def __checkBinary(self, param):
        if type(param) != str:
            raise Exception("Binary number should be passed as string")
        s = set(param)
        if s == {'0', '1'} or s == {'0'} or s == {'1'}:
            return True
        else: return False

    def __binary6Digits2Decimal(self, binary):
        """
        Convert 6 digits binary to decimal number
        @ binary: 6 digits binary - string
        """
        binary = np.array(list(binary)).astype(int)
        return (Base64_2DImageEncoder.OPERATOR * binary).sum()


class Base64_2DImageDecoder:
    def __init__(self, b64_string):
        self.b64 = b64_string
        self.readHeader()

    def readHeader(self):
        channel_byte = Base64_2DImageEncoder.CHANNEL_BYTE
        length_byte = Base64_2DImageEncoder.BIT_BYTE
        size_byte_half = Base64_2DImageEncoder.SIZE_BYTE_HALF
        header = []
        idx = 0
        for byte in [channel_byte, length_byte, size_byte_half, size_byte_half]:
            bi = ""
            for i in range(byte):
                bi += self.__b642Binary(self.b64[idx+i])
            info = self.__binary2DecimalNaive(bi)
            header.append(info)
            idx += byte
        self.channel, self.bit, self.H, self.W = header
        self.im_b64 = self.b64[idx:]
        self.operator = np.array([2**i for i in range(self.bit)][::-1])
        return header

    def decode1Channel(self, im_b64):
        im_bi = ""
        for c in im_b64:
            im_bi += self.__b642Binary(c)
        im_size_bi = self.H * self.W * self.bit
        im = []
        for i in range(0, im_size_bi, self.bit):
            binary = im_bi[i: i+self.bit]
            dec = self.__binary2Decimal(binary)
            im.append(dec)
        im = np.array(im).reshape((self.H, self.W))
        return im

    def run(self):
        if self.channel == 1:
            return self.decode1Channel(self.im_b64)
        else:
            channels = []
            step = int(len(self.im_b64)/self.channel)
            for idx in range(0, len(self.im_b64), step):
                im_b64 = self.im_b64[idx:idx+step]
                channels.append(self.decode1Channel(im_b64))
            return np.concatenate([c[:,:,np.newaxis] for c in channels], axis = 2)
            #return channels

    def __b642Binary(self, character):
        """Calculate single
        return 6 digits binary in string"""
        decimal = DECODE_DIC[character]
        bi = str(bin(decimal))[2:]
        return ''.join(['0']*(6-len(bi))) + bi

    def __binary2Decimal(self, binary):
        if len(binary) != self.bit:
            raise Exception("unmatched bit size")
        bi_np = np.array([int(i) for i in binary])
        return (bi_np*self.operator).sum()

    def __binary2DecimalNaive(self, binary):
        bi_np = np.array([int(i) for i in binary])
        operator = np.array([2**i for i in range(len(binary))][::-1])
        return (bi_np*operator).sum()


#==============================Encapsulation====================================

def imgEncodeB64(img, bit = None):
    """
    Encode image in Base64 scheme
    @ img: numpy array - int
    @ bit: size for each channel of a single pixel in bit
    """
    encoder = Base64_2DImageEncoder(img, bit)
    return encoder.run()

def imgDecodeB64(b64_string):
    """
    Decoder for the imgEncodeB64
    @ b64_string: string encoded with imgEncodeB64()
    """
    decoder = Base64_2DImageDecoder(b64_string)
    return decoder.run()
