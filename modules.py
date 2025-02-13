import sys
import os
import time
import random
class Bus:
    def __init__(self):
        self.table = {
        0x00: Hardware, 
        0x01: GPU
        }
        
    def interruption(self, inter, reg):
        if inter in self.table:
            id = reg.pop(0)
            int_obj = self.table[inter]()
            if id in int_obj.table:
                tmp = int_obj.table[id](reg)
                if tmp != None:
                    return tmp

class Hardware:
    def __init__(self):
        self.table = {
        0x00: self.halt, 
        0x01: self.input_int, 
        0x02: self.wait, 
        0x03: self.random_number, 
        0x04: self.input_str
        }
    
    def halt(self, reg):
        sys.exit()
    
    def input_int(self, reg):
        inp = int(input())
        return inp
    
    def wait(self, reg):
        time.sleep(reg[0] / 1000)
        
    def random_number(self, reg):
        return random.randint(reg[0], reg[1])
        
    def input_str(self, reg):
        inp = [ord(c) for c in input()]
        return inp
    
class GPU:
    def __init__(self):
        self.table = {
        0x00: self.print_ascii, 
        0x01: self.clear_console
        }
        
        
    def clear_console(self,reg):
        os.system('clear')
    
    def print_ascii(self, reg):
        print(chr(reg[2]), end='')