import pyvisa

class hp66332:
    def __init__(self, gpib_addr):
        self.rm = pyvisa.ResourceManager()
        self.gpib_addr = gpib_addr
        try:
            self.inst = self.rm.open_resource('GPIB0::%d::INSTR'%(int(gpib_addr)))
            query_result = self.inst.query("*IDN?")
            print(query_result)
            if ("HEWLETT-PACKARD,66332A" in query_result):
                self.init_valid = 1
                print("found device properly. Init valid for gpib addr: %d"%gpib_addr)
            else:
                self.init_valid = 0
                print("device not found properly. Check gpib addr - given addr: %d"%gpib_addr)
        except:
            print("failed to find device. Make sure correct identity is given")

    # enables power supply output
    def enable_output(self):
        command = "OUTP:STAT ON"      
        self.inst.write(command)

    # disables power supply output
    def disable_output(self):
        command = "OUTP:STAT OFF"      
        self.inst.write(command)

    # sets the voltage with a given voltage. Reports back the read voltage after setting it
    # arg: input_voltage - float
    def set_voltage(self, input_voltage):
        if (input_voltage <= 20.0): # max voltage is 20V
            command = "SOUR:VOLT %f"%input_voltage
            self.inst.write(command)
            
        else:
            print("invalid voltage. Exceeds limits")
            return -1 
        print("set voltage") 

    # returns curr voltage on the psu
    def get_curr_voltage(self):
        command = "MEAS:VOLTAGE?"
        return_statement = self.inst.query(command)
        return float(return_statement)

    def get_curr_current(self):
        command = ":MEAS:CURR?"
        return_statement = self.inst.query(command)
        print(return_statement)
        return float(return_statement)
