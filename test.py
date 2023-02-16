from hp66332 import hp66332

bat_tester = hp66332(3)

#bat_tester.set_current(.06)

#bat_tester.set_voltage(3.3)
#bat_tester.get_curr_current()
#bat_tester.disable_output()

#bat_tester.charge_cc_until_volt(4.2, 3.85, .65, -1, "data2.csv")
bat_tester.discharge_cc_until_volt(3.6,.2,-1, "data.csv")
#print(bat_tester.get_curr_voltage())
