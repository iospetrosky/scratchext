from flask import Flask, render_template, request
from os.path import exists
import sqlite3

app = Flask(__name__)

def opendb():
    if exists("/home/lorenzopedrotti/www"):
        return sqlite3.connect('/home/lorenzopedrotti/www/flask.db')
    if exists("/home/pi/WWW/scratchext"):
        return sqlite3.connect('/home/pi/WWW/scratchext/flask.db')
    if exists("C:/Users/LPEDR/Documents/SAP/Util/flask"):
        return sqlite3.connect('C:/Users/LPEDR/Documents/SAP/Util/flask/flask.db')

def check_session_cookie():
    if 'session_id' in request.cookies:
        return request.cookies.get('session_id')
    else:
        return 'X'

        
@app.route("/")
def index():
    if check_session_cookie() == 'X':
        return setsession()
        
    htdata = {'menu':'main'}
    return render_template("index.html", data = htdata)

@app.route("/variables")
def variables():
    htdata = {'menu':'variables'}
    return render_template("index.html", data = htdata)

@app.route("/varlist")
def varlist():
    htdata = {'menu':'variables'}
    #get the list from DB
    sql = "select id, session_id, varname, varvalue from myvar"
    rows = opendb().execute(sql).fetchall()
    htdata['rows'] = rows
    htdata['widths'] = [30,80,80, 250]
    htdata['names'] = ['id','session_id','varname','varvalue']
    return render_template("varlist.html", data = htdata)

@app.route("/setsession")    
@app.route("/setsession/<session_id>")
def setsession(session_id='X'):
    htdata = {'menu':'sessions'}
    return render_template("setsession.html", data = htdata)
    
    
    
@app.route("/pushvar/<varname>/<varvalue>")
def pushvar(varname, varvalue):
    db = opendb()
    #try to get the record... and in case update

    #otherwise create a new record


##The next TWO functions are used to deliver the scratch extension
@app.route("/testext.js")
def textext():
    return render_template("testext.js")

@app.route("/crossdomain.xml")
def crossdomain():
    return render_template("crossdomain.xml")

@app.route("/testget/<A>/<B>")
def testget(A,B):
    return "{} + {}".format(A,B)


#commented to run under pythonanywhere.com

if __name__ == "__main__":
    app.run(debug=True)
#    app.run(host='192.168.1.112',debug=True)
