# final_server.py

from multiprocessing import Process, Queue

import Car_Camera

import time
import socket
import pymysql
import sys

import cv2
import numpy as np
import matplotlib.pyplot as plt
import pytesseract

import datetime, time


class ServerProcess( Process ):
    def __init__(self,ip,port):
        Process.__init__( self, name = 'ServerProcess' )

        self.server_ip = ip
        self.server_port = port
        self.backlog = 5

        self.server_socket = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        self.server_socket.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
        self.server_address = ( self.server_ip, self.server_port )
        self.server_socket.bind( self.server_address )
        print( "[ Server IP : {0:15s} - {1:5d} ]".format( self.server_ip, self.server_port ) )

        self.server_socket.listen( self.backlog )
        print( '[ServerProcess __init__]' )

    def __del__( self ):
        print( '[ServerProcess __del__]' )
        self.server_socket.close()


    def run( self ):
        while True:
            try:
                client_socket, address = self.server_socket.accept()
                print( '[ Connection client IP : {0} ]'.format( address ) )
                print( 'Client connect Waiting\n')

                
                clientProcess = ClientProcess( client_socket, address )
                clientProcess.start()


            except Exception as e:
                print( e )

            except KeyboardInterrupt as e:
                print( e )
                sys.exit()


class ClientProcess( Process ):
    def __init__( self, c_sock, c_address ):
        Process.__init__( self, name='ClientProcess' )
        
        self.NAME_BUFSIZE = 6
        self.CODE_BUFSIZE = 1
        self.DATE_BUFSIZE = 16

        self.HOSTNAME = "kcoding-cert-db.cfpilismzi9r.ap-northeast-2.rds.amazonaws.com"
        self.PORT = 33306
        self.USERNAME = "prj-recycle"
        self.PASSWORD = "recycle123!@#"
        self.DATABASE = "recycle"
        self.CHARSET = "utf8"
        
        self.client_socket = c_sock
        self.client_address = c_address
        print( '[ClientProcess __init__]' )

    def __del__( self ):
        print( '[ClientProcess __del__]' )
        self.client_socket.close()


    def read_car_number(self):

        car_number = Car_Camera.CarCamera("C:\\Users\\hangaramit07\\Desktop\\final_pro\\images\\2.jpg")
        print(car_number)
        
        return car_number


    def car_insert(self, car_number):

        conn = pymysql.connect(
            host=self.HOSTNAME,
            port=self.PORT,
            user=self.USERNAME,
            password=self.PASSWORD,
            db=self.DATABASE,
            charset=self.CHARSET
        )

        sql = '''INSERT INTO trash_car(user_car_number) values (%s)'''
        curs = conn.cursor(pymysql.cursors.DictCursor)
        curs.execute(sql, car_number)
        conn.commit()


    def user_car_check(self, car_number):

        #DB 연결
        
        conn = pymysql.connect(
            host=self.HOSTNAME,
            port=self.PORT,
            user=self.USERNAME,
            password=self.PASSWORD,
            db=self.DATABASE,
            charset=self.CHARSET
        )

        sql = '''SELECT t1.user_car_number, t1.user_region FROM user_info t1 WHERE t1.user_car_number = (%s)'''
        curs = conn.cursor(pymysql.cursors.DictCursor)
        curs.execute(sql, car_number)


        car_result = curs.fetchone()

        return car_result

    


    def save_recycledata(self, data):    #db 저장 함수

        #DB 연결
        
   
        conn = pymysql.connect(
            host=self.HOSTNAME,
            port=self.PORT,
            user=self.USERNAME,
            password=self.PASSWORD,
            db=self.DATABASE,
            charset=self.CHARSET
        )
   


        sql1='''INSERT INTO trash(trash_Code, trash_Name, user_car_number, trash_region, trash_weight, create_date) VALUES(%s,%s,%s,%s,%s,%s)'''
        val = data
        
        curs=conn.cursor(pymysql.cursors.DictCursor)
        curs.execute(sql1,val)  #trash table에 insert

        conn.commit()



    def run( self ):
        loop = True

        print('clientprocess loop')


        car_number = self.read_car_number()
        time.sleep(1)
        self.car_insert(car_number)
        time.sleep(1)
        car_data = self.user_car_check(car_number)
        time.sleep(1)
        print(car_data)

        try:
            while(loop):
                print( "receiving waiting...\n" )

                
                recv_name = self.client_socket.recv( self.NAME_BUFSIZE )
                print('1')
                if ( recv_name != 'END' ):
                    print('2')
                    recv_code = self.client_socket.recv( self.CODE_BUFSIZE )
                    recv_date = self.client_socket.recv( self.DATE_BUFSIZE )
                    print("receiving complete")
                    
                    
                    
                    car_number_data = car_data['user_car_number'] 
                    
                    region_data = car_data['user_region'] 
                    weight_data = float( 0.7 )


                    name_data = recv_name.decode()


                    if name_data == 'plast1':
                        name_data = '플라스틱(투명)'
                    elif name_data == 'plast2':
                        name_data = '플라스틱(불투명)'
                    elif name_data == 'metal1':
                        name_data = '금속(철류)'
                    elif name_data == 'glass1':
                        name_data = '유리(투명)'
                    elif name_data == 'glass2':
                        name_data = '유리(녹색)'
                    elif name_data == 'glass3':
                        name_data = '유리(갈색)'

                    code_data = recv_code.decode()
                    date_data = recv_date.decode()

 
                    
                    if (len( name_data ) >= self.NAME_BUFSIZE and
                        len( code_data ) >= self.CODE_BUFSIZE and
                        len( date_data ) >= self.DATE_BUFSIZE):
    
                        data = code_data, name_data, car_number_data, region_data, weight_data, date_data
   
                        self.save_recycledata(data)

                    print("{0} {1} {2} {3} {4} {5}\ninsert complete\n".format( code_data, name_data, car_number_data, region_data, weight_data, date_data))
                
                else:
                    loop = False

        except FileNotFoundError:
            pass
        
        except KeyboardInterrupt:
            pass

        finally:
            print( "[Disconnection client]" )
            sys.exit()


if __name__ == '__main__':
    server_ip = '192.168.0.107'
    server_port = 9000
    serverManageProcess = ServerProcess( server_ip, server_port )
    serverManageProcess.start()
    serverManageProcess.join()
    print('Stop Main Process')
        