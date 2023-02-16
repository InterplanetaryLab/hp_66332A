import pyvisa
import time
import csv

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

    # sets the current output to the input current. 
    def set_current(self,current):
        command = "SOUR:CURR %f"%current
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

    # charges with cc until volt max is reached or until the timeout occurs
    # params: volt_max (float), dis_curr (float), time_sec - duration (float)
    # set time_sec to -1 if time duration is to be ignored
    def charge_cc_until_volt(self, charge_volt, volt_max, charge_curr, time_sec, filename = ""):
        print("starting charge cycle, timeout = %f, max_volt = %f, charge_curr = %f"%(time_sec,volt_max,charge_curr))
        self.disable_output()
        self.set_current(charge_curr)
        self.set_voltage(charge_volt)

        curr_curr = self.get_curr_current()
        curr_volt = self.get_curr_voltage()

        end_time = time.time() + time_sec
        start_time = end_time-time_sec

        self.enable_output()
        try:
            if (filename != ""):
                with open(filename, 'w', newline='') as csvfile:
                    data_writer = csv.writer(csvfile, delimiter=',')
                    data_writer.writerow(["Time (s)","Voltage","Current"])
            while ((curr_volt <volt_max)):
                if (time_sec > 0 and (time.time() > end_time)):
                    break
                curr_curr = self.get_curr_current()
                curr_volt = self.get_curr_voltage()
                if (filename != ""):
                    with open(filename, 'a', newline='') as csvfile:
                        data_writer = csv.writer(csvfile, delimiter=',')
                        data_writer.writerow([time.time()-start_time,curr_volt,curr_curr])
                print("time_remaining: %f, curr_volt: %f, curr_current: %f"%(end_time-time.time(),curr_volt,curr_curr))
                time.sleep(1)

        except:
            print("exception encountered. turning off psu")
            self.disable_output()
        self.disable_output()
        print("finished charge_cycle")

    # discharges until timeout is reached or until the voltage drops
    # params: volt_min (float), dis_curr (float), time_sec - duration (float), filename = "" (set to empty string for no file writing, otherwise specify path + filename)
    # set time_sec to -1 if time duration is to be ignored
    def discharge_cc_until_volt(self, volt_min, dis_curr, time_sec, filename = ""):
        print("starting discharge cycle, timeout = %f, min_volt = %f, dis_curr = %f"%(time_sec,volt_min,dis_curr))
        self.disable_output()
        self.set_current(dis_curr)
        self.set_voltage(volt_min)
        
        curr_curr = self.get_curr_current()
        curr_volt = self.get_curr_voltage()
        end_time = time.time() + time_sec
        start_time = end_time-time_sec

        self.enable_output()
        try:
            if (filename != ""):
                with open(filename, 'w', newline='') as csvfile:
                    data_writer = csv.writer(csvfile, delimiter=',')
                    data_writer.writerow(["Time (s)","Voltage","Current"])
            while ((curr_volt >volt_min)):
                if (time_sec > 0 and (time.time() > end_time)):
                    break
                curr_curr = self.get_curr_current()
                curr_volt = self.get_curr_voltage()
                if (filename != ""):
                    with open(filename, 'a', newline='') as csvfile:
                        data_writer = csv.writer(csvfile, delimiter=',')
                        data_writer.writerow([time.time()-start_time,curr_volt,curr_curr])
                print("time_remaining: %f, curr_volt: %f, curr_current: %f"%(end_time-time.time(),curr_volt,curr_curr))
                time.sleep(1)
        except:
            print("exception encountered. turning off psu")
            self.disable_output()
        self.disable_output()
        print("finished discharge cycle")

    def get_curr_current(self):
        command = ":MEAS:CURR?"
        return_statement = self.inst.query(command)
        print(return_statement)
        return float(return_statement)
