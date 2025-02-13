
#from assembler.errors import *
class PreProc:
    def __init__(self):
        self.in_byte_list = ["add","sub","mul","div","rem","mov"]
        self.two_bytes_inst = ["ld","jmp","stack", "ja","jb","je","jne","call","loop","rbd","wbd","lea"]
        self.contran = ["ja","jb","je","jne"]
  
    def _inbyte (self, first_half, second_half):
       return (int(first_half) << 4) | int(second_half) 
       
    def Preprocessing(self, code):
        return self.combine_bytes(self.two_byte(self.twobyteswap(self.special_symbols(self.variable_processing(self.label_processing(code)))))) 
        
    def combine_bytes(self, code):
        try:
            for i in code:
                if i[0] in self.in_byte_list:
                    i[1] = str(self._inbyte(i[1],i[2])) 
        except Exception as e:
            print(type(e),e) 
        return code
         
    def two_byte(self, code):
        for i in code:
            try:
                if int(i[3]) > 255:
                    h = hex(int(i[3]))[2:]
                    if len(h) == 3:
                        h1 = h[:1]
                        h2 = h[1:]
                        i[2] = str(int(h1, 16))
                        i[3] = str(int(h2, 16)) 
                    if len(h) == 4:
                        h1 = h[:2]
                        h2 = h[2:]
                        i[2] = str(int(h1, 16))
                        i[3] = str(int(h2, 16))
            except Exception as e:
                print(type(e),e) 
        return code
        
    def twobyteswap(self,code):
        try:
            for i in code:
                if i[0] == 'jmp':
                    i[1], i[2] = i[2], i[1]
                
                if i[0] == 'call':
                    i[1], i[2] = i[2], i[1]
                    
                if i[0] == 'loop':
                    i[1], i[2] = i[2], i[1]
                
                
                if i[0] in self.two_bytes_inst and i[3] == '0':
                    i[3], i[2] = i[2], i[3]
                
                if i[0] in self.contran:
                     i[1], i[3] = i[3], i[1]
                     i[1] = i[2]
                     i[2] = '0'
                 
             
                if i[0] == 'stack':
                    i[3] = i[1]
                    i[1] = '0'
        except Exception as e:
            print(type(e),e) 
             
        for I in code:
            print(I)

        return code
    
    def label_processing(self, code):
        labels = {}
        labcor = 1
        for d in code:
            if d[0] == '.bytes':
                labcor+=1
        
        for i in code:
            if i[0].endswith(':'):
                labels[i[0][:-1]] = code.index(i) * 4 - labcor * 4
                del code[code.index(i)]
        
        
        for ins in code:
            if ins[1] in labels.keys():
                ins[1] = str(labels[ins[1]]) 
            if ins[2] in labels.keys():
                ins[2] = str(labels[ins[2]]) 
            if ins[3] in labels.keys():
                ins[3] = str(labels[ins[3]])
             
        for k,v in labels.items():
            print(f'Label "{k}" replaced on address {hex(v)}')
            
        return code
        
    def special_symbols(self, code):
        try:
            for elm in code:
                if elm[1] == '$':
                    elm[1] = str(code.index(elm) * 4 -4) 
                if elm[2] == '$':
                    elm[2] = str(code.index(elm) * 4 -4) 
                if elm[3] == '$':
                    elm[3] = str(code.index(elm) * 4 -4) 
        except Exception as e:
             print(type(e),e) 
    
        return code
    
    def variable_processing(self, code):
        directives = []
        vars = []
        vars_adrs = {}
        for c in code:
            if c[0] == '.bytes':
                directives.append(c)

        for I in directives:
            for x in code:
                if x[0] == '.bytes':
                    del code[code.index(x)]
                
       
        for v in directives:
             if v[1] == 'db':
                 if v[3].startswith('"') and v[3].endswith('"'):
                     chrs = [ord(c) for c in v[3].strip('"').replace('_',' ')]
                     vars.append('0')
                     for ch in chrs:
                         vars.append(str(ch)) 
                     vars_adrs[v[2]] = len(code) * 4 + len(vars) - 4 - 1 - len(chrs) - 2
                 else:
                     vars.append('0')
                     vars.append(v[3])
                     vars_adrs[v[2]] = len(code) * 4 + len(vars) - 4 - 1
             if v[1] == 'dw':
                 vars.append('0')
                 if int(v[3]) > 255:
                    h = hex(int(v[3]))[2:]
                    if len(h) == 3:
                        h1 = h[:1]
                        h2 = h[1:]
                        vars.append(str(int(h1, 16)))
                        vars.append(str(int(h2, 16))) 
                    if len(h) == 4:
                        h1 = h[:2]
                        h2 = h[2:]
                        vars.append(str(int(h1, 16)))
                        vars.append(str(int(h2, 16))) 

                 vars_adrs[v[2]] = len(code) * 4 + len(vars) - 4 - 2
                 
        print((vars_adrs))
        for c in code:
             if c[1].startswith('%'):
                 c[1] = str(vars_adrs[c[1][1:]]) 

             if c[2].startswith('%'):
                 c[2] = str(vars_adrs[c[2][1:]]) 

             if c[3].startswith('%'):
                 c[3] = str(vars_adrs[c[3][1:]]) 
        code.append(vars)
        
        if code[-1] == []:
            del code[-1]
        
        return code
