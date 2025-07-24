import serial
import time
import matplotlib.pyplot as plt

# Connect to CO2 sensor (e.g., K-30 sensor via serial port)
ser = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=1)
ser.flushInput()

co2_levels = []

def read_co2():
    ser.flushInput()
    ser.write(b"\xFE\x44\x00\x08\x02\x9F\x25")  # Command to request CO2 data
    time.sleep(0.5)
    resp = ser.read(7)
    if len(resp) == 7:
        high = resp[3]
        low = resp[4]
        co2 = high * 256 + low
        return co2
    else:
        return None

def control_logic(co2_value):
    # Example control logic responding to CO2 levels
    if co2_value > 800:  # ppm threshold example
        print("High CO2 detected - activating absorption process")
        # Implement actuation commands here
    else:
        print("CO2 level normal - system idle")

try:
    while True:
        co2 = read_co2()
        if co2:
            print(f"CO2 concentration: {co2} ppm")
            co2_levels.append(co2)
            control_logic(co2)
        time.sleep(1)

except KeyboardInterrupt:
    print("Stopping monitoring")

# Simple plot for CO2 data visualization
plt.plot(co2_levels)
plt.title("CO2 Concentration Over Time")
plt.xlabel("Time (s)")
plt.ylabel("CO2 ppm")
plt.show()
