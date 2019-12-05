from flask import Flask, render_template, request, send_from_directory, make_response
from os.path import exists, join as pathjoin
import sqlite3, string, random

app = Flask(__name__)

def opendb():
    if exists("/home/lorenzopedrotti/www"):
        return sqlite3.connect('/home/lorenzopedrotti/www/flask.db')
    if exists("/home/pi/WWW/scratchext"):
        return sqlite3.connect('/home/pi/WWW/scratchext/flask.db')
    if exists("C:/Users/LPEDR/Documents/SAP/Util/flask"):
        return sqlite3.connect('C:/Users/LPEDR/Documents/SAP/Util/flask/flask.db')

def check_cookie(ckname):
    if ckname in request.cookies:
        return request.cookies.get(ckname)
    else:
        return 'X'
    
def check_session_cookie():
    return check_cookie('session_id')

def check_user_cookie():
    return check_cookie('user_id')

    
@app.route("/")
def index():
    if check_user_cookie() == 'X': return logon()
        
    htdata = {'menu':'main'}
    return render_template("index.html", data = htdata)

@app.route("/varlist")
def varlist():
    if check_user_cookie() == 'X': return logon()
    if check_session_cookie() == 'X': return mysessions()

    htdata = {'menu':'variables'}
    #get the list from DB
    db = opendb()
    htdata['session'] = check_session_cookie()
    sql = "select id, session_id, varname, varvalue from myvar where session_id = '{}'".format(check_session_cookie())
    rows = db.execute(sql).fetchall()
    htdata['rows'] = rows
    htdata['widths'] = [30,180,80,250]
    htdata['names'] = ['id','session_id','varname','varvalue']
    return render_template("varlist.html", data = htdata)

@app.route("/newsession",methods=["POST","GET"])    
def newsession():
    if check_user_cookie() == 'X': return logon()
    if request.method == 'POST':
        letters = string.ascii_lowercase + string.ascii_uppercase
        newid = ''.join(random.choice(letters) for i in range(12))
        sql = "insert into sessions (session_id, user_id) values ('{}','{}')"
        sql = sql.format(newid,check_user_cookie())
        db = opendb()
        db.execute(sql)
        db.commit()
        return mysessions()
    
    htdata = {'menu':'sessions'}
    return render_template("newsession.html", data = htdata)
    
@app.route("/setsession/<session_id>")
def setsession(session_id):
    if check_user_cookie() == 'X': return logon()
    #sql = 
    
@app.route("/mysessions")
def mysessions():
    if check_user_cookie() == 'X': return logon()
    
    #get the list of sessions and pass to the template
    htdata = {'menu':'sessions'}
    sql = "select id, session_id from sessions where user_id = {}".format(check_user_cookie())
    rows = opendb().execute(sql).fetchall()
    htdata['rows'] = rows
    htdata['widths'] = [30,180]
    htdata['names'] = ['id','session_id']
    return render_template("mysessions.html", data = htdata)

@app.route("/newvar", methods=["POST","GET"])
def newvar():
    if check_user_cookie() == 'X': return logon()
    if check_session_cookie() == 'X': return mysessions()
    if request.method == 'POST':
        sql = "insert into myvar (session_id, varname, varvalue) values ('{}','{}','{}')"
        sql = sql.format(check_session_cookie(), request.form['varname'], request.form['varvalue'])
        db = opendb()
        db.execute(sql)
        db.commit()
        return varlist()
        
    htdata = {'menu':'variables'}
    htdata['session'] = check_session_cookie()
    return render_template("newvar.html", data = htdata)
    
@app.route("/logon", methods=["POST","GET"])
def logon():
    #is there a logon attempt?
    if request.method == 'POST':
        sql = "select id, name from users where name = '{}' and passwd = '{}'".format(request.form['login'],request.form['password'])
        user = opendb().execute(sql).fetchone()
        if user is not None:
            htdata = {'menu':'main', 'screen':'welcome', 'info': "Welcome {}".format(user[1])}
            resp = make_response(render_template("index.html", data = htdata))
            try:
                if request.form["remember_me"] == "X":
                    resp.set_cookie('user_id', value = str(user[0]), max_age = 60*60*24*365) #remember for 1 year
            except:
                resp.set_cookie('user_id', value = str(user[0])) #remember for session
            resp.set_cookie('session_id', '', -1)
            return resp
        else:
            htdata = {'menu':'main', 'screen':'logon', 'info': 'Invalid user name or password'}
            resp = make_response(render_template("index.html", data = htdata))
            resp.set_cookie('user_id', '', -1)
            resp.set_cookie('session_id', '', -1)
            return resp
    #in all other cases
    htdata = {'menu':'main', 'screen':'logon'}
    resp = make_response(render_template("index.html", data = htdata))
    resp.set_cookie('user_id', '', -1)
    resp.set_cookie('session_id', '', -1)
    return resp


###########  AJAX CALLS  ############
@app.route("/getsession/<id>")
def get_session_name(id):
    sql = "select session_id from sessions where id = {}".format(id)
    return make_response(opendb().execute(sql).fetchone()[0])

@app.route("/delsession/<id>")
def delete_session(id):
    db = opendb()
    id_tx = db.execute("select session_id from sessions where id = {}".format(id)).fetchone()[0]
    db.execute("delete from sessions where id = {}".format(id))
    db.execute("delete from myvar where session_id = '{}'".format(id_tx))
    db.commit()
    return 'ok'
    
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

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(pathjoin(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')    

#commented to run under pythonanywhere.com

if __name__ == "__main__":
    app.run(debug=True)
#    app.run(host='192.168.1.112',debug=True)
