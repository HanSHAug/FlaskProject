from datetime import datetime
from flask import Flask, flash, session, redirect
from flask import request
from flask import render_template, url_for
from flask import flash
from flask_sqlalchemy import SQLAlchemy
import json
import pymysql 

class err(Exception):
    def __init__(self):
        print("무게입력X")

app = Flask(__name__)

# app.secret_key = 'sqasd12asdzxcsada'


@app.route('/')
def home():
    if session.get('id'):
        return render_template('inp.html')
    else:
        return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        request_id = request.form['id']
        request_password = request.form['password']
        if len(request_id)==0 & len(request_password)==0:
            return 'id or password not found'
        else:
            db = pymysql.connect(host='ec2-3-101-124-183.us-west-1.compute.amazonaws.com', \
            port=3306, user='root', passwd='1234', db='health', charset='utf8') 
            cursor = db.cursor(pymysql.cursors.DictCursor)
            sql = """
            SELECT * FROM user where id='%s'; 
            """ % request_id
            cursor.execute(sql)
            result = cursor.fetchall() #result = [{'id': 'abcd', 'password': 1234}]
            try:   
                result = result[0]
                # print(result)        # result = {'id': 'abcd', 'password': 1234}
                # print(request_id)   # abcd
                # print(request_password) # 1234
                if result['id'] == request_id and result['password'] == int(request_password):
                    session['id'] = request_id
                    return render_template('inp.html')
                else:
                    return render_template('index.html')
            except:
                flash("잘못된 정보입니다.")
                return redirect('/')
            

    else:
        return '잘못된 접근'

@app.route('/logout', methods=['POST','GET'])
def logout():
    session.clear()
    return redirect('/')

    # request_id = request.form.get('id')
    # try:
    #     if request_id == session['id']:
    #         return 'already login'
    #     else:
    #         return 'error'
    # except:
    #     request_password = request.form.get('password')
    #     db = pymysql.connect(host='ec2-3-101-124-183.us-west-1.compute.amazonaws.com', \
    #         port=3306, user='root', passwd='1234', db='health', charset='utf8') 
    #     cursor = db.cursor()
    #     sql = """
    #     SELECT * FROM user where id='%s'; 
    #     """%request_id
        
    #     cursor.execute(sql)
    #     result = cursor.fetchall()
    #     if result[0][1] == int(request_password):
    #         session['id'] = request_id
    #     print(result)
    #     db.commit()
    #     db.close()

    #     return 'a'

@app.route('/inp')
def inp():
    return render_template('inp.html')

@app.route('/view')
def view():
    return render_template('view.html')


@app.route('/input', methods=['POST'])
def input():
    
    try:
        image = request.files['chooseFile']

        filename=image.filename
        splitedFilename = filename.split(".")
        now=datetime.now().strftime('%Y%m%d_%H%M%S')
        imagePATH = "static/img/"
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
    db = pymysql.connect(host='ec2-3-101-124-183.us-west-1.compute.amazonaws.com', \
        port=3306, user='root', passwd='1234', db='health', charset='utf8') 
    cursor = db.cursor()
    sql = """
    INSERT INTO datas VALUES('%s',%s,'%s','%s');
    """ % (now1, weight, imagePATH+finalFileName, session['id'])
    cursor.execute(sql)
    db.commit()
    db.close()
    #INSERT INTO datas VALUES('1999-08-22 11:11:11',83.55,'/home/ec2-user/FlaskProject/images/20220423_105411.jpg')

    flash('업로드 완료')
    return render_template('inp.html')

@app.route('/body', methods =['GET'])
def body():
    db = pymysql.connect(host='ec2-3-101-124-183.us-west-1.compute.amazonaws.com', \
        port=3306, user='root', passwd='1234', db='health', charset='utf8') 
    cursor = db.cursor()
    sql = """
    SELECT * FROM datas where user_id ='%s'; 
    """ % session['id']
    cursor.execute(sql)
    
    result = cursor.fetchall()
    
    result_list = []
    for r in result :
        tmp = dict()
        tmp["date"] = r[0].strftime('%Y-%m-%d %H:%M:%S')
        tmp["weight"] = r[1]
        tmp["image_path"] = r[2]
        result_list.append(tmp)
    
    

    retValue = json.dumps(result_list)
    
    #retValue = "{\"health_datas\" : " + retValue + "}"
    retValue = '{"health_datas" :  %s }' % retValue


    db.commit()
    db.close()

    return retValue




if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True, host="0.0.0.0")