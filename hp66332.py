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

    # static function that will perform the charge cycle tests for a list of instruments
    # params: inst_list (pyvisa instr list), charge_volt_list (float list), volt_max_list(float list), charge_curr_list (float (list), time_sec (float), filename_list (str (list))
    def charge_cc_until_volt_multiple (inst_list, charge_volt_list, volt_max_list, charge_curr_list, time_sec, filename_list = []):
        curr_curr = 0
        curr_volt = 0
        curr_time = []
        start_time = []
        running_instance = 0
        run_inst_list = []
        num_instr = len(inst_list)
        for i in range(num_instr):
            try:
                inst_list[i].disable_output()
                inst_list[i].set_current(charge_curr_list[i])
                inst_list[i].set_voltage(charge_volt_list[i])
                if (filename_list != []):
                    with open(filename_list[i], "w", newline='') as csvfile:
                        data_writer = csv.writer(csvfile, delimiter=',')
                        data_writer.writerow(["Time (s)","Voltage","Current"])
                inst_list[i].enable_output()
                start_time.append(time.time())
                curr_volt = (inst_list[i].get_curr_voltage())
                curr_curr = (inst_list[i].get_curr_current())
                run_inst_list.append(1)
            except:
                print("failed to init power supplies. Disabling output")
                for ii in range(len(inst_list)):
                    inst_list[i].disable_output()
        print('starting loop for charge')
        while (sum(run_inst_list) > 0):
            try:
                if ((time_sec > 0) and (time.time() > start_time[0] +time_sec)):
                    break;
                for i in range(num_instr):
                    if (run_inst_list[i] == 1):
                        curr_volt = (inst_list[i].get_curr_voltage())
                        curr_curr = (inst_list[i].get_curr_current())
                        curr_time = time.time() - start_time[i]
                        
                        print("instr: %d - test_time: %f, curr_volt: %f, curr_current: %f"%(i+1,curr_time,curr_volt,curr_curr))
                        if (curr_volt > volt_max_list[i]):
                            print('max voltage reached')
                            inst_list[i].disable_output()
                            run_inst_list[i] = 0
                        else:
                            if (filename_list != []):
                                with open(filename_list[i], 'a', newline='') as csvfile:
                                    data_writer = csv.writer(csvfile, delimiter=',')
                                    data_writer.writerow([curr_time,curr_volt,curr_curr])
                    else:
                        print("instr: %d disabled."%i)
                    time.sleep(1) # 1 second delay in the loop
            except:
                print("failed in loop. Turning off equipment")
                for i in inst_list:
                    i.disable_output()
                break
        for i in inst_list:
            i.disable_output()
    def discharge_cc_until_volt_multiple (inst_list, volt_min_list, charge_curr_list, time_sec, filename_list = []):
        curr_curr = 0
        curr_volt = 0
        curr_time = []
        start_time = []
        running_instance = 0
        run_inst_list = []
        num_instr = len(inst_list)
        for i in range(num_instr):
            try:
                inst_list[i].disable_output()
                inst_list[i].set_current(charge_curr_list[i])
                inst_list[i].set_voltage(0.0)
                if (filename_list != []):
                    with open(filename_list[i], "w", newline='') as csvfile:
                        data_writer = csv.writer(csvfile, delimiter=',')
                        data_writer.writerow(["Time (s)","Voltage","Current"])
                inst_list[i].enable_output()
                start_time.append(time.time())
                curr_volt = (inst_list[i].get_curr_voltage())
                curr_curr = (inst_list[i].get_curr_current())
                run_inst_list.append(1)
            except:
                print("failed to init power supplies. Disabling output")
                for ii in range(len(inst_list)):
                    inst_list[i].disable_output()
        print('starting loop for discharge')
        while (sum(run_inst_list) > 0):
            try:
                if ((time_sec > 0) and (time.time() > start_time[0] +time_sec)):
                    break;
                for i in range(num_instr):
                    if (run_inst_list[i] == 1):
                        curr_volt = (inst_list[i].get_curr_voltage())
                        curr_curr = (inst_list[i].get_curr_current())
                        curr_time = time.time() - start_time[i]
                        
                        print("instr: %d - test_time: %f, curr_volt: %f, curr_current: %f"%(i+1,curr_time,curr_volt,curr_curr))
                        if (curr_volt < volt_min_list[i]):
                            print('min voltage reached')
                            inst_list[i].disable_output()
                            run_inst_list[i] = 0
                        else:
                            if (filename_list != []):
                                with open(filename_list[i], 'a', newline='') as csvfile:
                                    data_writer = csv.writer(csvfile, delimiter=',')
                                    data_writer.writerow([curr_time,curr_volt,curr_curr])
                    else:
                        print("instr: %d disabled."%i)
                    time.sleep(1) # 1 second delay in the loop
            except:
                print("failed in loop. Turning off equipment")
                for i in inst_list:
                    i.disable_output()
                break

        for i in inst_list:
            i.disable_output()

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

        self.enable_output()

        curr_curr = self.get_curr_current()
        curr_volt = self.get_curr_voltage()

        end_time = time.time() + time_sec
        start_time = end_time-time_sec

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
