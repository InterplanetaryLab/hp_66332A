from hp66332 import hp66332

bat_tester = hp66332(3)

#bat_tester.set_current(.06)

#bat_tester.set_voltage(3.3)
#bat_tester.get_curr_current()
#bat_tester.disable_output()

charge_volt = [4.2]
charge_max = [3.5]
charge_curr = [.35]
max_duration = -1
file_list = ["data3.csv"]
#hp66332.discharge_cc_until_volt_multiple ([bat_tester], charge_max, charge_curr, max_duration, filename_list = file_list)
#hp66332.charge_cc_until_volt_multiple ([bat_tester], charge_volt, charge_max, charge_curr, max_duration, filename_list = file_list)
#bat_tester.charge_cc_until_volt(4.2, 3.85, .65, -1, "data2.csv")

#bat_tester.discharge_cc_until_volt(3.6,.2,-1, "data.csv")
#print(bat_tester.get_curr_voltage())
