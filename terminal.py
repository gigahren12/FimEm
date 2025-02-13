from assembler.asm import Translator
from assembler.projects import Manager
import time
import emu as e
import sys
from mem_manager import HardManager
import datetime
translator = Translator()
projman = Manager()
def get_args(command):
    comnd = command.split()
    args = {}
    for c in comnd:
        if c.startswith("-") and not comnd[comnd.index(c) + 1].startswith("-"):
            args[c.replace("-","")] = comnd[comnd.index(c) + 1]
        else:
            args[c.replace("-","")] = True
    return args

def execute_comm(com):
    if com == '' or com == 'exit' or com == 'quit':
        sys.exit()
    name = com.split()[0]
    arg = get_args(com)
    if name == 'assembly':
        with open(arg['file'], 'r') as f:
            # Читаем строки из файла, удаляем пробелы и игнорируем комментарии
            code = [row.split(';')[0].strip() for row in f if row.strip() and not row.startswith(';')]
            code = [s.split(' ') for s in code]
        start = time.time()
        program = translator.assembly(code)
        end = time.time()
        length = 0
        print(program)
        current_date = datetime.datetime.now()
        current_date_string = current_date.strftime('%d%m%y-%H%M%S')
        with open(f"{arg['file'][:-4]}-BUILD-{current_date_string}.bin", 'wb') as f:
            for b in program:
                for byte in b:
                    f.write(byte)
                    length += 1
            print(f"The building was completed successfully in {str(int((end - start) * 1000))} milliseconds with a total file weight of {length} bytes.")
            
    elif name == 'format':
        print("Cooming soon...")
            
    elif name == 'run':
        em = e.Emulator(arg['boot'],int(arg['mem']))
        em.load_program(0,0)
        em.run(0)
        
    elif name == 'load':
            memman = HardManager (arg['device'])
            memman.load(arg['file'], int(arg['address'])) 
            print('Loading completed.')
    else:
        print(f'Error: bad command "{name}"')

print("FimEm terminal.")
print("Please, write command:")

while True:
    command = input(">")
    execute_comm(command)
