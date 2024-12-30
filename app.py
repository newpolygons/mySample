import os
import webbrowser
import terminal
from src import helpers
from flask import Flask, render_template, request, flash, url_for, redirect
from werkzeug.utils import secure_filename
from threading import Timer

currentDir = os.getcwd()
uploadDir = os.path.join(currentDir, 'downloads')
allowedExtenstions = {'mp3', 'wav'}
templateDir = os.path.abspath('frontend/templates')
staticDir = os.path.abspath('frontend/static')

app = Flask(__name__, template_folder = templateDir, static_folder = staticDir)
app.config['UPLOAD_FOLDER'] = uploadDir

def allowed_file(filename):
    #dont blow yourself up this runs locally :) 
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowedExtenstions

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000")

@app.route('/', methods = ['POST', 'GET'])
def frontendFunction():
    if request.method == "POST":
        d = request.form.to_dict()
        link = d.get("link")
        print(str(d))
        if 'file' not in request.files and  link == '':
            flash('Nothing submitted')
            return redirect(request.url)
        elif 'file' not in request.files and helpers.parseLink(link) == 'nothing':
            print(str(link))
            flash('Invalid link provided')
            return redirect(request.url)
        # some browsers submit files with empty name if no file selected.
        file = request.files['file']
        if file.filename == '' and link == '':
            flash('Nothing Submited.')
            return redirect(request.url)
        elif file.filename == '' and helpers.parseLink(link) == 'nothing':
            print(str(link))
            flash('Invalid link provided')
            return redirect(request.url)
        elif file.filename != '' and  link != '':
            print(str(link))
            flash('Cannot Submit local file and link at the same time!')
            return redirect(request.url)
        print(file.filename)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filePath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            terminal.main('local', filePath)
            return redirect(request.url)
        else:
            if helpers.parseLink(link) == 'nothing':
                flash("Please provide a valid link")
                return redirect(request.url)
            else:
                terminal.main('download', link)
                return redirect(request.url)
            print("end of the line")
            print("assuming something went wrong")
            pass
    return render_template('index.html')


if __name__ == "__main__":
    app.secret_key = 'secret'
    Timer(1, open_browser).start()
    app.run(port=5000)


    #https://stackoverflow.com/questions/14525029/display-a-loading-message-while-a-time-consuming-function-is-executed-in-flask