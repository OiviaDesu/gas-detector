import mysql.connector
import serial

mydb = mysql.connector.connect(
  host="localhost",
  user="oiviadesu",
  password="hidden",
  database="gas"
)

mycursor = mydb.cursor()

sql = "INSERT INTO gas (sensor_value, is_leak) VALUES (%s, %s)"

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
ser.reset_input_buffer()

while True:
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').rstrip()
        sensor_value, is_leak = line.split(" ")
        val = (sensor_value, is_leak)
        mycursor.execute(sql, val)

        mydb.commit()
        print(line)
