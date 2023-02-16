from hp66332 import hp66332

bat_tester = hp66332(3)

#bat_tester.set_current(.06)

#bat_tester.set_voltage(3.3)
#bat_tester.get_curr_current()
#bat_tester.disable_output()

#bat_tester.charge_cc_until_volt(3.9, .65, 500)
bat_tester.discharge_cc_until_volt(3.7,.3,-1, "data.csv")
#print(bat_tester.get_curr_voltage())
