from flask import Flask, render_template, Response, request
from camera import VideoCamera
from eye_detection import EyeDetection
from wtforms import FileField, SubmitField
from flask_wtf import FlaskForm
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired

app = Flask(__name__)
app.config["SECRET_KEY"] = "super"
app.config["UPLOAD_FOLDER"] = "files"

class UploadFileForm(FlaskForm):
    file =FileField("File", validators = [InputRequired()])
    submit = SubmitField("Upload File")


@app.route("/")
def index():
    return render_template("index.html")

def gen(eyeDetect):
    while True:
        frame = eyeDetect.getFrame()
        print("aaaa")
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame
               + b'\r\n')
        

@app.route("/video_feed")
def video_feed():
    return Response(gen(VideoCamera()), 
                    mimetype= 'multipart/x-mixed-replace; boundary=frame')



@app.route("/videoUpLoad", methods=["GET",'POST'])
def videoUpLoad():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config["UPLOAD_FOLDER"], secure_filename(file.filename)))
        return render_template("VideoUpLoadOK.html")
    # video_file = request.files['video_file']
    # video_file.save('.\video.mp4')
    return render_template("VideoUpLoad.html", form = form)



if __name__ == "__main__":
    app.run(host ="0.0.0.0", port = "5000", debug =True)

