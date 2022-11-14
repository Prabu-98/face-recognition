# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 10:15:27 2022

@author: PLAP033
"""
import cv2
import os
import face_recognition
import numpy as np
import datetime
import pyttsx3

video_entry = cv2.VideoCapture('rtsp://admin:@192.168.1.240/live/0/MAIN')
video_entry.set(cv2.CAP_PROP_FPS,5)
#video_entry.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
#video_entry.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
# out = cv2.VideoWriter('output_face.mp4', cv2.VideoWriter_fourcc(*'mp4v'),2.0, (1280, 720))

def imagesListInFolder(folderPath):
    imagesList=[]
    classes = []
    imagesFiles = os.listdir(folderPath)
    for imageFile in imagesFiles:
        image = cv2.imread(f'{folderPath}/{imageFile}')
        imagesList.append(image)
        classes.append((os.path.splitext(imageFile)[0]))
    return imagesList,classes

def findencodings(images):
    img_encodings = []
    for img in images:
          img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
          img = face_recognition.face_encodings(img)[0]
          img_encodings.append(img)
    return img_encodings 

def markAttendance(name,status):
    now = datetime.datetime.now()
    filenameCsv = str(now.strftime("%d_%b_%Y")) + ".csv"
   
    with open(filenameCsv, 'a+') as f:
        dtTime = now.strftime('%H:%M:%S')
        dtDate = now.strftime("%d/%b/%Y") 
        f.writelines('\n')
        f.writelines(f'{name},{status},{dtTime},{dtDate}')

def speak(name,greet = " "):
    speech = pyttsx3.init()
    withGreetings = greet + name
    speech.say(withGreetings)            
    speech.runAndWait()
    speech.stop()
     
def compare(known_face_encodings, face_encoding_to_check, tolerance=0.43):
    return list(face_recognition.face_distance(known_face_encodings, face_encoding_to_check) <= tolerance)
        
def find_person(cam):
    persons_in_current_frame.clear()
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
                persons_in_current_frame.add(name)
    return frame,persons_in_current_frame

folderPath = "training_images" #trainingImagesPath
images,classes = imagesListInFolder(folderPath)
encodeListKnown = findencodings(images) 
facecascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
old_persons_set_entry = set([])
persons_in_current_frame = set([])
old_persons_set_exit = set([])

while True:
    frame_entry, new_persons_set = find_person(video_entry)
    status = "entered"
    for name in new_persons_set:
        if name not in (new_persons_set & old_persons_set_entry):
            speak(name,"hello")
            markAttendance(name,status)
    old_persons_set_entry = new_persons_set.copy()
    cv2.imshow("entry",frame_entry)
    # out.write(frame_entry)
    key = cv2.waitKey(1)
    if key == 27: #esc
        break
# out.release()
video_entry.release()
cv2.destroyAllWindows()
