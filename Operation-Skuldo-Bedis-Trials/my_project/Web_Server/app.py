from datetime import date
from flask import Flask,render_template,request,redirect,url_for,session
import os
import cv2 as cv
import numpy as np
import sqlite3
from ..Database import BaseManager as dm
db=dm.Base()
app = Flask(__name__)

i=0
app.secret_key = '_kyG#IO5pD9(oS0_X'
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['user']== 'admin' and request.form['pass'] =='123456' :
            session['username'] = 'admin'
        return redirect(url_for('homepage'))
    return render_template('login.html')

@app.route("/addface",methods=['GET','POST'])
def add_to_data_set() :
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '' or not (file.filename.endswith(".jpg")):
            return redirect(request.url)
        name = request.form['name']
        os.makedirs("My_project/Live_Recognizer/DataSet/"+name)
        file.save(os.path.join("My_project/Live_Recognizer/DataSet",name,name + ".jpg" ))
        return redirect(url_for('homepage'))
    return render_template("addface.html")

@app.route("/")
def homepage():  
    print("bonjour")
    global db 
    db.connect()
    unknowns=db.selectUnknows()
    knowns=db.selectAll()
    liste_information=[]
    liste_information.append(len(unknowns))
    liste_information.append(len(knowns))
    liste_information.append(len(knowns)+len(unknowns))

    if 'username' in session:
        return render_template('home.html',liste_information=liste_information)
    return redirect(url_for('login'))
     

@app.route("/live-stream")
def live_stream():
    return render_template('Live-stream.html')

@app.route("/unknows")
def unknown():
    global db 
    db.connect()
    files_withoutpng=db.selectUnknows()
    db.close()
    if(files_withoutpng==[]): 
        print("here")
        return("non")
    else:
        return render_template('Unknows.html',files=files_withoutpng)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))
@app.route("/upload/",methods=['POST'])
def uploadFile():
    global i
    global db
    db.connect()
    if request.method == 'POST':
        number_facess=request.json
        print(number_facess)
        file = request.files['file'].read()      
        
        
        
        
        number_faces=number_facess[0]
       

        arr = np.frombuffer(file,dtype="uint8")
        im = cv.imdecode(arr,1)
        cv.imwrite('my_project/Web_Server/uploads/image{}.jpg'.format(i),im)
        print("here"+str(i))
        for j in range(number_faces) :
            db.insert("image{}_{}.jpg".format(i,j))
            db.close()
        i+=1
        print(i)
        return "..."
@app.route("/forme",methods=['get','post'])
def traitement_form():
    return(render_template('choice.html'))
@app.route("/show",methods=['POST'])
def affichage():
    global db 
    db.connect()
    if(request.form["person_type"]=="all"):
        if(request.form["date"]!=""): 
            date_requested=request.form["date"]
            liste=db.selectAll(date=date_requested)

                
            for user_info in liste:
                if ("unknown" not in user_info): 
                    id,date,person=user_info
                    liste[liste.index(user_info)]=(id,date,"knowns",person)
            for item in liste :
                a = item[0].index("_")
                b = item[0].index(".")
                item[0].replace(item[0][a:b],"")
                print(item[0])

            return(render_template('show.html',liste=liste))
        else:
            liste=db.selectAll()
            for user_info in liste:
                if ("unknown" not in user_info): 
                    id,date,person=user_info
                    liste[liste.index(user_info)]=(id,date,"knowns",person)
            for item in liste :
                a = item[0].index("_")
                b = item[0].index(".")
                item[0].replace(item[0][a:b],"")
                print(item[0])
            return(render_template('show.html',liste=liste))
    elif(request.form["person_type"]=="unknown"):
        if(request.form["date"]!=""): 
            date_requested=request.form["date"]
            liste=db.selectUnknows(date=date_requested)
            for item in liste :
                a = item[0].index("_")
                b = item[0].index(".")
                item[0].replace(item[0][a:b],"")
                print(item[0])
            return(render_template('show.html',liste=liste))
        else: 
            liste=db.selectUnknows()
            for item in liste :
                a = item[0].index("_")
                b = item[0].index(".")
                item[0].replace(item[0][a:b],"")
                print(item[0])
            return(render_template('show.html',liste=liste))
    elif(request.form["person_type"]=="known"):
            if(request.form["date"]!=""): 
                date_requested=request.form["date"]
                liste=db.selectVerified(date=date_requested)
                for user_info in liste:
                    id,date,person=user_info
                    liste[liste.index(user_info)]=(id,date,"knowns",person)
                for item in liste :
                    a = item[0].index("_")
                    b = item[0].index(".")
                    item[0].replace(item[0][a:b],"")
                    print(item[0])
                return(render_template('show.html',liste=liste))
            else: 
                liste=db.selectVerified()
                for user_info in liste:
                    id,date,person=user_info
                    liste[liste.index(user_info)]=(id,date,"knowns",person)
                for item in liste :
                    a = item[0].index("_")
                    b = item[0].index(".")
                    item[0].replace(item[0][a:b],"")
                    print(item[0])
                return(render_template('show.html',liste=liste))
            

    return("here")
app.run(debug=True,host= '0.0.0.0',port=5000)
