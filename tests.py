from Deepracer import deepracer
import time

dr = deepracer.Deepracer(base_url='https://<Your Vehicle IP Address>', password='<Your Password>')

if dr.login():
    print('Login Successful ...')
    dr.set_led_color(0, 255, 0)
    colors = dr.get_led_color()
    print(colors)

    for i in range(1, 10):
        dr.set_led_color(0,0,0,rand=True)
        time.sleep(1)

    print(dr.get_battery_level())


else:
    print("Login Failed ...")



