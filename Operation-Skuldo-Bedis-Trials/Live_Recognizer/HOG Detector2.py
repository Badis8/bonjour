import face_recognition
import cv2 as cv
import numpy as np
import os
import time
import datetime as date 
class handler:
    path=''
    path_uploads=''
    known_faces=[]
    labels=[]
    def __init__(self):
        self.path=os.path.dirname(os.path.realpath(__file__))  #gives me the apsolute path name of current file 
        self.path_uploads = os.path.join(self.path, "..", "Web_Server", "uploads")
    def add(self,direct,name): #adds the features of a face in a list, we can use them to compare later
        face_image=face_recognition.load_image_file(os.path.join(self.path, "DataSet", direct,name))
        face_image_features=face_recognition.face_encodings(face_image)[0]
        if(len(face_image_features)!=128):
            print("no face detected")
        else:
            self.known_faces.append(face_image_features)
            self.labels.append(direct)
    def compare(self,image):
        frame = face_recognition.load_image_file(os.path.join(self.path_uploads,image))
        face_locations = face_recognition.face_locations(frame)   
        face_encodings = face_recognition.face_encodings(frame, face_locations)
        for  face_encoding in face_encodings:
            matches = face_recognition.compare_faces(self.known_faces,face_encoding)
            name = "Unknown"
            face_distances = face_recognition.face_distance(self.known_faces,face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = self.labels[best_match_index]
        return(name,frame)

 
my_handler=handler()
my_handler.add("Bedis","bedis.jpg")  
my_handler.add("Yassine","yassine.jpg")
done=[]
executed=0
while(True):
    files = os.listdir(my_handler.path_uploads)
    number_of_files=len(files)
    if(executed!=number_of_files):
        for file_name in files: 
            if(file_name not in done):
                time.sleep(1)
                name,frame=my_handler.compare(files[files.index(file_name)])
                print(name)
                if(name=="Unknown"):
                    cv.imwrite(os.path.join(my_handler.path,"..","Web_Server","static","unknowns",file_name),frame)
                done.append(file_name)
    else :
        continue





            
         

