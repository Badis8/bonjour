import cv2 as cv
import numpy as np
import os
import csv

face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')
face_recognizer = cv.face.LBPHFaceRecognizer_create()

main_dir = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(main_dir,"images")

Residents = {}
idCounter = 0
TrainList =[]
ids =[]


for root , dirs , files in os.walk(path) :
    for dir in dirs :
        if not dir in Residents :
            Residents[dir]= idCounter
            idCounter += 1
    for f in files :
        src = os.path.join(path,root,f)
        img = cv.imread(src)
        
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray,scaleFactor = 1.1, minNeighbors =5 )
        for x,y,w,h in faces :
            TrainList.append(gray[y:y+h,x:x+w])
            ids.append(Residents[os.path.basename(root)])


print(len(TrainList))
print(len(ids))



face_recognizer.train((TrainList),np.array(ids))

print("Done ???????")

face_recognizer.save("data.yml")


"""
with open("output.txt","w") as f :
    json.dump(Residents, f)"""


w = csv.writer(open("output.csv", "w", newline=''))
w.writerow(["Name","ID"])
for key, val in Residents.items():
    w.writerow([key, val])
