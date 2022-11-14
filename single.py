# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 10:15:27 2022

@author: PLAP033
"""
import base64
import cv2
import os
import face_recognition
import numpy as np
import mysql.connector

video_entry = cv2.VideoCapture(1)
video_entry.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
video_entry.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
out = cv2.VideoWriter('face recognition.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 5.0, (1280, 720))

def imagesListInFolder(host_,user_,password_,database_):
        
    connection = mysql.connector.connect(host=host_,user = user_, password = password_, database = database_)
    cursor = connection.cursor()
    #querying
    images = "SELECT Image FROM user_face.user "
    label =  "SELECT Name FROM user_face.user "
    
    cursor.execute(images)
    photo = cursor.fetchall()
    
    cursor.execute(label)
    labels = cursor.fetchall()
    imagesList=[]
    classes = []
    
    for photo in photo:
        a = photo.encode()
        data_to_img =  base64.b64encode(a)
        image = cv2.imread(data_to_img)
        imagesList.append(image)
        classes.append(labels)


        
    cursor.close()
    connection.close()
    return imagesList,classes

def findencodings(images):
    img_encodings = []
    for img in images:
          img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
          img = face_recognition.face_encodings(img)[0]
          img_encodings.append(img)
    return img_encodings 

     
def compare(known_face_encodings, face_encoding_to_check, tolerance=0.43):
    
    return list(face_recognition.face_distance(known_face_encodings, face_encoding_to_check) <= tolerance)
        
def find_person(cam):
    _,frame = cam.read()
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    faces = facecascade.detectMultiScale(rgb_frame, scaleFactor = 1.05, minNeighbors = 5)
    for x,y,w,h in faces:
        face_location = face_recognition.face_locations(rgb_frame)
        encodes_frame = face_recognition.face_encodings(rgb_frame,face_location)
        for encodeface,faceLoc in zip(encodes_frame,face_location):
            matches = compare(encodeListKnown,encodeface)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeface)
            matchIndex = np.argmin(faceDis)
            if matches[matchIndex]:
                name= classes[matchIndex].upper()
                y1, x2, y2, x1 = faceLoc
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(frame, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(frame, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
    return frame

host_,user_,password_,database_ = "localhost","root","Prabhu123@","user_face"
 

images,classes = imagesListInFolder(host_,user_,password_,database_ )
encodeListKnown = findencodings(images) 
facecascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

while True:
    try:
        frame_entry = find_person(video_entry)
        cv2.imshow("entry",frame_entry)
        out.write(frame_entry)
        key = cv2.waitKey(1)
        if key == 27: #esc
            break
    except:
        break
out.release()
video_entry.release()
cv2.destroyAllWindows()
