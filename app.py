from flask import Flask
from flask import render_template, request, redirect, send_file
import firebase_admin
from firebase_admin import credentials, storage
from firebase_connector import StorageConnector

import uuid

app = Flask(__name__)

cred = credentials.Certificate("key.json")
firebase_admin.initialize_app(cred, {
    "storageBucket": "adbms-exp6-45b6f.appspot.com"
})
bucket = storage.bucket()
storageConnector = StorageConnector(bucket)


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/image/<filename>')
def get_image(filename):
    filepath = f"images/{filename}"
    return send_file(filepath, mimetype='image/png')

@app.route('/upload', methods=["GET", "POST"])
def upload():
    if request.method == 'POST':
        data = dict(request.form)

        imageName = data["image_name"]
        image = request.files['image']
    
        localPath = f"images/{str(uuid.uuid4())}.jpg" 
        image.save(localPath)
        storageConnector.upload(localPath, f"{imageName}.jpg")
        
        return redirect("/")
    
    return render_template("upload.html")

@app.route('/download', methods=["GET", "POST"])
def download():
    displayImage = None
    
    if request.method == 'POST':
        data = dict(request.form)

        imageName = data["image_name"]
        localImageName = f"{str(uuid.uuid4())}.jpg"
        localPath = f"images/{localImageName}"
        storageConnector.download(f"{imageName}.jpg", localPath)
        
        displayImage = localImageName
        
    return render_template("download.html", image_name=displayImage)

@app.route('/delete', methods=["GET", "POST"])
def delete():
    if request.method == 'POST':
        data = dict(request.form)

        imageName = data["image_name"]
        storageConnector.delete(f"{imageName}.jpg")
        
        return redirect("/")
        
    return render_template("delete.html")

@app.route('/rotate', methods=["GET", "POST"])
def rotate():
    if request.method == 'POST':
        data = dict(request.form)

        imageName = data["image_name"]
        storageConnector.rotate(f"{imageName}.jpg")
        
        return redirect("/")
        
    return render_template("rotate.html")

@app.route('/compress', methods=["GET", "POST"])
def compress():
    if request.method == 'POST':
        data = dict(request.form)

        imageName = data["image_name"]
        storageConnector.compress(f"{imageName}.jpg")
        
        return redirect("/")
        
    return render_template("compress.html")
