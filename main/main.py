#### İmport libraries
import time
import cv2
from detection import ripeness_detection ,disease_detection
#from rotate import rotate90, rotateback
from datetime import date
import serial #Serial Communication with Arduino Mega
import re # For string parsing
from flask import Flask, render_template, request
from datetime import datetime
app = Flask(__name__)

#### Initialize the code

ser = serial.Serial('/dev/ttyUSB0',9600,timeout=10)
ser.reset_input_buffer()
airTemp = 0
temp_felt = 0
waterTemp = 0
ppm = 0
disease_t=" "
unripe = 0
semiripe = 0
ripe = 0
total = 0
light = 0
red = 0
green = 0
blue = 0
water_cond = 0
humidity = 0
waterLevel = 0
## Check Buttons
heating = 0
cooling = 0
nutrient = 0
waterPump = 0
waterDump = 0
waterMixer = 0
auto = 1


@app.route('/',methods=['POST','GET'])
def index():
    global airTemp 
    global temp_felt 
    global waterTemp 
    global ppm 
    global disease_t
    global unripe 
    global semiripe 
    global ripe 
    global total 
    global light 
    global red
    global green
    global blue
    global water_cond
    global humidity
    global waterLevel
    global ser

    global heating 
    global cooling 
    global nutrient 
    global waterPump 
    global waterDump 
    global waterMixer 
    global auto
    global waterLevel

    if request.method == "POST":
        
        if request.form.get("cooling")!=None:
            cooling = int(request.form.get("cooling"))
            print(type(cooling))
            if(cooling==1):
                print("Cooling Fan is activated!")
                ser.write(bytes("cooling=1\n","utf-8"))
            else:
                print("Cooling Fan is deactivated!")
                ser.write(bytes("cooling=0\n","utf-8"))
        if request.form.get('heating')!=None:
            heating = int(request.form.get('heating'))
            if(heating==1):
                print("Heating Fan is activated!")
                ser.write(bytes("heating=1\n","utf-8"))
            else:
                print("Heating Fan is deactivated!")
                ser.write(bytes("heating=0\n","utf-8"))
        if request.form.get('nutrition')!=None:
            nutrient = int(request.form.get("nutrition"))
            if(nutrient==1):
                print("Nutrient Pump is activated!")
                ser.write(bytes("nutrition=1\n","utf-8"))
            else:
                print("Nutrient Pump is deactivated!")
                ser.write(bytes("nutrition=0\n","utf-8"))
        if request.form.get("waterPump")!=None:
            waterPump = int(request.form.get("waterPump"))
            if(waterPump==1):
                print("Water Pump is activated!")
                ser.write(bytes("waterPump=1\n","utf-8"))
            else:
                print("Water Pump is deactivated!")
                ser.write(bytes("waterPump=0\n","utf-8"))
        if request.form.get("waterDump")!=None:
            waterDump = int(request.form.get("waterDump"))
            if(waterDump==1):
                print("Water Dump is activated!")
                ser.write(bytes("waterDump=1\n","utf-8"))
            else:
                print("Water Dump is deactivated!")
                ser.write(bytes("waterDump=0\n","utf-8"))
        if request.form.get("waterMixer")!=None:
            waterMixer = int(request.form.get("waterMixer"))
            if(waterMixer==1):
                print("Water Mixer is activated!")
                ser.write(bytes("waterMixer=1\n","utf-8"))
            else:
                print("Water Mixer is deactivated!")
                ser.write(bytes("waterMixer=0\n","utf-8"))
        if request.form.get("auto")!=None:
            auto = int(request.form.get("auto"))
            if(auto==1):
                print("Autonomous mode is enabled!")
                ser.write(bytes("auto=1\n","utf-8"))
            else:
                print("Autonomous mode is disabled!")
                ser.write(bytes("auto=0\n","utf-8"))
        
            
        with open("logFile.txt", "a") as myfile:
            myfile.write(f"Time:{datetime.now().strftime('%Y-%m-%d, %H:%M:%S')}\n")
        with open("logFile.txt", "a") as myfile:    
            myfile.write(f"Air Temperature: {airTemp}, Apparent Temperature: {temp_felt}, Water Temperature: {waterTemp}\n")
        with open("logFile.txt", "a") as myfile: 
            myfile.write(f"Light Intensity:{light}lux, PPM:{ppm}, Red:{red}-Green:{green}-Blue:{blue}\n")
        with open("logFile.txt", "a") as myfile: 
            myfile.write(f"ripe:{ripe},semiripe:{semiripe},unripe:{unripe},total:{total}\n")
        with open("logFile.txt", "a") as myfile: 
            myfile.write(f"Water Conductivity:{water_cond}, Humidity:{humidity}, auto:{auto}\n{'-'*10}\n\n")
                            

        return render_template('index.html',
                                    currentTime=datetime.now().strftime("%Y-%m-%d, %H:%M:%S"),
                                    airTemp = airTemp,
                                    temp_felt = temp_felt,
                                    waterTemp = waterTemp,
                                    ppm = ppm,
                                    light=light,
                                    red=red,
                                    green = green,
                                    blue = blue,
                                    water_cond = water_cond,
                                    waterLevel = waterLevel,
                                    humidity = humidity,
                                    semiripe=semiripe,
                                    ripe=ripe,
                                    unripe=unripe,
                                    total=total,
                                    disease=disease_t,
                                    ex_heating=heating,
                                    ex_cooling=cooling,
                                    ex_waterPump=waterPump,
                                    ex_waterDump=waterDump,
                                    ex_auto=auto,
                                    ex_waterMixer=waterMixer,
                                    ex_nutrition=nutrient)
    else:
        while ser.in_waiting > 0:
            message_from_arduino = ser.readline().decode('utf-8').rstrip()
            print("arduinodan gelen data",message_from_arduino)
            message_from_arduino = re.split(";|=",message_from_arduino)
            print(f"gelen data boyutu: {len(message_from_arduino)}")
            for i in range(len(message_from_arduino)):
                if (message_from_arduino[i]=="red"):
                    red = message_from_arduino[i+1]
                if (message_from_arduino[i]=="green"):
                    green = message_from_arduino[i+1]
                if (message_from_arduino[i]=="blue"):
                    blue = message_from_arduino[i+1]
                if (message_from_arduino[i]=="lux"):
                    light = message_from_arduino[i+1]
                if (message_from_arduino[i]=="airTemp"):
                    airTemp = message_from_arduino[i+1]
                if (message_from_arduino[i]=="waterLevel"):
                    waterLevel = message_from_arduino[i+1]
                if (message_from_arduino[i]=="humidity"):
                    humidity = message_from_arduino[i+1]
                if (message_from_arduino[i]=="temp_felt"):
                    temp_felt = message_from_arduino[i+1]
                if (message_from_arduino[i]=="ppm"):
                    ppm = message_from_arduino[i+1]
                if (message_from_arduino[i]=="waterTemp"):
                    waterTemp = message_from_arduino[i+1]
                if (message_from_arduino[i]=="water_cond"):
                    water_cond = message_from_arduino[i+1]
              
    
        return render_template('index.html',
                                  currentTime=datetime.now().strftime("%Y-%m-%d, %H:%M:%S"),
                                  airTemp = airTemp,
                                  temp_felt = temp_felt,
                                  waterTemp = waterTemp,
                                  waterLevel = waterLevel,
                                  ppm = ppm,
                                  light=light,
                                  red=red,
                                  green = green,
                                  blue = blue,
                                  water_cond = water_cond,
                                  humidity = humidity,
                                  semiripe=semiripe,
                                  ripe=ripe,
                                  unripe=unripe,
                                  total=total,
                                  disease=disease_t,
                                  ex_heating=heating,
                                    ex_cooling=cooling,
                                    ex_waterPump=waterPump,
                                    ex_waterDump=waterDump,
                                    ex_auto=auto,
                                    ex_waterMixer=waterMixer,
                                    ex_nutrition=nutrient)

@app.route('/takenimages',methods=['POST','GET'])
def takenimages():
    global airTemp 
    global temp_felt 
    global waterTemp 
    global ppm 
    global disease_t
    global unripe 
    global semiripe 
    global ripe 
    global total 
    global light 
    global red
    global green
    global blue
    global water_cond
    global humidity
    global waterLevel
    global ser

    global heating 
    global cooling 
    global nutrient 
    global waterPump 
    global waterDump 
    global waterMixer
    global auto

    if request.method == "POST":
        if request.form.get("newPhoto")!=None:
            ser.write(bytes("cameraMode=1\n","utf-8"))
            time.sleep(3) #wait arduino to make RGB LED white
            date_t = datetime.now().strftime("%Y-%m-%d")
            #capture first image
            cam = cv2.VideoCapture(0) # get frame
            ret, image = cam.read()       # read frame
            cam.release() #release the camera
            print(type(image))
            cv2.imwrite(filename=f"static/images/{date_t}_1.jpg", img=image)  # save image into static folder

            
            time.sleep(8)
            #capture second image
            cam = cv2.VideoCapture(0) # get frame
            ret, image = cam.read()       # read frame
            cam.release() #release the camera
            print(type(image))
            cv2.imwrite(filename=f"static/images/{date_t}_2.jpg", img=image)  # save image into static folder

            
            time.sleep(8)
            #capture third image
            cam = cv2.VideoCapture(0) # get frame
            ret, image = cam.read()       # read frame
            cam.release() #release the camera
            print(type(image))
            cv2.imwrite(filename=f"static/images/{date_t}_3.jpg", img=image)  # save image into static folder
            
            
            time.sleep(8)
            #capture the fourth image 
            cam = cv2.VideoCapture(0) # get frame
            ret, image = cam.read()       # read frame
            cam.release() #release the camera
            print(type(image))
            cv2.imwrite(filename=f"static/images/{date_t}_4.jpg", img=image)  # save image into static folder

            cam.release() #release the camera
            ser.write(bytes("cameraMode=0\n","utf-8"))

        elif request.form.get("startRipeness")!=None:
            #start detecting the ripeness level  
            date_t = datetime.now().strftime("%Y_%m_%d")
            ripe,semiripe,unripe=ripeness_detection()
            # ripeness detection code (input is time so that detect correct photos)
            print(f"Ripe : {ripe}")
            print(f"SemiRipe : {semiripe}")
            print(f"UnRipe : {unripe}")
            """if(ripeness["Ripe"]>(ripeness["Semi_ripe"]+ripeness["Unripe"])):
                ## call arduino to get 1300 ppm
                print("You should have 1300 ppm")
                else:
                ## call arduino to get 1600 ppm
                print("You should have 1600 ppm")"""
            if(semiripe or ripe or unripe):
                ser.write(bytes("fruitMode=1\n","utf-8"))
            else:
                ser.write(bytes("fruitMode=0\n","utf-8"))
        
        elif request.form.get("startDisease")!=None:
            date_t = datetime.now().strftime("%Y_%m_%d")
            disease = disease_detection()   # disease detection code (input is time so that detect correct photos)

            insect = disease["Insect"]
            anthracnose = disease["Anthracnose"]
            gray_mold = disease["Gray_Mold"]
            leaf_spot = disease["Leaf_Spot"]
            
            if (insect or anthracnose or gray_mold or leaf_spot):
                ser.write(bytes("disease=1\n","utf-8"))
                if(insect):
                    disease_t +="-Insect"
                if(anthracnose):
                    disease_t +="-Anthracnose"
                if(gray_mold):
                    disease_t +="-Gray Mold"
                if(leaf_spot):
                    disease_t +="-Leaf Spot"
            else:
                disease_t = "No Disease or Insect Detected"
                ser.write(bytes("disease=0\n","utf-8"))
            print(disease_t) 
        return render_template('takenimages.html',
                                unripe=unripe,
                                semiripe=semiripe,
                                ripe=ripe,
                                disease=disease_t,
                                total=total)
    else:
        return render_template('takenimages.html',
                                unripe=unripe,
                                semiripe=semiripe,
                                ripe=ripe,
                                disease=disease_t,
                                total=total)


@app.route('/manualcontrol',methods=['POST','GET'])
def manualcontrol():
    global ripe
    global semiripe
    global unripe
    global total
    global disease_t
    global ser

    if request.method == "POST":
        ripe = int(request.form['ripe'])
        print(f"Given Ripe:{ripe}")
        semiripe = int(request.form['semiripe'])
        print(f"Given Semiripe:{semiripe}")
        unripe = int(request.form["unripe"])
        print(f"Given Unripe:{unripe}")
        total = ripe+semiripe+unripe
        disease_t = request.form['disease']

        if(unripe or semiripe or ripe):
            ser.write(bytes("fruitMode=1\n","utf-8"))
        else:
            ser.write(bytes("fruitMode=0\n","utf-8"))
        
        if(disease_t=="No Disease"):
            ser.write(bytes("disease=0\n","utf-8"))
        else:
            ser.write(bytes("disease=1\n","utf-8"))



        return render_template('manualcontrol.html',
                                unripe=unripe,
                                semiripe=semiripe,
                                ripe=ripe,
                                disease=disease_t,
                                total=total)


    else:
        return render_template('manualcontrol.html',
                                unripe=unripe,
                                semiripe=semiripe,
                                ripe=ripe,
                                disease=disease_t,
                                total=total)





if __name__=='__main__':
    app.run(debug=False,host='0.0.0.0',port=15080)
    
