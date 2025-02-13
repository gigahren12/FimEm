class HardManager:
    def __init__(self, disk_name):
        self.disk_name = disk_name
       

    def read_byte(self, number):
        with open(self.disk_name, 'rb') as f:
           bytes = list(f.read()) 

        return bytes[number]

               
    def write_byte(self, number, data):
        with open(self.disk_name, 'rb') as f:
           bytes = list(f.read()) 
              
        bytes[number] = data
        
        with open(self.disk_name, 'wb') as f:
            for b in bytes:
                f.write(b.to_bytes(1,'little'))
               
    def format(self,type,size):
       pass
           
       
    def load(self, name, address):
           with open(name, 'rb') as f:
               program = f.read()
               
           c = 0
           for b in program:
               self.write_byte(c + address, program[c])
               c+=1