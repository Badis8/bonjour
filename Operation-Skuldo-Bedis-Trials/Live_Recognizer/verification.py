import cv2 as cv
import numpy as np
import datetime as date
import csv
import mysql.connector as sql


today = date.datetime.now()

d = str(today.strftime("%B %d, %Y %H:%M:%S"))


d = d.replace(":","-")
d = d.replace(",","at")



d = today.strftime("%B %d, %Y %H:%M:%S")
d = d.replace(":","-")
d = d.replace(",","at")

"""
f = open("output.csv","r")
dic = dict(list(csv.DictReader(f))[0])

print(dic)
"""
"""
db = sql.connect(host="localhost",user="root",passwd="Ec_p0lMki1xL",database="test")
mycursor = db.cursor()
mycursor.execute("select * from myguests")
result = mycursor.fetchone()
for i in result :
    print(i)

"""



"""
face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')

frame = cv.imread("E:\PROGRAMATION\Python\Operation Skuld\images\Bill Gates\download (2).jpg")
gray = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(gray,scaleFactor = 1.1, minNeighbors =4)

for x,y,w,h in faces :
    cv.rectangle(frame, (x,y), (x+w,y+h), (0,255,255))

cv.imshow("frame", frame)
cv.waitKey(0)"""


#main_dir = os.path.dirname(os.path.abspath(__file__))

#matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
"""
db = sql.connect(host="localhost",user="root",passwd="Ec_p0lMki1xL",database="test")
mycursor = db.cursor()
mycursor.execute("select * from myguests")
result = mycursor.fetchone()
"""
