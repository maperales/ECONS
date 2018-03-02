import network
import socket 
import machine


#Fichero HTML a mandar
html1 = """<!DOCTYPE html>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />

<html>
<center>
<img src="http://ftp.us.es/ftp/pub/Logos/marca-dos-tintas_150.gif" ALT="LOGO_UNIV">  
</center>
  <head> <title>Página de prueba</title> </head>
<style >   
	.border {     
	  border-color : green;
	  border-style: double;
	  border-radius: 15px;
	  border-width : 10px;
	 }
	.fondo {
	background-color: rgb(240, 220, 180);
	padding: 20px 50px; 
	color: indigo;
	}

	.texto {
	font-family: "Helvetica";
	font-size: 18px;
	}
</style>
<head> <title>ESP8266 LED ON/OFF</title> </head>
<center><h2>Servidor Web mínimo con el ESP8266</h2></center>
<center><h3>Enciende/apaga led y lee ADC</h3></center>
<form>
<div class="border fondo texto "> 
ADC: 
<button name="ADC" value="READ" type="submit12">LEE ADC</button> = %d
</div>   

<br><br>
<div class="border fondo texto "> 

LED2: 
<button name="LED" value="ON2" type="submit">LED ON</button>
<button name="LED" value="OFF2" type="submit">LED OFF</button>
</div>   

</form>
</html>
""" 
#Setup PINS
LED2 = machine.Pin(2, machine.Pin.OUT)
adc=machine.ADC(0)


#
# Conectar el ESP8266 a la Wifi
#
yourWifiSSID = "TU_RED"
yourWifiPassword = "TU_PASSW"
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect(yourWifiSSID, yourWifiPassword)
while not sta_if.isconnected():
  pass

print("Connected to wifi")
ADCVAL=adc.read()
valor="%4d" %ADCVAL

#Setup Socket WebServer
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)
while True:
    conn, addr = s.accept()
    print("Got a connection from %s" % str(addr))
    request = conn.recv(1024)
    print(request)
    request = str(request)
    ADCREAD = request.find('/?ADC=READ')
    LEDON2 = request.find('/?LED=ON2')
    LEDOFF2 = request.find('/?LED=OFF2')
    if ADCREAD ==6:
        print('Leer el ADC')
        ADCVAL=adc.read()
        valor="%4d" %ADCVAL  
    if LEDON2 ==6:
        print('TURN LED2 ON')
        LED2.low()
    if LEDOFF2 ==6:
        print('TURN LED2 OFF')
        LED2.high()
        
    response = html1 %ADCVAL
    conn.send(response)
    conn.close()
