import Adafruit_DHT
import urllib2
import serial
# publish :  sends data given website url
def publish(temp,hum,soilMoisture1,soilMoisture2,distance,rainGauge):
    #print state
    #url = "http://10.0.3.23:8333/sensors/display/"+str(temp)+"/"+str(hum)+"/"
    #url = "https://monicaguduru.pythonanywhere.com/sensors/display/"+str(temp)+"/"+str(hum)+"/"+str(temp)+"/"+'yes'+"/"+str(temp)+"/"+'no'+"/"+str(temp)+"/"url = "https://monicaguduru.pythonanywhere.com/sensors/display/"+str(temp)+"/"+str(hum)+"/"+str(temp)+"/"+'yes'+"/"+str(temp)+"/"+'no'+"/"+str(temp)+"/"
    url = "https://djvams.pythonanywhere.com/sensors/display/"+str(temp)+"/"+str(hum)+"/"+str(soilMoisture1)+"/"+str(soilMoisture2)+"/"+str(distance)+"/"+str(rainGauge)+"/"
    #url = "https://127.0.0.1:8000/music/display/"+ str(temp) +"/"+ "5" +"/"
    #url =  "https://transportation.pythonanywhere.com/BTP/default/fun/AP123/50/70/5/"+str(temp)+"/"
    print(url)
    result = urllib2.urlopen(url).read()

t=0
ser = serial.Serial('/dev/ttyACM0',9600)  
s=[0,1]
# previous values are stored
previousHumidity=0
previousTemperature=0
previousSoilMoisture1=0
previousSoilMoisture2=0
previousRainGauge=0
previousDistance=0
#main while loop
while (True):
    t+=1
    # humidity and temperature : values taken from raspberry pi
    humidity, temperature = Adafruit_DHT.read_retry(11, 27)  # GPIO27 (BCM notation)
    # soil moisture sensor readings and rain sensor taken from arduino
    read_serial=ser.readline()

    s[0] = str(ser.readline())
    #print s[0]
    #print s[0]
    value=s[0].split(" ")
    print value
    #converting the values to respective datatype
    distance=int(value[0])+0.0
    soilMoisture1=int(value[2])+0.0
    soilMoisture2=int(value[6])+0.0
    rainGauge=value[10].strip("\r\n")
    rainGauge=float(rainGauge)+0.0
    #print distance,state
    #print sm
#print read_serial
    
    #print ("Humidity = {} %; Temperature = {} C ; Moisture = {}".format(humidity, temperature, sm))
    # sends data only if previous values donot match with current readings
    if(previousHumidity!=humidity or previousTemperature!=temperature or previousDistance!=distance or previousSoilMoisture1!=soilMoisture1 or previousSoilMoisture2!=soilMoisture2 or previousRainGauge!=rainGauge):
        print ("Humidity = {} %; Temperature = {} C ; Moisture1 = {}; Moisture2 = {}; distanceance ={} ; Rain={}".format(humidity, temperature, soilMoisture1,soilMoisture2,distance,rainGauge))
        publish(temperature,humidity,soilMoisture1,soilMoisture2,distance,rainGauge)
    
    #publish(temperature,humidity)
    previousHumidity=humidity
    previousTemperature=temperature
    previousDistance=distance
    previousSoilMoisture1=soilMoisture1
    previousSoilMoisture2=soilMoisture2
    previousRainGauge=rainGauge
