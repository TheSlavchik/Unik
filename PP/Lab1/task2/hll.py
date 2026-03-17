import math
import mmh3

class HyperLogLog:
    def __init__(self, p=None, q=32, eps=None):
        if eps is not None:
            self.p = max(4, int(math.ceil(2 * math.log2(1.04 / eps))))
        elif p is not None:
            self.p = p
        else:
            raise ValueError("p is not defined")
        
        self.q = q
        self.m = 2 ** self.p
        
        self.registers = [0] * self.m
        
        if self.m == 16:
            self.alpha_m = 0.673
        elif self.m == 32:
            self.alpha_m = 0.697
        elif self.m == 64:
            self.alpha_m = 0.709
        else:
            self.alpha_m = 0.7213 / (1 + 1.079 / self.m)
    
    def _hash(self, value):
        hash_int = mmh3.hash(str(value)) & (2**self.q - 1)
        return f"{hash_int:0{self.q}b}"
    
    def get_index(self, hash_binary):
        return int(hash_binary[:self.p], 2)
    
    def count_zeros(self, hash_binary):
        remaining = hash_binary[self.p:]
        
        zeros = 0
        for bit in remaining:
            if bit == '0':
                zeros += 1
            else:
                break
        
        return zeros + 1
    
    def add(self, value):
        hash_binary = self._hash(value)
        idx = self.get_index(hash_binary)
        zeroes = self.count_zeros(hash_binary)
        
        self.registers[idx] = max(self.registers[idx], zeroes)
    
    def __add__(self, other):
        if self.p != other.p or self.m != other.m:
            raise Exception("Cannot merge hll with different p or m")
        
        result = HyperLogLog(self.p, self.q)
        for i in range(self.m):
            result.registers[i] = max(self.registers[i], other.registers[i])

        return result
    
    def count(self):
        sum_inv = 0
        for val in self.registers:
            sum_inv += 2 ** -val
        
        if sum_inv == 0:
            return 0
            
        Z = 1 / sum_inv
        
        E = self.alpha_m * self.m * self.m * Z
        
        V = self.registers.count(0)
        if V > 0 and E < 2.5 * self.m:
            n_small = self.m * math.log(self.m / V)
            return int(n_small)
        
        if E > (2 ** self.q) / 30:
            n_big = -(2 ** self.q) * math.log(1 - E / (2 ** self.q))
            return int(n_big)
        
        return int(E)
