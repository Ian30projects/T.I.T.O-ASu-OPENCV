import tkinter as tk
from tkinter import *
import cv2
from PIL import Image, ImageTk
import face_recognition
import os
import csv
from datetime import datetime
# import datetime as dt
# from tkinter import ttk
# import pytz
# import functools as fc







# Initialize the camera
cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 500)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 500)

# Load a pre-trained face detection cascade classifier
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

#------------------------------------------For Image Location
known_images_path = ['img/don', 'img/ian', 'img/sonnie']
known_face_encodings = []
known_face_names = []

                                #Read the Path file 
for i in range(3):
    for filename in os.listdir(known_images_path[i]):
        if filename.endswith((".jpg", ".png")):
            name = os.path.splitext(filename)[0]
            image = face_recognition.load_image_file(os.path.join(known_images_path[i], filename))
            encoding = face_recognition.face_encodings(image)[0]
            known_face_encodings.append(encoding)
            known_face_names.append(name)
detected_names = set()
#------------------------------------------For Image Location END



def CIN():


    def record_time_in():

        current_date = datetime.now().strftime('%Y-%m-%d')
        path_in = 'check_in'+ current_date+'.csv'

        isExist_in = os.path.exists(path_in)


        if isExist_in == True:
        # csv_file = open('attendance'+ current_time+'.csv','w', newline='')
            csv_file = open('check_in'+ current_date+'.csv','r+', newline='')
            csv_writer_in = csv.writer(csv_file)
        else:
            csv_file = open('check_in'+ current_date+'.csv','w', newline='')
            csv_writer_in = csv.writer(csv_file)



        #-------------CREATE FRAME FOR CAMERA
        _, frame = cam.read()
        frame = cv2.flip(frame, 1)
        #-------------CREATE FRAME FOR CAMERA end

        
        #----------------Detect faces in the frame
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        #----------------Detect faces in the frame end

        #----------------rwectangle sa Detect faces 
        for (x, y, w, h) in faces:
            face = frame[y:y + h, x:x + w]
            rgb_face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
            face_encodings = face_recognition.face_encodings(rgb_face)

            if len(face_encodings) > 0:
                matches = face_recognition.compare_faces(known_face_encodings, face_encodings[0])
                
                name = "Unknown"
                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_face_names[first_match_index]

                    #PARA MAAPALITAN YUNG NAME NA ILALAGAY SA CSV
                    remove = "()123456789"
                    for char in remove:
                        name = name.replace(char, "")
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    cv2.putText(frame, name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

                    if name not in detected_names:
                        # Record the current time

                        csv_writer_in.writerow([name])
                        detected_names.add(name)
        #----------------rwectangle sa Detect faces end


        
        #----------para may maprocess na img
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        photo = ImageTk.PhotoImage(image=image)
        #----------para may maprocess na img end
        
        #-----------para magpakita sa ROOT o Tkinter
        vid_frame.create_image(0, 0, image=photo, anchor=tk.NW)
        vid_frame.photo = photo
        #-----------para magpakita sa ROOT o Tkinter end

        # para may frame
        root.after(10, record_time_in)




    root = tk.Tk()
    root.resizable(False, False)
    root.geometry("1417x720+150+50")
    root.title("Face Recognition")


    vid_frame = tk.Canvas(root, width=500, height=500)
    vid_frame.place(x=30, y=60)



    time_in_label = tk.Label(root, text="Time In: ")
    time_in_label.place(x=30, y=570)
    time_out_label = tk.Label(root, text="Time Out: ")
    time_out_label.place(x=30, y=600)

    time_in_button = tk.Button(root, text="Time In", command=lambda: [root.quit(), CIN()])
    time_in_button.place(x=200, y=565)
    time_out_button = tk.Button(root, text="Time Out", command=lambda: [root.quit(), COUT()])
    time_out_button.place(x=200, y=595)



    record_time_in()
    root.mainloop()
    return root



def COUT():


    def record_time_out():

        current_date = datetime.now().strftime('%Y-%m-%d')
        path_out = 'check_out'+ current_date+'.csv'

        isExist_out = os.path.exists(path_out)



        if isExist_out == True:
        # csv_file = open('attendance'+ current_time+'.csv','w', newline='')
            csv_file = open('check_out'+ current_date+'.csv','r+', newline='')
            csv_writer_out = csv.writer(csv_file)
        else:
            csv_file = open('check_out'+ current_date+'.csv','w', newline='')
            csv_writer_out = csv.writer(csv_file)



        #-------------CREATE FRAME FOR CAMERA
        _, frame = cam.read()
        frame = cv2.flip(frame, 1)
        #-------------CREATE FRAME FOR CAMERA end

        
        #----------------Detect faces in the frame
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        #----------------Detect faces in the frame end

        #----------------rwectangle sa Detect faces 
        for (x, y, w, h) in faces:
            face = frame[y:y + h, x:x + w]
            rgb_face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
            face_encodings = face_recognition.face_encodings(rgb_face)

            if len(face_encodings) > 0:
                matches = face_recognition.compare_faces(known_face_encodings, face_encodings[0])
                
                name = "Unknown"
                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_face_names[first_match_index]

                    #PARA MAAPALITAN YUNG NAME NA ILALAGAY SA CSV
                    remove = "()123456789"
                    for char in remove:
                        name = name.replace(char, "")
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    cv2.putText(frame, name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

                    if name not in detected_names:
                        # Record the current time

                        csv_writer_out.writerow([name])
                        detected_names.add(name)
        #----------------rwectangle sa Detect faces end


        
        #----------para may maprocess na img
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        photo = ImageTk.PhotoImage(image=image)
        #----------para may maprocess na img end
        
        #-----------para magpakita sa ROOT o Tkinter
        vid_frame.create_image(0, 0, image=photo, anchor=tk.NW)
        vid_frame.photo = photo
        #-----------para magpakita sa ROOT o Tkinter end

        # para may frame
        root.after(10, record_time_out)




    root = tk.Tk()
    root.resizable(False, False)
    root.geometry("1417x720+150+50")
    root.title("Face Recognition")


    vid_frame = tk.Canvas(root, width=500, height=500)
    vid_frame.place(x=30, y=60)



    time_in_label = tk.Label(root, text="Time In: ")
    time_in_label.place(x=30, y=570)
    time_out_label = tk.Label(root, text="Time Out: ")
    time_out_label.place(x=30, y=600)

    time_in_button = tk.Button(root, text="Time In", command=lambda: [root.quit(), CIN()])
    time_in_button.place(x=200, y=565)
    time_out_button = tk.Button(root, text="Time Out", command=lambda: [root.quit(), COUT()])
    time_out_button.place(x=200, y=595)



    record_time_out()
    root.mainloop()
    return root

CIN()