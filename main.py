import machine, time
led = machine.Pin("LED", machine.Pin.OUT)
for i in range(0, 10):
    print(i)
    led.on()
    time.sleep(0.5)
    led.off()
    time.sleep(0.5)