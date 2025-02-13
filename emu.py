from modules import Bus
import mem_manager as mm

class Emulator:
    def __init__(self,boot,ram_sizex):
        self.ram_size = ram_sizex
        self.ram = [0] * self.ram_size   # Инициализация оперативной памяти
        self.bootdrive = boot

        self.a = 0  # Регистр a
        self.b = 0  # Регистр b
        self.c = 0  # Регистр c
        self.d = 0  # Регистр d
        self.ax = 0  # Регистр ax
        self.bx = 0  # Регистр bx
        self.cx = 0  # Регистр cx
        self.dx = 0  # Регистр dx
        self.cf = 0 # флаг сравнения
        self.esp = 0 # вершина стека
        self.ebp = 0 # база стека
        self.bp = 0 # база программы
        self.si = 0 # индекс источника
        self.bi = 0 # индекс приемника
        self.bus = Bus()
        self.stack = []
        self.running = True
        self.diskman = mm.HardManager(self.bootdrive)
        self.pc = 0
        self.instructions = {
            0x00: self.nop, 
            0x10: self.add,
            0x11: self.sub,
            0x12: self.mul,
            0x13: self.div,
            0x14: self.rem, 
            0x20: self.mov, 
            0x21: self.ld, 
            0x30: self.jmp, 
            0x50: self.stackmodel, 
            0x51: self.push, 
            0x52: self.pop, 
            0x40: self.andb, 
            0x41: self.orb, 
            0x42: self.xor, 
            0x22: self.inc, 
            0x23: self.dec, 
            0xF1: self.int, 
            0xF0: self.cmp, 
            0x31: self.ja, 
            0x32: self.jb, 
            0x33: self.je, 
            0x34: self.jne, 
            0x43: self.shr, 
            0x44: self.shl,  
            0xF2: self.entrypoint, 
            0x35: self.call, 
            0x36: self.ret, 
            0x37: self.ra, 
            0x38: self.rb, 
            0x39: self.re, 
            0x3A: self.rne,
            0x3B: self.loop, 
            0xF3: self.log, 
            0xFA: self.breakpoint, 
            0x60: self.movsb, 
            0x61: self.cmpsb, 
            0x62: self.stosb, 
            0x63: self.lodsb, 
            0x64: self.movsw, 
            0x65: self.cmpsw, 
            0x66: self.stosw, 
            0x67: self.lodsw, 
            0x68: self.lea, 
            0x70: self.rbd, 
            0x71: self.wbd, 
            0xFF: self.hlt
            }



    def parse_instruction(self, instruction):
        while len(instruction) < 4:
            instruction.append(0)
        
        opcode = instruction[0]
        arg1 = instruction[1]
        arg2 = instruction[2]
        arg3 = instruction[3]
        return opcode, arg1, arg2, arg3

    def execute_instruction(self, opcode, arg1, arg2, arg3):
        if opcode in self.instructions:
            self.instructions[opcode](arg1, arg2, arg3)
        else:
            self.log(0,0,0)
            raise TypeError(f"Unknown instruction: {opcode}")



    def load_program(self, start,address):
        byte = 0
        c = start
        count = 0
        while count < 512:
            byte = self.diskman.read_byte(c)
            self.ram[c + address] = byte
            c+=1
            count+=1
        
    def run(self, sector):
        self.instruction = [0, 0, 0, 0]
        while self.instruction[0] != 0xFA and self.running:
            self.instruction = self.ram[self.pc:self.pc + 4]
            opcode, arg1, arg2, arg3= self.parse_instruction(self.instruction)
            self.execute_instruction(opcode, arg1, arg2, arg3)
            self.pc += 4 
            
        self.log(0, 0, 0)



    def get_register_value(self, register_id):
        """Возвращает значение указанного регистра."""
            
        if register_id == 1:
            return self.a
        elif register_id == 2:
            return self.b
        elif register_id == 3:
            return self.c
        elif register_id == 4:
            return self.d
        elif register_id == 5:
            return self.ax
        elif register_id == 6:
            return self.bx
        elif register_id == 7:
            return self.cx
        elif register_id == 8:
            return self.dx
        elif register_id == 9:
            return self.bp
        elif register_id == 10:
            return self.esp
        elif register_id == 11:
            return self.ebp
        elif register_id == 12:
            return self.si
        elif register_id == 13:
            return self.bi
        else:
            
            self.log(0,0,0)
            raise ValueError(f"Ошибка: Неизвестный регистр {register_id}.")

            
    def set_register(self, reg, val):
        if reg == 1:
            self.a = val
        elif reg == 2:
            self.b = val
        elif reg == 3:
            self.c = val
        elif reg == 4:
            self.d = val
        elif reg == 5:
            self.ax = val
        elif reg == 6:
            self.bx = val
        elif reg == 7:
            self.cx = val
        elif reg == 8:
            self.dx = val
        elif reg == 9:
            self.bp = val
        elif reg == 10:
            self.esp = val
        elif reg == 11:
            self.ebp = val
        elif reg == 12:
            self.si = val
        elif reg == 13:
            self.bi = val
        else:
            self.log (0,0,0)
            raise ValueError("Некорректный регистр.")
        
    def log(self,a,b,d):
        instruction = [hex(s) for s in self.instruction]
        print("\n*LOGS*")
        print(f"*REGISTERS*\nA:{self.a}\nB:{self.b}\nC:{self.c}\nD:{self.d}\nAX:{self.ax}\nBX:{self.bx}\nCX:{self.cx}\nDX:{self.dx}\nEBP:{self.ebp}\nESP:{self.esp}\nSI:{self.si}\nBI:{self.bi}")
        print(f"*MEMORY*\nFIRST 256 BYTES OF RAM:{self.ram[:256]}\nSTACK:{self.stack}")
        print(f"*OTHER*\nPROGRAM COUNTER:{self.pc}\nLAST EXECUTED INSTRUCTION:{instruction}\nCF:{self.cf}\nBP:{self.bp}")
        
    def div_byte(self, byte_val):
        first_half = (byte_val >> 4) & 0x0F  # Первые 4 бита
        second_half = byte_val & 0x0F          # Последние 4 бита
        return first_half, second_half
        
    def comb_bytes(self, byte1, byte2):
        b1 = int(byte1).to_bytes(1, 'little')
        b2 = int(byte2).to_bytes(1, 'little')
        
        return int.from_bytes(b2 + b1,'little')
        

        
    def nop(self, arg1, arg2, arg3):
        pass
        
    def add(self, arg1, arg2, arg3):
        """Сложение."""
        f, s = self.div_byte(arg1)
        s, arg2 = arg2, s
        if arg3 == 0:
            self.set_register(f, self.get_register_value(f) + self.get_register_value (s))
        else:
            self.set_register(f, self.get_register_value(f) + arg2)

    def sub(self, arg1, arg2, arg3):
        """Вычитание."""
        f, s = self.div_byte(arg1)
        s, arg2 = arg2, s
        self.set_register(f, self.get_register_value(f) - self.get_register_value (s))

    def mul(self, arg1, arg2, arg3):
        """Умножение."""
        f, s = self.div_byte(arg1)
        s, arg2 = arg2, s
        self.set_register(f, self.get_register_value(f) * self.get_register_value (s))

    def div(self, arg1, arg2, arg3):
        """Деление."""
        f, s = self.div_byte(arg1)
        s, arg2 = arg2, s
        if self.get_register_value(s) == 0:
            self.log(0, 0, 0)
            raise ZeroDivisionError("Деление на ноль!")
        self.set_register(f, self.get_register_value(f) // self.get_register_value (s))
        
    def rem(self, arg1, arg2, arg3):
        f, s = self.div_byte(arg1)
        s, arg2 = arg2, s
        if self.get_register_value(s) == 0:
            self.log(0,0,0)
            raise ZeroDivisionError("Остаток от деления на ноль!")
        self.set_register(f, self.get_register_value(f) % self.get_register_value (s))

    def mov(self, arg1, arg2, arg3):
        f, s = self.div_byte(arg1)
        s, arg2 = arg2, s
        self.set_register(f, self.get_register_value(s))
       
    def ld(self, arg1, arg2, arg3):
        x = self.comb_bytes(arg2, arg3)
        self.set_register(arg1, x)

    def jmp(self, arg1, arg2, arg3):
        x = self.comb_bytes(arg2, arg3)
        if arg1 == 0:
            self.pc = self.bp + x - 4
        elif arg1 == 1:
            self.pc = self.bp + get_register_value(arg3) - 4
            
    def stackmodel(self, arg1, arg2, arg3):
        x = self.comb_bytes(arg2, arg3)
        self.stack = self.ram[-x:]
        del self.ram[-x:]

    def push(self, arg1, arg2, arg3):
        try:
            if arg2 == 0:
                if self.esp == 0 and self.stack[self.esp] == 0:
                    self.stack[self.esp] = self.get_register_value(arg1)
                    return 0
                self.esp += 1
                self.stack[self.esp] = self.get_register_value(arg1)
            elif arg2 == 1:
                if self.esp == 0 and self.stack[self.esp] == 0:
                    self.stack[self.esp] = arg1
                    return 0
                self.esp += 1
                self.stack[self.esp] = arg1
        except IndexError:
            self.log(0,0,0)
            raise MemoryError("Stack overflow")

    def pop(self, arg1, arg2, arg3):
        if self.esp < self.ebp:
            self.log(0, 0, 0)
            raise MemoryError("Stack empty")
        self.set_register(arg1, self.stack[self.esp])
        self.stack[self.esp] = 0
        if self.esp != 0:
            self.esp-=1
            pass

    def andb(self, arg1, arg2, arg3):
        self.set_register(arg1, self.get_register_value(arg1) & self.get_register_value(arg2))
    
    def orb(self, arg1, arg2, arg3):
        self.set_register(arg1, self.get_register_value(arg1) | self.get_register_value(arg2))
    
    def xor(self, arg1, arg2, arg3):
        self.set_register(arg1, self.get_register_value(arg1) ^ self.get_register_value(arg2))
    
    def inc(self, arg1, arg2, arg3):
        self.set_register(arg1, self.get_register_value(arg1) + 1)
    
    def dec(self, arg1, arg2, arg3):
        self.set_register(arg1, self.get_register_value(arg1) - 1)
        
    def int(self, arg1, arg2, arg3):
        buf = self.bus.interruption(arg1, [self.a, self.b, self.c, self.d])
        if arg2 != 0:
            if arg1 == 0 and self.a == 4:
                a = arg2 + self.bp 
                for c in buf:
                    self.ram[a] = c
                    a+=1
            else:
                self.set_register(arg2, buf)
    
    def cmp(self, arg1, arg2, arg3):
        if arg3 == 1:
            self.cf = self.get_register_value(arg1) - arg2
        else:
            self.cf = self.get_register_value(arg1) - self.get_register_value(arg2)
    
    def ja(self, arg1, arg2, arg3):
        if self.cf > 0:
            x = self.comb_bytes(arg2, arg3)
            if arg1 == 0:
                self.pc = self.bp + x - 4
            elif arg1 == 1:
                self.pc = self.bp + get_register_value(arg3) - 4
    
    def jb(self, arg1, arg2, arg3):
        if self.cf < 0:
            x = self.comb_bytes(arg2, arg3)
            if arg1 == 0:
                self.pc = self.bp + x - 4
            elif arg1 == 1:
                self.pc = self.bp + get_register_value(arg3) - 4
    
    def je(self, arg1, arg2, arg3):
        if self.cf == 0:
            x = self.comb_bytes(arg2, arg3)
            if arg1 == 0:
                self.pc = self.bp + x - 4
            elif arg1 == 1:
                self.pc = self.bp + get_register_value(arg3) - 4
    
    def jne(self, arg1, arg2, arg3):
        if self.cf != 0:
            x = self.comb_bytes(arg2, arg3)
            if arg1 == 0:
                self.pc = self.bp + x - 4
            elif arg1 == 1:
                self.pc = self.bp + get_register_value(arg3) - 4
    
    def shr(self, arg1, arg2, arg3):
        if arg3 == 0:
            self.set_register(arg1, self.get_register_value(arg1) >> arg2)
        elif arg3 == 1:
            self.set_register(arg1, self.get_register_value(arg1) >> self.get_register_value(arg2)) 
        
    def shl(self, arg1, arg2, arg3):
        if arg3 == 0:
            self.set_register(arg1, self.get_register_value(arg1) << arg2)
        elif arg3 == 1:
             self.set_register(arg1, self.get_register_value(arg1) << self.get_register_value(arg2)) 
        
    def entrypoint(self, arg1, arg2, arg3):
        self.bp = self.pc + 4
        
    def call(self, arg1, arg2, arg3):
        x = self.comb_bytes(arg2, arg3)
        self.push(self.pc+4,1,0)
        self.pc = self.bp + x - 4
        
    def ret(self, arg1, arg2, arg3):
        self.pc = self.stack[self.esp] - 4
        self.stack[self.esp] = 0
        self.esp-=1
        
    def ra(self, arg1, arg2, arg3):
        if self.cf > 0:
            self.pc = self.stack[self.esp] - 4
            self.stack[self.esp] = 0
            self.esp-=1
        
    def rb(self, arg1, arg2, arg3):
        if self.cf < 0:
            self.pc = self.stack[self.esp] - 4
            self.stack[self.esp] = 0
            self.esp-=1
       
    def re(self, arg1, arg2, arg3):
        if self.cf == 0:
            self.pc = self.stack[self.esp] - 4
            self.stack[self.esp] = 0
            self.esp-=1
        
    def rne(self, arg1, arg2, arg3):
        if self.cf != 0:
            self.pc = self.stack[self.esp] - 4
            self.stack[self.esp] = 0
            self.esp-=1
    
    def loop(self, arg1, arg2, arg3):
        self.c -= 1
        if self.c != 0:
            x = self.comb_bytes(arg2, arg3)
            self.pc = self.bp + x - 4
    
    def lea(self, arg1, arg2, arg3):
        x = self.comb_bytes(arg2, arg3)
        self.set_register(arg1, x + self.bp + 3)
    
    def movsb(self, arg1, arg2, arg3):
        self.ram[self.bi] = self.ram[self.si]
        
    def cmpsb(self, arg1, arg2, arg3):
        self.cf = self.ram[self.si] - self.ram[self.bi]
        
    def stosb(self, arg1, arg2, arg3):
        self.ram[self.bi] = self.get_register_value(arg1)
        
    def lodsb(self, arg1, arg2, arg3):
        self.set_register(arg1, self.ram[self.si])
    
    def movsw(self, arg1, arg2, arg3):
        self.ram[self.bi] = self.comb_bytes(self.ram[self.si], self.ram[self.si + 1]) 
        
    def cmpsw(self, arg1, arg2, arg3):
        self.cf = comb_bytes(self.ram[self.si], self.ram[self.si + 1]) - comb_bytes(self.ram[self.bi], self.ram[self.bi + 1]) 
        
    def stosw(self, arg1, arg2, arg3):
            h = hex(int(self.get_register_value(arg1)))[2:]
            if len(h) == 3:
                h1 = h[:1]
                h2 = h[1:]
                self.ram[self.bi] = int(h1, 16)
                self.ram[self.bi+1] = int(h2, 16)
            if len(h) == 4:
                h1 = h[:2]
                h2 = h[2:]
                self.ram[self.bi] = int(h1, 16)
                self.ram[self.bi + 1] = int(h2, 16)
        
    def lodsw(self, arg1, arg2, arg3):
        self.set_register(arg1, self.comb_bytes(self.ram[self.si], self.ram[self.si + 1])) 
    
    def rbd(self, arg1, arg2, arg3):
        x = self.comb_bytes(arg2, arg3)
        self.set_register(arg1, self.diskman.read_byte(x)) 
    
    def wbd(self, arg1, arg2, arg3):
        x = self.comb_bytes(arg2, arg3)
        self.diskman.write_byte(x, self.get_register_value(arg1)) 
    
    def breakpoint(self, arg1, arg2, arg3):
        pass
        
    def hlt(self, arg1, arg2, arg3):
        self.running = False