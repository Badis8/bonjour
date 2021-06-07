import face_recognition
import cv2 as cv
import numpy as np
import os
import time
import datetime as date 
import threading
import my_project.Database.BaseManager as dm 
 
class handler:
    path=''
    path_uploads=''
    path_dataset = ''
    known_faces=[]
    labels=[]
    bd=dm.Base()
    def __init__(self):
        self.path=os.path.dirname(os.path.realpath(__file__))  #gives me the apsolute path name of current file 
        self.path_uploads = os.path.join(self.path,"my_project", "Web_Server", "uploads")
        self.path_dataset = os.path.join(self.path,"my_project","Live_Recognizer","DataSet" )
    def add(self,direct,name): #adds the features of a face in a list, we can use them to compare later
        face_image=face_recognition.load_image_file(os.path.join(self.path,"my_project","Live_Recognizer", "DataSet", direct,name))

        face_image_features=face_recognition.face_encodings(face_image)[0]
        
        
        if(len(face_image_features)!=128):
            print("no face detected")
        else:
            self.known_faces.append(face_image_features)
            self.labels.append(direct)
    def compare(self,image):
        names=[]
        file_names=[]
        frame = face_recognition.load_image_file(os.path.join(self.path_uploads,image))
        face_locations = face_recognition.face_locations(frame)  
         
        face_encodings = face_recognition.face_encodings(frame, face_locations)
        print(len(face_locations))
        i=1
        file_multiple_face=image
        for  face_encoding in face_encodings:
          
            matches = face_recognition.compare_faces(self.known_faces,face_encoding)
            name = "Unknown"
            face_distances = face_recognition.face_distance(self.known_faces,face_encoding)
            best_match_index = np.argmin(face_distances)
            if(i==1):
            
                if matches[best_match_index]:
                    name = self.labels[best_match_index]
                    names.append(name)
                    self.bd.connect()
                    print("updating to"+image)
                    self.bd.update(image,name)
                    file_names.append(image)
                    self.bd.close()
                    i=i+1
                else: 
                    print("unknown:/")
                    file_names.append(image)
                    names.append("unknown")
                    i=i+1         
            else: 
              
                if matches[best_match_index]:   
                    name = self.labels[best_match_index]
                    names.append(name)
                    self.bd.connect()
                    image=str(i)+image
                    file_names.append(image)
                    self.bd.insert(image,name)
                    self.bd.close()
                    print("adding face number"+str(i))
                    i=i+1
                else: 
                    image="face"+str(i)+image
                    self.bd.connect()
                    self.bd.insert(image,"unknown")
                    names.append("unknown")
                    file_names.append(image)
                    print("adding face number"+str(i))
                    i=i+1
                    self.bd.close()

           
        return(file_names,names,frame)


    def scanFaces (self) :
        for root,dir,files in os.walk(self.path_dataset):            
            if os.path.basename(root) not in self.labels :
                for f in files :
                    self.add(os.path.basename(root),f)
                print("new list",self.labels)
        print("new list",self.labels)


#my_handler.add("Bedis","bedis.jpg")  
#my_handler.add("Yassine","yassine.jpg")



def realtime_scanner(exit) :
    global my_handler,lock
    while(not exit.is_set()) :
        lock.acquire()
        my_handler.scanFaces()
        lock.release()
        time.sleep(30)
    if (lock.locked()):
        lock.release()

def recognizer(exit) :
    global my_handler,done,executed,lock

    while(not exit.is_set()):
        lock.acquire()
        files = os.listdir(my_handler.path_uploads)
        number_of_files=len(files)
        if(executed!=number_of_files):
            for file_name in files: 
                if(file_name not in done):
                    time.sleep(1)
                    file_names_server=[]
                    file_names_server,names,frame=my_handler.compare(files[files.index(file_name)])
                    for (file_name_server,name) in zip(file_names_server,names):
                        print(file_names_server)
                        print(names)
                        if(name=="unknown"):
                            cv.imwrite(os.path.join(my_handler.path,"my_project","Web_Server","static","unknown",file_name_server),frame)
                            
                        else:
                            cv.imwrite(os.path.join(my_handler.path,"my_project","Web_Server","static","knowns",file_name_server),frame)
                    done.append(file_name)
                
        lock.release()
    if (lock.locked()):
        lock.release()
my_handler=handler()
my_handler.scanFaces()
done=[]
executed=0
exit = threading.Event()
lock = threading.Lock()
t1= threading.Thread(target=realtime_scanner,args=[exit])

t2 = threading.Thread(target=recognizer,args=[exit])
t1.start()
t2.start()  

try :
    while(1) :
        pass
except KeyboardInterrupt :
    exit.set()
    print("it s set")

         

