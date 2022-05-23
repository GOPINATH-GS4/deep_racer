from Deepracer import deepracer
import time

dr = deepracer.Deepracer(base_url='https://10.0.0.72', password='Merck12+0$')

if dr.login():
    print('Login Successful ...')
    dr.stop()
    dr.set_calibration_mode()
    time.sleep(1)
    dr.set_led_color(255, 0, 0)
    time.sleep(2)
    colors = dr.get_led_color()
    print(colors)

    for i in range(1, 10):
        dr.set_led_color(0,0,0,rand=True)
        time.sleep(1)

    print(dr.get_battery_level())


else:
    print("Login Failed ...")



