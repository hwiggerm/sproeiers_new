#!/usr/bin/python
# -*- coding: utf-8 -*-
#  /home/pi/wiringPi/examples/lights
#
# date 14-jul-19
# version 2.1 hwi
# ported to python3 - no extra functionality
#
#

import MySQLdb as mdb
import time
import sunrise
import datetime as dt
import os

from subprocess import call


#function switch_kaku
def switch_kaku( sdevid, action, ksource ):
    schakel = mdb.connect('localhost','kaku_user','klikaan','kaku')
    slcur = schakel.cursor()
    with slcur:
        # get actual switchtime
        now_c = time.localtime(time.time())
        #convert time to string
        switch_time = time.strftime("%Y-%m-%d %H:%M:%S", now_c)
        
        if int(action)==1:
            # print ('AanSchakelmoment ')
            slcur.execute("select * from switchlist where sdevid=%s",[sdevid])
            nr = slcur.rowcount
            print (nr)
            
            #check on records, if so delete
            if nr>0:
                slcur.execute("delete from switchlist where sdevid = %s",[sdevid])
            #
            # building switchcode based on device data and switch on
            #
            slcur.execute("select devgroup,devcode from devices where devid=%s",[sdevid])
            srows = slcur.fetchall()
            for row in srows:
                if int(sdevid)<10:
                    commando = "sudo " + "/home/pi/raspKaku/kaku " + row[0] + " " + str(row[1]) + " on"      
                    os.system(commando)
                    os.system(commando)
                else:
                    #action
                    commando = "sudo " + "/home/pi/raspKaku/kaku " + row[0] + " " + str(row[1]) + " on"
                    os.system(commando)
                    os.system(commando)


            slcur.execute("insert into switchlist(sdevid) values (%s)",[sdevid])
            
        if int(action)==0:
            # print "UitSchakelmoment "
            #
            # building switchcode based on device data and switch off
            #
            slcur.execute("select devgroup,devcode from devices where devid=%s",[sdevid])
            srows = slcur.fetchall()
            for row in srows:
                if int(sdevid)<10:
                    commando = "sudo " + "/home/pi/raspKaku/kaku " + row[0] + " " + str(row[1]) + " off"      
                    os.system(commando)
                    os.system(commando)
                else:
                    #action
                    commando = "sudo " + "/home/pi/raspKaku/kaku " + row[0] + " " + str(row[1]) + " off"
                    os.system(commando)
                    os.system(commando)


                slcur.execute("delete from switchlist where sdevid = %s",[sdevid])
           
        #save swithmoment for future use
        add_history = "insert into swhistory (sdevid, swmoment, saction, stype) values (%s, %s, %s, %s)"
        #print(add_history)
        slcur.execute(add_history, [sdevid, switch_time, action, ksource])
        schakel.commit();
    return;

#function read_timetable
def read_tt():
        con = mdb.connect('localhost','kaku_user','klikaan','kaku');
        ttcur = con.cursor()
        with ttcur:
                ttcur.execute("select devid, ntime, ssdelta, srdelta, saction from timetable")
                rows = ttcur.fetchall()
        return rows;



#mainprogram
def main():
    oldtime = "00:00"
    #read timetable
    rows = read_tt()
    #endless loop
    while True:
        #loop timetable and compare with currenttime
        #get current time
        now = time.localtime(time.time())
        current_time = time.strftime("%H:%M", now)
        #print(current_time)

        #get the sunrise time for Wageningen
        s = sunrise.sun(lat=51.8,long=5.40)

        #convert time to a datetime
        sr = dt.datetime.combine(dt.date(1901,1,1),s.sunrise())
        ss = dt.datetime.combine(dt.date(1901,1,1),s.sunset() )

        #st = dt.datetime.combine(dt.date(1901,1,1),s.sunrise())
	#print(st)
	#print(st.strftime("%H:%M"))
	#st = st + 10 
	#print(st)


        
        if current_time == '08:30':
           rows = read_tt()
        
        if current_time != oldtime:
            #print('loop')
            #print( current_time )
            for row in rows:
                if row[1] is not None:
                    #there is a switchtime
                    #print ("%s %s %s %s %s" % row)
                    if row[1] == current_time:
                      #print('lights timef on') 
                      switch_kaku(row[0],row[4],'A')
                else:
                    #print('we have a sunrise/set time')
                    #print(row[3])
                    
                    if row[3] is None:
                        #print('sunset')
                        #calculate time
                        #print(row[2])
                        delta_s = dt.timedelta(minutes=row[2])
                        ss =  ss + delta_s
                        
                        #sstime=ss
                        sstime=ss.strftime("%H:%M")
                        #print('SS',sstime)
                        
                        if sstime == current_time:
                            #print ("%s %s %s %s %s" % row)
                            switch_kaku(row[0],row[4],'A')
                    else:
                        #print('sunrise')
                        #calculate time
                        delta_r = dt.timedelta(minutes=row[3])
                        sr =  sr + delta_r
                            
                        srtime=time.strftime("%H:%M")
                        print('sr',srtime)

                        if srtime == current_time:
                            #print( "%s %s %s %s %s" % row)
                            switch_kaku(row[0],row[4],'A')
                            #to ensure we switch oly one time per minute
                            oldtime = current_time
    return;


#run the mainprogram
if __name__ == "__main__":
    main()
