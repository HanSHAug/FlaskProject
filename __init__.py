from datetime import datetime
from logging import exception
from flask import Flask
from flask import request
from flask import render_template


class err(Exception):
    def __init__(self):
        print("석일뱃살")

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/input', methods=['POST'])
def input():
    
    try:
        image = request.files['chooseFile']

        filename=image.filename
        splitedFilename = filename.split(".")
        now=datetime.now().strftime('%Y%m%d_%H%M%S')
        imagePATH = "./images/"
        finalFileName = now + "." + splitedFilename[1]
        image.save(dst=imagePATH+finalFileName)
    except:
        pass
    try:
        weight = request.form.get('weight')
        if weight == "" :
            raise err
        f = open("weight.txt", 'a')
        conf = open("main.config", 'r')
        line = conf.readline()   
        f.write(weight+line+"\n")
        f.close()

    except:
        pass

    return 'hello'


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")