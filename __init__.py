from datetime import datetime
from logging import exception
from flask import Flask
from flask import request
from flask import render_template
import pymysql 

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
        imagePATH = "/home/ec2-user/FlaskProject/images/"
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
    
    
    now1=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    db = pymysql.connect(host='ec2-3-101-124-183.us-west-1.compute.amazonaws.com', port=3306, user='root', passwd='1234', db='health', charset='utf8') 
    cursor = db.cursor()
    sql = """
    INSERT INTO datas VALUES('%s',%s,'%s');
    """ % (now1, weight, imagePATH+finalFileName)
    cursor.execute(sql)
    db.commit()
    db.close()
    #INSERT INTO datas VALUES('1999-08-22 11:11:11',83.55,'/home/ec2-user/FlaskProject/images/20220423_105411.jpg')


    return 'hello'




if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")