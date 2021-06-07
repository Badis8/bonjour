import cv2 as cv
import numpy as np
import datetime as date
import csv


face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')
face_recognizer = cv.face.LBPHFaceRecognizer_create()
face_recognizer.read("data.yml")
cap = cv.VideoCapture(0)

ids = {}


with open("output.csv",'r') as data:   
    for line in csv.reader(data) :
        ids[line[1]] = line[0]


conf = 0
while True :
    r, frame = cap.read()
    gray = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray,scaleFactor = 1.1, minNeighbors =4)
    for x,y,w,h in faces :
        cv.rectangle(frame, (x,y), (x+w,y+h), (0,255,255))
        roi = gray[y:y+h,x:x+w]
        
        id,conf = face_recognizer.predict(roi)
        print(conf)

            
        cv.putText(frame, ids[str(id)], (x,y+h), cv.FONT_HERSHEY_PLAIN, 1,(255,255,0)  )



    
    cv.imshow('frame', frame)
    if cv.waitKey(20) & 0xFF == ord('q') :
        break


cap.release()
cv.destroyAllWindows()
