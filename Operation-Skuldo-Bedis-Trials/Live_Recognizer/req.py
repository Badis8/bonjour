import requests
import cv2 as cv


url = "http:// 10.10.22.83:5000/upload/"

im = cv.imread("mergeza.jpg")

#{'file': <_io.BufferedReader name='mergeza.jpg'>}
#files = {'file': open('mergeza.jpg', 'rb')}

b , arr = cv.imencode(".jpg",im)

files = arr.tobytes()
#print(files)

r = requests.post(url, files={'file': files})
