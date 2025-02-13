from assembler.preprocess import PreProc

class Translator:
    def __init__(self):
        self.instructions_n = {
            'nop': 0, 'add': 16, 'sub': 17, 'mul': 18, 'div': 19, 'rem': 20,
            'mov': 32, 'ld': 33, 'jmp': 48, 'stack': 80, 'push': 81, 'pop': 82,
            'and': 64, 'or': 65, 'xor': 66, 'inc': 34, 'dec': 35, 'int': 241,
            'cmp': 240, 'ja': 49, 'jb': 50, 'je': 51, 'jne': 52, 'shr': 67,
            'shl': 68, 'epoint': 242, 'call': 53, 'ret': 54, 'ra': 55, 'rb': 56,
            're': 57, 'rne': 58,'loop':59, 'trap': 243,  'bpoint': 250, 'movsb':96, 
            'cmpsb':97,'stosb':98,'lodsb':99, 'movsw':100, 'cmpsw':101, 'stosw':102, 
            'lodsw':103, 'lea':104, '0':0, 'rbd':112, 'wbd':113, 
            'hlt': 255
        }
        self.prpr = PreProc()

    def parse_asm_file(self, filename):
        code = filename
        
        # Обработка директив .include
        for s in code:
            if s[0] == '.include':
                code = self.include(s[1], code, code.index(s))
        
        # Заполнение подсписков до 4 элементов и замена регистров
        for sublist in code:
            while len(sublist) < 4:
                sublist.append('0')
            if len(sublist) >= 3:
                sublist[1] = self.replace_registers(sublist[1])
                sublist[2] = self.replace_registers(sublist[2])
        
        # Предобработка кода
        code = self.prpr.Preprocessing(code)

        return code

    def replace_registers(self, element):
        registers = {
            'a': '1', 'b': '2', 'c': '3', 'd': '4',
            'ax': '5', 'bx': '6', 'cx': '7', 'dx': '8', 'bp': '9', 
            'sp':'10', 'sb':'11', 'si':'12', 'di':'13'
        }
        return registers.get(element, element)

    def replace_mnemocode(self, parse_code):
        for sublist in parse_code:
            # Замена мнемокодов на байты
            if sublist[0] in self.instructions_n:
                sublist[0] = self.instructions_n[sublist[0]]
            for i, s in enumerate(sublist):
                sublist[i] = int(s).to_bytes(1, 'little') 
        return parse_code

    def include(self, path, code, address):
        with open(path, 'r') as f:
            included_code = [
                row.split(';')[0].strip() for row in f if row.strip() and not row.startswith(';')
            ]
            included_code = [s.split(' ') for s in included_code]
        
        del code[address]
        for i in included_code:
            while len(i) < 4:
                i.append('0')
            code.insert(address + included_code.index(i), i)

        return code

    def assembly(self, filename):
        parsed_code = self.replace_mnemocode(self.parse_asm_file(filename))
        return parsed_code