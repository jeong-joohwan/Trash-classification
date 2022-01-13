from tensorflow.keras.models import load_model
from multiprocessing import Process, Queue
from threading import Thread
from PIL import Image, ImageOps

import socket
import time
import cv2
import numpy as np
import time, datetime
import sys
import os
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
predict_trash = ''
check1 = 0

class NetClient():
    def __init__( self, hostIP, hostPort ):
        self.host = hostIP
        self.port = hostPort
        self.client_sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        self.server_address = ( self.host, self.port )
        self.client_sock.connect((self.host, self.port) )

    def __del__( self ):
        self.client_sock.close()
        print( "Closing connection to the server" )

    def sendstringData(self, stringData ):
        try:
            self.client_sock.send(str(len(stringData)).ljust(28).encode())
            self.client_sock.send(stringData)

        except socket.errno as e:
            print( "Socket error: %s" %str(e) )
        except ConnectionResetError as e:
            print( "ConnectionResetError: %s" %str(e) )
        except Exception as e:
            print( "Other exception: %s" %str(e) )

    def sendData( self, data ):
        try:
            print("Sending --> {0}".format( data ))
            self.client_sock.send( data.encode() )

        except socket.errno as e:
            print( "Socket error: %s" %str(e) )
        except Exception as e:
            print( "Other exception: %s" %str(e) )
        
    def receiveData( self ):
        return self.client_sock.recv(1024)


class Conveyor1(Thread):
    def __init__(self):
        Thread.__init__(self, name='Conveyor1')
        self.con1_port = 17 #11
        GPIO.setup(self.con1_port, GPIO.OUT)

    def __del__( self ):
        print( "Closing Conveyor1" )

    def conveyor_init(self):
        GPIO.output(self.con1_port, True)

    def con1_On(self):
        GPIO.output(self.con1_port, False)

    def con1_Off(self):
        GPIO.output(self.con1_port, True)

class Robot1(Thread):
    def __init__(self):
        Thread.__init__(self, name='Robot1')
        self.port1 = 20 #38
        self.port2 = 21 #40
        self.port3 = 23 #16
        GPIO.setup(self.port1, GPIO.OUT)
        GPIO.setup(self.port2, GPIO.OUT)
        GPIO.setup(self.port3, GPIO.OUT)

        
    def Rb1_right(self):
        p1=GPIO.PWM(self.port1, 100)
        p2=GPIO.PWM(self.port2, 100)
        p3=GPIO.PWM(self.port3, 50)
        p1.start(0)
        p2.start(0)
        p3.start(0)
        p3.ChangeDutyCycle(5) # 집게 열고
        time.sleep(0.8)
        p1.ChangeDutyCycle(20) #밑으로 내리고
        time.sleep(0.8)
        p3.ChangeDutyCycle(10) #집게 닫고
        time.sleep(0.8)
        p1.ChangeDutyCycle(10) #다시 올리고
        time.sleep(0.8)
        p2.ChangeDutyCycle(3) #옆으로 돌리고
        time.sleep(0.8)
        p1.ChangeDutyCycle(20) #밑으로 내리고
        time.sleep(0.8)
        p3.ChangeDutyCycle(5) # 집게 열고
        time.sleep(0.8)
        p1.ChangeDutyCycle(10) #다시 올라오고
        time.sleep(0.8)
        p2.ChangeDutyCycle(13) #원위치로 돌아가고
        time.sleep(0.8)
        p3.ChangeDutyCycle(10) #집게 닫고
        time.sleep(0.8)

    def Rb1_left(self):

        p1=GPIO.PWM(self.port1, 100)
        p2=GPIO.PWM(self.port2, 100)
        p3=GPIO.PWM(self.port3, 50)
        p1.start(0)
        p2.start(0)
        p3.start(0)
        p3.ChangeDutyCycle(5) # 집게 열고
        time.sleep(0.8)
        p1.ChangeDutyCycle(20) #밑으로 내리고
        time.sleep(0.8)
        p3.ChangeDutyCycle(10) #집게 닫고
        time.sleep(0.8)
        p1.ChangeDutyCycle(10) #다시 올리고
        time.sleep(0.8)
        p2.ChangeDutyCycle(23) #왼족으로로 돌리고
        time.sleep(0.8)
        p1.ChangeDutyCycle(20) #밑으로 내리고
        time.sleep(0.8)
        p3.ChangeDutyCycle(5) # 집게 열고
        time.sleep(0.8)
        p1.ChangeDutyCycle(10) #다시 올라오고
        time.sleep(0.8)
        p2.ChangeDutyCycle(13) #원위치로 
        time.sleep(0.8)
        p3.ChangeDutyCycle(10) #집게 닫고
        time.sleep(0.8)   

    def Rb1_back(self):

        p1=GPIO.PWM(self.port1, 100)
        p2=GPIO.PWM(self.port2, 100)
        p3=GPIO.PWM(self.port3, 50)
        p1.start(0)
        p2.start(0)
        p3.start(0)
        p3.ChangeDutyCycle(5) # 집게 열고
        time.sleep(0.8)
        p1.ChangeDutyCycle(20) #밑으로 내리고
        time.sleep(0.8)
        p3.ChangeDutyCycle(10) #집게 닫고
        time.sleep(0.8)
        p1.ChangeDutyCycle(3) #다시 올리고
        time.sleep(0.8)
        p3.ChangeDutyCycle(5) # 집게 열고
        time.sleep(0.8)
        p1.ChangeDutyCycle(10) #다시 올라오고
        time.sleep(0.8)
        p3.ChangeDutyCycle(10) #집게 닫고
        time.sleep(0.8) 



class Robot2(Thread):
    def __init__(self):
        Thread.__init__(self, name='Robot2')
        self.port4 = 5 #29
        self.port5 = 6 #31
        self.port6 = 13 #33
        GPIO.setup(self.port4, GPIO.OUT)
        GPIO.setup(self.port5, GPIO.OUT)
        GPIO.setup(self.port6, GPIO.OUT)


    def Rb2_right(self):

        p4=GPIO.PWM(self.port4, 100)
        p5=GPIO.PWM(self.port5, 50)
        p6=GPIO.PWM(self.port6, 50)
        p4.start(0)
        p5.start(0)
        p6.start(0)
        p6.ChangeDutyCycle(2) # 집게 열고
        time.sleep(1)
        p4.ChangeDutyCycle(25) #밑으로 내리고
        time.sleep(1)
        p6.ChangeDutyCycle(10) #집게 닫고
        time.sleep(1)
        p4.ChangeDutyCycle(15) #다시 올리고
        time.sleep(1)
        p5.ChangeDutyCycle(3) #옆으로 돌리고
        time.sleep(1)
        p4.ChangeDutyCycle(25) #밑으로 내리고
        time.sleep(1)
        p6.ChangeDutyCycle(2) # 집게 열고
        time.sleep(1)
        p4.ChangeDutyCycle(15) #다시 올라오고
        time.sleep(1)
        p5.ChangeDutyCycle(8) #원위치로 돌아가고
        time.sleep(1)
        p6.ChangeDutyCycle(10) #집게 닫고
        time.sleep(1)

    def Rb2_left(self):

        p4=GPIO.PWM(self.port4, 100)
        p5=GPIO.PWM(self.port5, 50)
        p6=GPIO.PWM(self.port6, 50)
        p4.start(0)
        p5.start(0)
        p6.start(0)
        p6.ChangeDutyCycle(2) # 집게 열고
        time.sleep(1)
        p4.ChangeDutyCycle(25) #밑으로 내리고
        time.sleep(1)
        p6.ChangeDutyCycle(10) #집게 닫고
        time.sleep(1)
        p4.ChangeDutyCycle(15) #다시 올리고
        time.sleep(1)
        p5.ChangeDutyCycle(12.5) #옆으로 돌리고
        time.sleep(1)
        p4.ChangeDutyCycle(25) #밑으로 내리고
        time.sleep(1)
        p6.ChangeDutyCycle(2) # 집게 열고
        time.sleep(1)
        p4.ChangeDutyCycle(15) #다시 올라오고
        time.sleep(1)
        p5.ChangeDutyCycle(8) #원위치로 돌아가고
        time.sleep(1)
        p6.ChangeDutyCycle(10) #집게 닫고
        time.sleep(1)

    def Rb2_back(self):

        p4=GPIO.PWM(self.port4, 100)
        p5=GPIO.PWM(self.port5, 50)
        p6=GPIO.PWM(self.port6, 50)
        p4.start(0)
        p5.start(0)
        p6.start(0)
        p6.ChangeDutyCycle(2) # 집게 열고
        time.sleep(1)
        p4.ChangeDutyCycle(25) #밑으로 내리고
        time.sleep(1)
        p6.ChangeDutyCycle(10) #집게 닫고
        time.sleep(1)
        p4.ChangeDutyCycle(5) #뒤로꺾기
        time.sleep(1)  
        p6.ChangeDutyCycle(2) # 집게 열고
        time.sleep(1)
        p4.ChangeDutyCycle(15) #다시 올라오고
        time.sleep(1)
        p6.ChangeDutyCycle(10) #집게 닫고
        time.sleep(1)

class Ultra(Thread):
    def __init__(self, M2Cque, C2Mque):
        Thread.__init__(self, name = 'Ultra')
        self.sig = 27 #13
        self.C2Mque = C2Mque
        self.M2Cque = M2Cque
        
    def __del__(self):
        print( "Closing UltraSensor1" )

    def picture(self):
        Check1 = 1
        self.M2Cque.put(Check1)
        print('active Put')
        time.sleep(2)
        Check1 = 0
        
    def run(self):
        GPIO.setup(self.sig, GPIO.OUT)
        GPIO.output(self.sig, False)
        time.sleep(0.5)

        GPIO.output(self.sig, False)
        time.sleep(0.00001)
        GPIO.output(self.sig, True)

        GPIO.setup(self.sig, GPIO.IN)
        while GPIO.input(self.sig) == False:
            self.pulse_start = time.time()
        while GPIO.input(self.sig) == True:
            self.pulse_end = time.time()

        self.pulse_duration = self.pulse_end - self.pulse_start
        self.distance = self.pulse_duration * 17000
        self.distance = round(self.distance, 2)

        print( 'Distance : {:.2f}cm'.format( self.distance ))
        return self.distance

class TurnOff(Conveyor1):
    def __init__(self):
        Conveyor1.__init__(self)

    def __del__(self):
        print('Turn Off Conveyor')

    def AllOff(self):
        self.con1_Off()
  

class MachineProcess( Process, NetClient, TurnOff):
    def __init__(self, host, port, M2Cque, C2Mque, trashque):
        self.M2Cque = M2Cque
        self.C2Mque = C2Mque
        self.trashque = trashque
        self.item_list = Queue()
        Process.__init__(self, name = 'MachineProcess')
        NetClient.__init__(self, host, port)
        TurnOff.__init__(self)

        print('[MachineProcess __init__]')

    def __del__(self):
        self.AllOff()
        GPIO.cleanup()
        print('[MachineProcess __del__]')

    def run(self):


        # make object
        conveyor1 = Conveyor1()
        robot1 = Robot1()
        robot2 = Robot2()
        ultra = Ultra(self.M2Cque, self.C2Mque)

        ultra.__init__(self.M2Cque, self.C2Mque)
        while True:
            conveyor1.con1_On()

            while True:
                if ultra.run() <= 40.00:
                    print('1')
                    conveyor1.con1_Off()

                    ultra.picture()
                    
                    break

            conveyor1.con1_On()

            while True:
                if ultra.run() <= 18.00:
                    print('2')
                    conveyor1.con1_Off()
                    now = datetime.datetime.now()
                    measuredate = now.strftime( '%Y-%m-%d %H:%M' )


                    if self.trashque.qsize() == 0:
                        continue

                    else :
                        predict_trash = self.trashque.get(timeout=100)

                        if predict_trash == 'plastic2':
                            robot2.Rb2_right()
                            self.sendData('plast2')
                            self.sendData('6')
                            self.sendData(measuredate)
                        elif predict_trash == 'plastic1':
                            robot2.Rb2_left()
                            self.sendData('plast1')
                            self.sendData('5')
                            self.sendData(measuredate)
                        elif predict_trash == 'can':
                            robot2.Rb2_back()
                            self.sendData('metal1')
                            self.sendData('1')
                            self.sendData(measuredate)
                        elif predict_trash == 'glass1':
                            robot1.Rb1_right()
                            self.sendData('glass1')
                            self.sendData('2')
                            self.sendData(measuredate)
                        elif predict_trash == 'glass2':
                            robot1.Rb1_left()
                            self.sendData('glass2')
                            self.sendData('3')
                            self.sendData(measuredate)
                        elif predict_trash == 'glass3':
                            robot1.Rb1_back()
                            self.sendData('glass3')
                            self.sendData('4')
                            self.sendData(measuredate)
                            
                        break
            
class CameraProcess( Process, NetClient):
    def __init__( self, host, port, M2Cque, C2Mque, trashque ):
        Process.__init__(self, name='CameraProcess')
        NetClient.__init__( self, host, port )
        
        self.M2Cque = M2Cque
        self.C2Mque = C2Mque
        self.trashque = trashque

        print( '[CameraProcess __init__]' )

    def __del__( self ):
        print( '[CameraProcess __del__]' )

    def sendImg2Server( self, model, img_roi ):
        # set imencode parameter. set image quality 0~100 (100 is the best quality). default is 95
        encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),100]

        # image encoding,  encode_param is composed of [1, 100]
        result, imgencode = cv2.imencode('.jpg', img_roi, encode_param)
        if result==False:
            print("Error : result={}".format(result))

        # Show image
        cv2.imshow('image', img_roi)
        
        # Convert numpy array
        roi_data = np.array(imgencode)

        # Convert String for sending Data
        stringData = roi_data.tostring()

        # Send to server

        self.predictType(model, stringData)
        

    def predictType( self, model, stringData ):

        imgdata = np.frombuffer(stringData, dtype='uint8')

        # img decode
        decimg=cv2.imdecode(imgdata,1)
        img_location = './img_file/buf.png'

        cv2.imwrite(img_location, decimg)

        """
        Create an array of the shape to supply to the Keras model
        The number of 'lengths' or images that can be placed in an array...
        ..determined by the first position of the tuple, in this case '1'
        """
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

        image = Image.open(img_location)
        size = (224, 224)
        image = ImageOps.fit(image, size, Image.ANTIALIAS)


        #turn the image into a numpy array
        image_array = np.asarray(image)

        # Normalize the image
        normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

        # Load the image into the array
        data[0] = normalized_image_array

        prediction = model.predict(data) # 카테고리당 확률 나타냄

        class_1 = prediction[0][0]
        class_2 = prediction[0][1]
        class_3 = prediction[0][2]
        class_4 = prediction[0][3]
        class_5 = prediction[0][4]
        class_6 = prediction[0][5]

        print(prediction)   
        predict_class = max(prediction[0])

       

        if class_1 == predict_class:
            print('prediction result : metal1')
            predict_type = 'can'
            classification = 'can'

        elif class_2 == predict_class:
            print('prediction result : glass1')
            predict_type = 'glass1'
            classification = 'glass1'

        elif class_3 == predict_class:
            print('prediction result : glass2')
            predict_type = 'glass2'
            classification = 'glass2'

        elif class_4 == predict_class:
            print('prediction result : glass3')
            predict_type = 'glass3'
            classification = 'glass3'

        elif class_5 == predict_class:
            print('prediction result : plast1)')
            predict_type = 'plastic1'
            classification = 'plastic1'

        elif class_6 == predict_class:
            print('prediction result : plast2')
            predict_type = 'plastic2'
            classification = 'plastic2'



        predict_trash = self.trashque.put(predict_type)

        print(predict_trash)





    def run(self):
        np.set_printoptions(suppress=True)

        cap = cv2.VideoCapture(-1) #0 카메라 사용 타입
        cap.set(cv2.CAP_PROP_FRAME_WIDTH,480)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480)

        # load model.
        model = load_model('123.hdf5')
        try:
            while True:
                ret, img_color = cap.read()
                if ret == False:
                    continue
                cv2.imshow('Camera', img_color)

                cv2.waitKey(1) 
                
                if self.M2Cque.qsize() == 0:
                    continue
                else:
                    a = self.M2Cque.get(timeout=100)
                    img_roi = cv2.resize(img_color, dsize=(224, 224))
                    print('MachineVision process progressed...')
                    ''' ### send image data to server ### '''
                    self.sendImg2Server(model, img_roi)

                    print(a)

        except KeyboardInterrupt :
            cv2.destroyAllWindows()
                
if __name__ == '__main__':
    server_ip = '192.168.0.107'
    server_port = 9000
    M2Cque = Queue()
    C2Mque = Queue()
    trashque = Queue()


    ClientProcess = MachineProcess( server_ip, server_port, M2Cque, C2Mque, trashque)
    ClientProcess.start()
    CP = CameraProcess(server_ip, server_port, M2Cque, C2Mque, trashque)
    CP.start()

    