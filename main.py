# Real Time Human Detection, Counting, And Tracking

# imported necessary library
from http import client
from tkinter import *
from centroidtracker import CentroidTracker
import tkinter as tk
import tkinter.messagebox as mbox
from PIL import ImageTk, Image
import cv2
import numpy as np
import imutils
import argparse
from fpdf import FPDF
import datetime
import math
import pandas as pd


import mysql.connector


protopath = "ResNetSSD_deploy.prototxt"
modelpath = "ResNetSSD_deploy.caffemodel"
detector = cv2.dnn.readNetFromCaffe(prototxt=protopath, caffeModel=modelpath)

# broker = 'armadillo.rmq.cloudamqp.com'
# port = 1883
# topic = "jmlPelanggan"

# generate client ID with pub prefix randomly
# client_id = f'python-mqtt-{random.randint(0, 100)}'
# username = 'zwlrpnko:zwlrpnko'
# password = 'VhM5RTgFuKVMudvzrAoRZk5ebITarytH'


CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
           "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
           "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
           "sofa", "train", "tvmonitor"]



#Tracker
tracker = CentroidTracker(maxDisappeared=10, maxDistance=1800)


# Main Window & Configuration
window = tk.Tk()
window.title("Real Time Customer Detection & Counting")
window.geometry('1000x700')

# top label
start1 = tk.Label(text = "REAL-TIME-CUSTOMER\nDETECTION  &  COUNTING", font=("Arial", 50,"underline"), fg="magenta") # same way bg
start1.place(x = 70, y = 10)

# function defined to start the main application
def start_fun():
    window.destroy()

# created a start button
Button(window, text="▶ START",command=start_fun,font=("Arial", 25), bg = "orange", fg = "blue", cursor="hand2", borderwidth=3, relief="raised").place(x =130 , y =570 )

# image on the main window
path1 = "Images/front3.png"
img2 = ImageTk.PhotoImage(Image.open(path1))
panel1 = tk.Label(window, image = img2)
panel1.place(x = 90, y = 250)

# image on the main window
path = "Images/front1.png"
img1 = ImageTk.PhotoImage(Image.open(path))
panel = tk.Label(window, image = img1)
panel.place(x = 380, y = 180)

exit1 = False
# function created for exiting from window
def exit_win():
    global exit1
    if mbox.askokcancel("Exit", "Do you want to exit?"):
        exit1 = True
        window.destroy()

# exit button created
Button(window, text="❌ EXIT",command=exit_win,font=("Arial", 25), bg = "red", fg = "blue", cursor="hand2", borderwidth=3, relief="raised").place(x =680 , y = 570 )

window.protocol("WM_DELETE_WINDOW", exit_win)
window.mainloop()

if exit1==False:
    # Main Window & Configuration of window1
    window1 = tk.Tk()
    window1.title("Real Time Costumer Detection & Counting")
    window1.geometry('1000x700')

    # db = mysql.connector.connect(
    #     host="localhost",
    #     user="root",
    #     passwd="",
    #     database="counter"
    # )



    def argsParser():
        arg_parse = argparse.ArgumentParser()
        arg_parse.add_argument("-c", "--camera", default=False, help="Set true if you want to use the camera.")
        arg_parse.add_argument("-o", "--output", type=str, help="path to optional output video file")
        args = vars(arg_parse.parse_args())
        return args

    # ---------------------------- camera section ------------------------------------------------------------
    def camera_option():
        # new window created for camera section
        windowc = tk.Tk()
        windowc.title("Human Detection from Camera")
        windowc.geometry('1000x700')

        max_count3 = 0
        rects = []
        obj_id_list = []
        sys_start = ""
        sys_stop = ""
        pagi = 0
        pagi2 = 0
        pagi3 = 0
        pagi4 = 0
        siang = 0
        siang2 = 0
        siang3 = 0
        siang4 = 0
        siang5 = 0
        sore = 0
        sore2 = 0
        sore3 = 0
        sore4 = 0
        malam = 0
        malam2 = 0
        malam3 = 0
        malam4 = 0
        lpc_counts = 0
        
        def round_up(n, decimals=0):
            multiplier = 10 ** decimals
            return math.ceil(n * multiplier) / multiplier

        def non_max_suppression_fast(boxes, overlapThresh):
            try:
                if len(boxes) == 0:
                    return []
                if boxes.dtype.kind == "i":
                    boxes = boxes.astype("float")
                
                pick = []

                x1 = boxes[:, 0]
                y1 = boxes[:, 1]
                x2 = boxes[:, 2]
                y2 = boxes[:, 3]

                area = (x2 - x1 + 1) * (y2 - y1 + 1)
                idxs = np.argsort(y2)

                while len(idxs) > 0:
                    last = len(idxs) - 1
                    i = idxs[last]
                    pick.append(i)

                    xx1 = np.maximum(x1[i], x1[idxs[:last]])
                    yy1 = np.maximum(y1[i], y1[idxs[:last]])
                    xx2 = np.minimum(x2[i], x2[idxs[:last]])
                    yy2 = np.minimum(y2[i], y2[idxs[:last]])

                    w = np.maximum(0, xx2 - xx1 + 1)
                    h = np.maximum(0, yy2 - yy1 + 1)

                    overlap = (w * h) / area[idxs[:last]]

                    idxs = np.delete(idxs, np.concatenate(([last],
                                                        np.where(overlap > overlapThresh)[0])))
                return boxes[pick].astype("int")
            except Exception as e:
                print("Exception occurred in non_max_suppression : {}".format(e))

        # function defined to open the camera
        def open_cam():
            global max_count3, obj_id_list, sys_start, sys_stop, pagi, pagi2, pagi3, pagi4, siang, siang2, siang3, siang4, siang5, sore, sore2, sore3, sore4, malam, malam2, malam3, malam4, lpc_counts, cpc_counts, rects, client

            max_count3 = 0
            rects = []
            obj_id_list = []
            sys_start = ""
            sys_stop = ""
            pagi = 0
            pagi2 = 0
            pagi3 = 0
            pagi4 = 0
            siang = 0
            siang2 = 0
            siang3 = 0
            siang4 = 0
            siang5 = 0
            sore = 0
            sore2 = 0
            sore3 = 0
            sore4 = 0
            malam = 0
            malam2 = 0
            malam3 = 0
            malam4 = 0
            lpc_counts = 0
            cpc_counts = 0
            
            # client = mqttClient.Client("Python")
            

            args = argsParser()

            info1.config(text="Status : Opening Camera...")
            # info2.config(text="                                                  ")
            mbox.showinfo("Status", "Opening Camera...Please Wait...", parent=windowc)
            # time.sleep(1)

            writer = None
            if args['output'] is not None:
                writer = cv2.VideoWriter(args['output'], cv2.VideoWriter_fourcc(*'MJPG'), 10, (600, 600))
            if True:
                detectByCamera(writer)

        # function defined to detect from camera
        def detectByCamera(writer):
            global max_count3, obj_id_list, sys_start, sys_stop, pagi, pagi2, pagi3, pagi4, siang, siang2, siang3, siang4, siang5, sore, sore2, sore3, sore4, malam, malam2, malam3, malam4, lpc_counts, cpc_counts, rects, client

            max_count3 = 0
            rects = []
            obj_id_list = []
            sys_start = ""
            sys_stop = ""
            pagi = 0
            pagi2 = 0
            pagi3 = 0
            pagi4 = 0
            siang = 0
            siang2 = 0
            siang3 = 0
            siang4 = 0
            siang5 = 0
            sore = 0
            sore2 = 0
            sore3 = 0
            sore4 = 0
            malam = 0
            malam2 = 0
            malam3 = 0
            malam4 = 0
            lpc_counts = 0
            cpc_counts = 0
            
            # client = mqttClient.Client("Python")

            # function defined to plot the people count in camera

            def cam_gen_report():
                pdf = FPDF(orientation='P', unit='mm', format='A4')
                pdf.add_page()
                pdf.set_font("Arial", "", 20)
                pdf.set_text_color(128, 0, 0)
                pdf.image('Images/Crowd_Report-1.png', x=0, y=0, w=210, h=297)
                now = datetime.datetime.now().date()
                # sql_now = datetime.datetime.now()

                dateCreated =str(now) +" From : "+str(sys_start.hour)+":"+str(sys_start.minute)+" - "+str(sys_stop.hour)+":"+str(sys_stop.minute)

                
                if (sys_start.minute<10 and sys_stop.minute<10):
                    dateCreated =str(now) +" From : "+str(sys_start.hour)+":0"+str(sys_start.minute)+" - "+str(sys_stop.hour)+":0"+str(sys_stop.minute)
                elif(sys_start.minute<10 and sys_stop.minute>10):
                    dateCreated =str(now) +" From : "+str(sys_start.hour)+":0"+str(sys_start.minute)+" - "+str(sys_stop.hour)+":"+str(sys_stop.minute)
                elif(sys_start.minute>10 and sys_stop.minute<10):
                    dateCreated =str(now) +" From : "+str(sys_start.hour)+":"+str(sys_start.minute)+" - "+str(sys_stop.hour)+":"+str(sys_stop.minute)
                
                # cursor = db.cursor()
                # sql = "INSERT INTO people (Tanggal, Jumlah) VALUES (%s, %s)"

                # val = (sql_now.strftime('%Y-%m-%d %H:%M:%S'), str(len(obj_id_list)))
                # cursor.execute(sql, val)

                # db.commit()

                # print("{} data ditambahkan".format(cursor.rowcount))

                pdf.text(120, 155, str(max_count3))
                pdf.text(95, 168, str(len(obj_id_list)))
                pdf.text(50, 181, dateCreated)
                pdf.text(109, 206, str(pagi))
                pdf.text(109, 218, str(pagi2))
                pdf.text(109, 230, str(pagi3))
                pdf.text(109, 242, str(siang))

                pdf.add_page()
                pdf.set_font("Arial", "", 20)
                pdf.set_text_color(128, 0, 0)
                pdf.image('Images/Crowd_Report-2.png', x=0, y=0, w=210, h=297)


                pdf.text(109, 35, str(siang2))
                pdf.text(109, 45, str(siang3))
                pdf.text(109, 55, str(siang4))
                pdf.text(109, 67, str(sore))
                pdf.text(109, 77, str(sore2))

                pdf.output('Crowd_Report_'+str(now)+'.pdf')
                mbox.showinfo("Status", "Report Generated and Saved Successfully.", parent = windowc)

                data = {
                    'Tanggal': [dateCreated],
                    '7 Sampai 8': [str(pagi)],
                    '9 Sampai 10': [str(pagi2)],
                    '11 Sampai 12': [str(pagi3)],
                    '13 Sampai 14': [str(siang)],
                    '15 Sampai 16': [str(siang2)],
                    '17 Sampai 18': [str(siang3)],
                    '19 Sampai 20': [str(siang4)],
                    '21 Sampai 22': [str(sore)],
                    '23 Sampai 00': [str(sore2)],
                }

                # Make data frame of above data
                df = pd.DataFrame(data)
                
                # append data frame to CSV file
                df.to_csv('csv/count.csv', mode='a', index=False, header=False)
                
                # print message
                print("Data appended successfully.")

            cap = cv2.VideoCapture(3)
            sys_start = datetime.datetime.now()

            fps_start_time = datetime.datetime.now()
            fps = 0
            total_frames = 0 
            
            while True:
                ret, frame = cap.read()
                frame = imutils.resize(frame, height=600,)
                total_frames = total_frames + 1

                (H, W) = frame.shape[:2]

                blob = cv2.dnn.blobFromImage(frame, 0.007843, (W, H), 127.5)

                detector.setInput(blob)
                person_detections = detector.forward()
                rects = []
                for i in np.arange(0, person_detections.shape[2]):
                    confidence = person_detections[0, 0, i, 2]
                    if confidence > 0.5:
                        idx = int(person_detections[0, 0, i, 1])

                        if CLASSES[idx] != "person":
                            continue

                        person_box = person_detections[0, 0, i, 3:7] * np.array([W, H, W, H])
                        (startX, startY, endX, endY) = person_box.astype("int")
                        rects.append(person_box)

                boundingboxes = np.array(rects)
                boundingboxes = boundingboxes.astype(int)
                rects = non_max_suppression_fast(boundingboxes, 0.3)

                objects = tracker.update(rects)
                for (objectId, bbox) in objects.items():
                    x1, y1, x2, y2 = bbox
                    x1 = int(x1)
                    y1 = int(y1)
                    x2 = int(x2)
                    y2 = int(y2)

                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                    text = "ID: {}".format(objectId)
                    cv2.putText(frame, text, (x1, y1-5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), 1)

                    if objectId not in obj_id_list:
                        obj_id_list.append(objectId)
                        time_in = datetime.datetime.now()
                        print(time_in.hour)
                        if (time_in.hour >= 7 and time_in.hour <=8):
                            print("Pagi")
                            pagi = pagi + 1
                            print (str(pagi))
                        elif(time_in.hour >= 9 and time_in.hour <=10):
                            print("Pagi2")
                            pagi2 = pagi2 + 1
                            print (str(pagi2))
                        elif(time_in.hour >= 11 and time_in.hour <=12):
                            print("pagi3")
                            pagi3 = pagi3 + 1
                            print (str(siang))
                        elif(time_in.hour >= 13 and time_in.hour <=14):
                            print("Siang")
                            siang = siang + 1
                            print (str(siang))
                        elif(time_in.hour >= 15 and time_in.hour <=16):
                            print("Siang2")
                            siang2 = siang2 + 1
                            print (str(siang2))
                        elif(time_in.hour >= 17 and time_in.hour <=18):
                            print("Siang3")
                            siang3 = siang3 + 1
                            print (str(siang3))
                        elif(time_in.hour >= 19 and time_in.hour <=20):
                            print("Siang4")
                            siang4 = siang4 + 1
                            print (str(siang4))
                        elif(time_in.hour >= 21 and time_in.hour <=22):
                            print("Sore")
                            sore = sore + 1
                            print (str(sore))
                        elif(time_in.hour >= 23 and time_in.hour <=24):
                            print("Sore2")
                            sore2 = sore2 + 1
                            print (str(sore2))
                        

                fps_end_time = datetime.datetime.now()
                time_diff = fps_end_time - fps_start_time
                if time_diff.seconds == 0:
                    fps = 0.0
                else:
                    fps = (total_frames / time_diff.seconds)

                fps_text = "FPS: {:.2f}".format(fps)

                cv2.putText(frame, fps_text, (5, 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), 1)
                # client.publish("python/test",fps_text)

                lpc_counts = len(objects)
                cpc_counts = len(obj_id_list)
                


                if (lpc_counts > max_count3):
                    max_count3 = lpc_counts

                lpc_txt = "Person In Room Now: {}".format(lpc_counts)
                cpc_txt = "Total Person Today: {}".format(cpc_counts)
                
                
                cv2.putText(frame, lpc_txt, (5, 60), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), 1)
                cv2.putText(frame, cpc_txt, (5, 90), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), 1)

                clock = datetime.datetime.now()

                # if (clock.hour == 23 and clock.minute == 59):
                #     cam_gen_report()
                #     pagi = 0
                #     siang = 0
                #     sore = 0
                #     malam = 0


                cv2.imshow("Human Detection from Camera", frame)
                key = cv2.waitKey(1)
                if key & 0xFF == ord('q'):
                    sys_stop = datetime.datetime.now()
                    print (str(sys_start))
                    print (str(sys_stop))
                    # client.disconnect()
                    # client.loop_stop()
                    cam_gen_report()
                    break

            cap.release()
            info1.config(text="                                                  ")
            # info2.config(text="                                                  ")
            info1.config(text="Status : Detection & Counting Completed")
            # info2.config(text="Max. Human Count : " + str(max_count3))
            cv2.destroyAllWindows()

            # Button(windowc, text="Generate Report", command=cam_gen_report, cursor="hand2", font=("Arial", 20),bg="gray", fg="blue").place(x=325, y=550)

        lbl1 = tk.Label(windowc, text="DETECT  FROM\nCAMERA", font=("Arial", 50, "underline"), fg="brown")  # same way bg
        lbl1.place(x=230, y=20)

        Button(windowc, text="OPEN CAMERA", command=open_cam, cursor="hand2", font=("Arial", 20), bg="light green", fg="blue").place(x=370, y=230)

        info1 = tk.Label(windowc, font=("Arial", 30), fg="gray")  # same way bg
        info1.place(x=100, y=330)
        # info2 = tk.Label(windowc, font=("Arial", 30), fg="gray")  # same way bg
        # info2.place(x=100, y=390)

        # function defined to exit from the camera window
        def exit_winc():
            if mbox.askokcancel("Exit", "Do you want to exit?", parent = windowc):
                windowc.destroy()
        windowc.protocol("WM_DELETE_WINDOW", exit_winc)


    # options -----------------------------
    lbl1 = tk.Label(text="OPTION", font=("Arial", 50, "underline"),fg="brown")  # same way bg
    lbl1.place(x=340, y=20)

    # image on the main window
    pathi = "Images/image1.jpg"
    imgi = ImageTk.PhotoImage(Image.open(pathi))
    paneli = tk.Label(window1, image = imgi)
    paneli.place(x = 90, y = 110)

    # image on the main window
    pathv = "Images/image2.png"
    imgv = ImageTk.PhotoImage(Image.open(pathv))
    panelv = tk.Label(window1, image = imgv)
    panelv.place(x = 700, y = 260)# 720, 260

    # image on the main window
    pathc = "Images/image3.jpg"
    imgc = ImageTk.PhotoImage(Image.open(pathc))
    panelc = tk.Label(window1, image = imgc)
    panelc.place(x = 90, y = 415)

    # created button for all option
    Button(window1, text="DETECT FROM CAMERA ➡",command=camera_option, cursor="hand2", font=("Arial", 30), bg = "light green", fg = "blue").place(x = 110, y = 300)

    # function defined to exit from window1
    def exit_win1():
        if mbox.askokcancel("Exit", "Do you want to exit?"):
            window1.destroy()

    # created exit button
    Button(window1, text="❌ EXIT",command=exit_win1,  cursor="hand2", font=("Arial", 25), bg = "red", fg = "blue").place(x = 440, y = 600)

    window1.protocol("WM_DELETE_WINDOW", exit_win1)
    window1.mainloop()

