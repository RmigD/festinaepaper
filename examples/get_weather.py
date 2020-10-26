#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import datetime
import json
import logging
import requests

picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')

if os.path.exists(libdir):
    sys.path.append(libdir)

from waveshare_epd import epd2in13bc
import time
from PIL import Image,ImageDraw,ImageFont


y = json.load(open('/home/pi/epaper/Weather/examples/apids.json'))
#datapihole = json.load(open('/home/pi/epaper/Weather/examples/pihole.json'))

font30 = ImageFont.truetype(os.path.join(picdir, 'Calibri.ttf'), 30)
font20 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 20)
font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
font16 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 16)
font12 = ImageFont.truetype(os.path.join(picdir, 'Calibri.ttf'), 12)
font13 = ImageFont.truetype(os.path.join(picdir, 'Calibri.ttf'), 13)
fontTiny = ImageFont.truetype(os.path.join(picdir, 'Calibri.ttf'), 9)
fontweather = ImageFont.truetype(os.path.join(picdir, 'weathericons-regular-webfont.ttf'), 58)
fontweathersmall = ImageFont.truetype(os.path.join(picdir, 'weathericons-regular-webfont.ttf'), 24)
fontweathersmaller = ImageFont.truetype(os.path.join(picdir, 'weathericons-regular-webfont.ttf'), 20)
fontweathertiny = ImageFont.truetype(os.path.join(picdir, 'weathericons-regular-webfont.ttf'), 15)

PUSHBULLET_API_KEY=""

PIHOLE_PERCBLOCK=datapihole["ads_percentage_today"]
PIHOLE_ADSBLOCKED=datapihole["ads_blocked_today"]

CUR_ICON=y["currently"]["icon"]
CUR_SUMMARY="> "+y["currently"]["summary"]
FC_TOMORROW=y["daily"]["summary"]
CUR_TEMP=str(round((y["currently"]["temperature"]),1))+"°C"
NEXT_TEMP=str(round((y["hourly"]["data"][1]["temperature"]),1))+"°C"
CUR_WIND_DIR=y["currently"]["windBearing"]
CUR_WIND_GUST=y["currently"]["windGust"]*3.6 #convert from m/s to km/h
CUR_WIND_SPEED=y["currently"]["windSpeed"]*3.6 #convert from m/s to km/h
print (CUR_TEMP)
print (NEXT_TEMP)
print (FC_TOMORROW)
print ("Gust: ", CUR_WIND_GUST)
print ("Wind Speed: ", CUR_WIND_SPEED)
strong_Wind=18 # km/h

#tells me the weather via the speaker of my Pi3 with the Google AIY HAT (authentication is set up via SSH keys):
#convert spaces into underscores, otherwise "espeak dude" will only say the first word (due to my inability to properly escape quote marks).
ESPEAK_TEST=FC_TOMORROW.replace(" ","_")
os.system('ssh -t pi@192.168.1.41 "espeak "' + "\"" + ESPEAK_TEST + "\"") # If by any chance the forecast is ever "; rm -rf", boy am I screwed!

#

moonPhase=y["daily"]["data"][0]["moonPhase"]
moonConstant=10000
moonPhase=int(moonPhase*moonConstant)

TEMP3_ICON=y["hourly"]["data"][3]["icon"]
TEMP3_SUM=y["hourly"]["data"][3]["summary"]
TEMP3=str(round((y["hourly"]["data"][3]["temperature"]),1))+"°"

TEMP6_ICON=y["hourly"]["data"][6]["icon"]
TEMP6_SUM=y["hourly"]["data"][6]["summary"]
TEMP6=str(round((y["hourly"]["data"][6]["temperature"]),1))+"°"
WIND_GUSTS6=y["hourly"]["data"][6]["windGust"]

TEMP9_ICON=y["hourly"]["data"][9]["icon"]
TEMP9_SUM=y["hourly"]["data"][9]["summary"]
TEMP9=str(round((y["hourly"]["data"][9]["temperature"]),1))+"°"

epochNow=y["currently"]["time"]
HOUR_NOW=datetime.datetime.fromtimestamp(epochNow+3600).strftime('%H')
MINUTE_NOW=datetime.datetime.fromtimestamp(epochNow+3600).strftime('%M')

epoch3=y["hourly"]["data"][3]["time"]
TIME3=datetime.datetime.fromtimestamp(epoch3+3600).strftime('%H%M')

epoch6=y["hourly"]["data"][6]["time"]
TIME6= datetime.datetime.fromtimestamp(epoch6+3600).strftime('%H%M')

epoch9=y["hourly"]["data"][9]["time"]
TIME9= datetime.datetime.fromtimestamp(epoch9+3600).strftime('%H%M')

moonFraction=int(1/28*moonConstant)
moonFractionRng=int(1/56*moonConstant)

# 

def temp_evolution(x,y):
	if x<y:
		return ("↑")
	elif x>y:
		return ("↓")
	else:
		return ("↔")

def measure_temp():
    temp = os.popen("cat /sys/class/thermal/thermal_zone0/temp").readline()
    return (round(int(temp),0)/1000)

temp=str(measure_temp())

def toDateTime(i):
    datetime.datetime.fromtimestamp(i+3600).strftime('%H:%M')

def windStrength(i):
    if i > strong_Wind:
	    return("")

def windDir(i):
    if i in range(23,69):
        return("")
    elif i in range(69,115):
        return("")
    elif i in range(115,161):
        return("")
    elif i in range(161,207):
        return("")
    elif i in range(207,253):
        return("")
    elif i in range(253,299):
        return("")
    elif i in range(299,345):
        return("")
    elif i in range(345,360) or i in range(0,23):
        return("")
    else:
        return("?")

def iconTime(i):
    if i in ("00","12"):
        return("")
    elif i in ("01","13"):
        return("")
    elif i in ("02","14"):
        return("")
    elif i in ("03","15"):
        return("")
    elif i in ("04","16"):
        return("")
    elif i in ("05","17"):
        return("")
    elif i in ("06","18"):
        return("")
    elif i in ("07","19"):
        return("")
    elif i in ("08","20"):
        return("")
    elif i in ("09","21"):
        return("")
    elif i in ("10","22"):
        return("")
    elif i in ("11","23"):
        return("")
 
def is_half_hour(x):
    if int(x) in range (20,40):
        return("|")
    else:
        return("")
 
def icon(i):
    if i in ("cloudy"):
        return("")
    elif i == "partly-cloudy-night":
        return ("")
    elif i == "clear-day":
        return ("")
    elif i == "partly-cloudy-day":
        return ("")
    elif i == "rain":
        return ("")
    elif i == "wind":
        return ("")
    elif i == "sunny":
        return ("")
    elif i == "drizzle":
        return ("")
    elif i == "clear-night":
        return ("")
    else:
        return(i)

def split_string(x,y): #(string, half)
    max_len=16
    if (len(x) > max_len):
        i=0
        elements=(x.split(' '))
        first_part=elements[0]
        print (first_part)
        print (len(elements))
        print (elements)
        while i < len(elements) and len(first_part) < max_len:
                i=i+1
                first_part=first_part + ' ' + elements[i]
                second_part=x.split(first_part)
                second_part=second_part[1]
        if (y==1):
                #print(first_part)
                return(first_part)
        else:
                #print(second_part)
                return(second_part)
    else:
        if (y==1):
                return(x)
        else:
                return("")

def iconMoon(x):
    if  x in range((moonFraction*14)-moonFractionRng,(moonFraction*14)+moonFractionRng):
       return("")
    elif x in range((moonFraction*15)-moonFractionRng,(moonFraction*15)+moonFractionRng):
       return("")
    elif x in range((moonFraction*16)-moonFractionRng,(moonFraction*16)+moonFractionRng):
       return("")
    elif x in range((moonFraction*17)-moonFractionRng,(moonFraction*17)+moonFractionRng):
       return("")
    elif x in range((moonFraction*18)-moonFractionRng,(moonFraction*18)+moonFractionRng):
       return("")
    elif x in range((moonFraction*19)-moonFractionRng,(moonFraction*19)+moonFractionRng):
       return("")
    elif x in range((moonFraction*20)-moonFractionRng,(moonFraction*20)+moonFractionRng):
       return("")
    elif x in range((moonFraction*21)-moonFractionRng,(moonFraction*21)+moonFractionRng):
       return("")
    elif x in range((moonFraction*22)-moonFractionRng,(moonFraction*22)+moonFractionRng):
       return("")
    elif x in range((moonFraction*23)-moonFractionRng,(moonFraction*23)+moonFractionRng):
       return("")
    elif x in range((moonFraction*24)-moonFractionRng,(moonFraction*24)+moonFractionRng):
       return("")
    elif x in range((moonFraction*25)-moonFractionRng,(moonFraction*25)+moonFractionRng):
       return("")
    elif x in range((moonFraction*26)-moonFractionRng,(moonFraction*26)+moonFractionRng):
       return("")
    elif x in range((moonFraction*27)-moonFractionRng,(moonFraction*27)+moonFractionRng):
       return("")
    elif ((x > (moonConstant-moonFractionRng)) or (x < moonFractionRng)):
       return("")
    elif x in range((moonFraction*1)-moonFractionRng,(moonFraction*1)+moonFractionRng):
       return("")
    elif x in range((moonFraction*2)-moonFractionRng,(moonFraction*2)+moonFractionRng):
       return("")
    elif x in range((moonFraction*3)-moonFractionRng,(moonFraction*3)+moonFractionRng):
       return("")
    elif x in range((moonFraction*4)-moonFractionRng,(moonFraction*4)+moonFractionRng):
       return("")
    elif x in range((moonFraction*5)-moonFractionRng,(moonFraction*5)+moonFractionRng):
       return("")
    elif x in range((moonFraction*6)-moonFractionRng,(moonFraction*6)+moonFractionRng):
       return("")
    elif x in range((moonFraction*7)-moonFractionRng,(moonFraction*7)+moonFractionRng):
       return("")
    elif x in range((moonFraction*8)-moonFractionRng,(moonFraction*8)+moonFractionRng):
       return("")
    elif x in range((moonFraction*9)-moonFractionRng,(moonFraction*9)+moonFractionRng):
       return("")
    elif x in range((moonFraction*10)-moonFractionRng,(moonFraction*10)+moonFractionRng):
       return("")
    elif x in range((moonFraction*11)-moonFractionRng,(moonFraction*11)+moonFractionRng):
       return("")
    elif x in range((moonFraction*12)-moonFractionRng,(moonFraction*12)+moonFractionRng):
       return("")
    elif x in range((moonFraction*13)-moonFractionRng,(moonFraction*13)+moonFractionRng):
       return("") 
    else:
        return("N/A")

logging.basicConfig(level=logging.DEBUG)

FULL_TEMP=CUR_TEMP + temp_evolution(CUR_TEMP,NEXT_TEMP)
print (FULL_TEMP)

try:
    logging.info("Festina Weather")
    
    epd = epd2in13bc.EPD()
    logging.info("init and Clear")
    epd.init()
    epd.Clear()
    time.sleep(1)
    
    # Drawing on the image
    logging.info("Drawing")    

    # Drawing on the Vertical image
    logging.info("1.Drawing on the Vertical image...") 
    HBlackimage = Image.new('1', (epd.width, epd.height), 255)  # 298*126
    HRYimage = Image.new('1', (epd.width, epd.height), 255)  # 298*126  ryimage: red image  
    drawblack = ImageDraw.Draw(HBlackimage)
    drawry = ImageDraw.Draw(HRYimage)
    
    #Updated at
    drawblack.text((6,0), iconTime(HOUR_NOW), font = fontweathersmaller, fill = 0)
    #Big icon
    drawry.text((28, 0), icon(CUR_ICON), font = fontweather, fill = 0)
    #Current wind direction
    if CUR_WIND_SPEED>strong_Wind:
        drawry.text((4,30), "", font = fontweathertiny, fill = 0) 
    else:
	    drawblack.text((5,27), windDir(CUR_WIND_DIR), font = fontweathersmaller, fill = 0)
    
    #Moon phase
    drawblack.text((6,54), iconMoon(moonPhase), font = fontweathersmaller, fill = 0)
    #Current temperature
    drawblack.text((4, 81), FULL_TEMP, font = font30, fill = 0)
    #Summary of current conditions
    drawblack.text((2, 110), CUR_SUMMARY, font = font13, fill = 0)
    
    
    #Icon for conditions in 3 hours
    drawry.text((4, 124), icon(TEMP3_ICON), font = fontweathersmall, fill = 0)
    #Temperature in 3 hours
    drawblack.text((3, 158), TEMP3, font = font13, fill = 0)
    #Time in 3 hours
    drawblack.text((3, 172), TIME3, font = font13, fill = 0)
    
    #Icon for conditions in 6 hours
    drawry.text((39, 124), icon(TEMP6_ICON), font = fontweathersmall, fill = 0)
    #Temperature in 6 hours
    drawblack.text((39, 158), TEMP6, font = font13, fill = 0)
    #time in 6 hours
    drawblack.text((39, 172), TIME6, font = font13, fill = 0)
    
    #Icon for conditions in 9 hours
    drawry.text((74, 124), icon(TEMP9_ICON), font = fontweathersmall, fill = 0)
    #Temperature in 9 hours
    drawblack.text((74, 158), TEMP9, font = font13, fill = 0)
    #time in 9 hours
    drawblack.text((74, 172), TIME9, font = font13, fill = 0)
    
    #Forecast tomorrow #186
    print(FC_TOMORROW)
    FC_TOMORROW1=split_string(FC_TOMORROW,1)
    FC_TOMORROW2=split_string(FC_TOMORROW,2)
    drawblack.text((1,190), FC_TOMORROW1, font = font12, fill = 0)
    drawblack.text((1,200), FC_TOMORROW2, font = font12, fill = 0)

    #Status pihole
    #statsBottom= "a:" + str(PIHOLE_ADSBLOCKED) + "(" + str(int(PIHOLE_PERCBLOCK)) + "%);t:" + str(temp) + "°"
    # drawblack.text((1,199), statsBottom, font = font12 , fill = 0)
    # print(statsBottom)
    
    def send_notification_via_pushbullet(title, body):

        data_send = {"type": "note", "title": title, "body": body}
    
        ACCESS_TOKEN = PUSHBULLET_API_KEY
        resp = requests.post('https://api.pushbullet.com/v2/pushes', data=json.dumps(data_send),
                            headers={'Authorization': 'Bearer ' + ACCESS_TOKEN, 'Content-Type': 'application/json'})
        if resp.status_code != 200:
            raise Exception('Something wrong')
        else:
            print ('complete sending')
    
    #Notify wind in 6 hours
    if WIND_GUSTS6 > strong_Wind:
        data = {
            'type': 'note',
            'title': 'Wind alert',
            'body': 'Strong wind gusts in 6 hours'
        }

        response = requests.post('https://api.pushbullet.com/v2/pushes', data=data, auth=(PUSHBULLET_API_KEY, ''))


    epd.display(epd.getbuffer(HBlackimage), epd.getbuffer(HRYimage))
    time.sleep(2)
   
    logging.info("Goto Sleep...")
    epd.sleep()
    
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd2in13bc.epdconfig.module_exit()
    exit()
