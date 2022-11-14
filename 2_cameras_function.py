# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 10:15:27 2022

@author: PLAP033
"""
import threading
import cv2 as cv
import os
import face_recognition
import numpy as np
import datetime
import pyttsx3

video_entry = cv.VideoCapture(0)
video_exit = cv.VideoCapture(1) 


def imagesListInFolder(folderPath):
    imagesList=[]
    classes = []
    imagesFiles = os.listdir(folderPath)
    for imageFile in imagesFiles:
        image = cv.imread(f'{folderPath}/{imageFile}')
        imagesList.append(image)
        classes.append((os.path.splitext(imageFile)[0]))
    return imagesList,classes

def findencodings(images):
    img_encodings = []
    for img in images:
          img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
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
    withGreetings = greet + " " + name
    speech.say(withGreetings)            
    speech.runAndWait()
    speech.stop()
     
def compare(faceDis, tolerance=0.43):
    return list(faceDis <= tolerance)
        
def find_person(cam):
    persons_in_current_frame.clear()
    _,frame = cam.read()
    rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    face_location = face_recognition.face_locations(rgb_frame)
    encodes_frame = face_recognition.face_encodings(rgb_frame,face_location)
    for encodeface,faceLoc in zip(encodes_frame,face_location):
        faceDis = face_recognition.face_distance(encodeListKnown, encodeface)
        matches = compare(faceDis)
        matchIndex = np.argmin(faceDis)
        if matches[matchIndex]:
            name = classes[matchIndex].upper()
            y1, x2, y2, x1 = faceLoc
            cv.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv.rectangle(frame, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv.FILLED)
            cv.putText(frame, name, (x1 + 6, y2 - 6), cv.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            persons_in_current_frame.add(name)
    return frame,persons_in_current_frame
        

def entry_cam(new_persons_set):
    while True:
        status = "entered"
        for name in new_persons_set:
            if name not in (new_persons_set & old_persons_set_entry):
                speak(name,"Welcome")
                markAttendance(name,status)
                entry = datetime.datetime.now() 
            print(f'{name} entered at {entry}')
            old_persons_set_entry = new_persons_set.copy()
            return entry


def exit_cam(new_persons_set):        
    while True:
        status = "exited"
        for name in new_persons_set:
            if name not in (new_persons_set & old_persons_set_exit):
                speak(name, "Good bye")
                markAttendance(name,status)
                exit = datetime.datetime.now()
            print(f'{name} exited at {exit}')            
            old_persons_set_exit = new_persons_set.copy()
            return exit

def time_spent(exit,entry):
    total_time = exit - entry
    print(total_time)


folderPath = "training_images" #trainingImagesPath
images,classes = imagesListInFolder(folderPath)
encodeListKnown = findencodings(images) 
facecascade = cv.CascadeClassifier("haarcascade_frontalface_default.xml")
old_persons_set_entry = set([])
persons_in_current_frame = set([])
old_persons_set_exit = set([])
frame_entry, new_persons_set1 = find_person(video_entry)
frame_exit, new_persons_set2 = find_person(video_exit)


t1 = threading.Thread(target = entry_cam, args=(new_persons_set1,))
t2 = threading.Thread(target = exit_cam, args=(new_persons_set2,))
t1.start()
t2.start()
cv.imshow("entry",frame_entry)
cv.imshow("exit",frame_exit)

cv.waitKey(1)        
t1.join()
t2.join()

video_entry.release()
video_exit.release()
cv.destroyAllWindows()
