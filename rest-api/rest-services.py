import pymysql
from app import app
from mysql import mysql
from flask import jsonify
from flask import flash, request
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import numpy as np

# from werkzeug import generate_password_hash,check_password_hash
@app.route('/')
def home():
    return "Restful Services for Spam Classifier"

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    loaded_model = pickle.load(open('../model/spam_classifier.sav', 'rb'))
    loaded_vectorizer = pickle.load(open("../model/tfidfvectorizer.pickle", "rb"))
    spam_dict = {1: "SPAM", 0: "NOT SPAM"}
    list_of_new_testing_data = []
    list_of_new_testing_data.append(data['message'])
    tranformed_data = loaded_vectorizer.transform(list_of_new_testing_data)
    predictions = loaded_model.predict(tranformed_data)
    return spam_dict[predictions[0]]

def predict(message):
    loaded_model = pickle.load(open('../model/spam_classifier.sav', 'rb'))
    loaded_vectorizer = pickle.load(open("../model/tfidfvectorizer.pickle", "rb"))
    spam_dict = {1: "SPAM", 0: "NOT SPAM"}
    list_of_new_testing_data = []
    list_of_new_testing_data.append(message)
    tranformed_data = loaded_vectorizer.transform(list_of_new_testing_data)
    predictions = loaded_model.predict(tranformed_data)
    return predictions[0]

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        conn = mysql.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute("SELECT * FROM user WHERE email='{}' and password='{}'".format(data["email"],data["password"]))
        rows = cur.fetchall()
        if(len(rows)>0):
            resp = jsonify({'message':'login success'})
            resp.status_code = 200
        else:
            resp = jsonify({'message':'login failed'})
            resp.status_code = 400
        return resp
    except Exception as e:
        print(e)
    finally:
        cur.close()
        conn.close()

"""
USER REST SERVICES
"""
@app.route('/email/create', methods=['POST'])
def email_create():
    try:
        data = request.get_json()
        conn = mysql.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute("INSERT INTO email VALUES(0,'{}','{}','{}','{}',{})".format(data["subject"],data["body"],data["sender"],data["receiver"],predict(data["body"])))

        # insert into email values(0,'sub','message','sender','receiver',spam_detector)
        conn.commit()
        resp = jsonify({'message':'Email Created'})
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cur.close()
        conn.close()

@app.route('/email/delete/<string:id>', methods=['DELETE'])
def email_delete(id):
    try:
        conn = mysql.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute("DELETE FROM email where eid='{}'".format(id))
        conn.commit()
        resp = jsonify({'message':'Email Deleted'})
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cur.close()
        conn.close()

@app.route('/email/inbox/<string:email>', methods=['GET'])
def email_inbox(email):
    try:
        conn = mysql.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute("SELECT * from email where receiver='{}' and is_spam=0".format(email))
        rows = cur.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cur.close()
        conn.close()
@app.route('/email/spam/<string:email>', methods=['GET'])
def email_spam(email):
    try:
        conn = mysql.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute("SELECT * from email where receiver='{}' and is_spam=1".format(email))
        rows = cur.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cur.close()
        conn.close()

@app.route('/email/sent/<string:email>', methods=['GET'])
def email_sent(email):
    try:
        conn = mysql.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute("SELECT * from email where sender='{}'".format(email))
        rows = cur.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cur.close()
        conn.close()

@app.route('/email/all/<string:email>', methods=['GET'])
def email_all(email):
    try:
        conn = mysql.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute("SELECT * from email where (sender='{}' or receiver='{}')".format(email,email))
        rows = cur.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cur.close()
        conn.close()



"""
ADMIN REST SERVICES
"""


@app.route('/user/create', methods=['POST'])
def user_create():
    try:
        data = request.get_json()
        conn = mysql.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute("INSERT INTO user VALUES('{}','{}')".format(data["email"],data["password"]))
        conn.commit()
        resp = jsonify({'message':'User Created'})
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cur.close()
        conn.close()


@app.route('/user/delete/<string:email>', methods=['DELETE'])
def user_delete(email):
    try:
        conn = mysql.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute("DELETE FROM user where email='{}'".format(email))
        conn.commit()
        resp = jsonify({'message':'User Deleted'})
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cur.close()
        conn.close()


@app.route('/user/update/<string:email>', methods=['PUT'])
def user_update(email):
    try:
        data = request.get_json()
        conn = mysql.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute("UPDATE user SET password='{}' where email='{}';".format(data['password'],email))
        conn.commit()
        resp = jsonify({'message': 'User Updated'})
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cur.close()
        conn.close()

@app.route('/user/read/<string:email>', methods=['GET'])
def user_read(email):
    try:
        conn = mysql.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute("SELECT * from user where email='{}';".format(email))
        rows = cur.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cur.close()
        conn.close()

@app.route('/user/read_all', methods=['GET'])
def user_read_all():
    try:
        conn = mysql.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute("SELECT * from user;")
        rows = cur.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cur.close()
        conn.close()

@app.route('/email/read_all', methods=['GET'])
def email_read_all():
    try:
        conn = mysql.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute("SELECT * from email;")
        rows = cur.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cur.close()
        conn.close()





@app.errorhandler(404)
def not_found():
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp
if __name__ == "__main__":
    app.run()
