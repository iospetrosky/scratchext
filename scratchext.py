from flask import Flask, render_template, request, send_from_directory, make_response
from os.path import exists, join as pathjoin
import string, random, sys, pygal
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins":"*"}})

def print_debug(text):
    dbg = True #debug main switch
    if dbg:
        caller = sys._getframe(1).f_code.co_name
        print('Calling from: ' + caller, file=sys.stderr)
        print(text)

def opendb():
    if exists("/home/lorenzopedrotti/www"):
        return mysql.connector.connect(
                host="lorenzopedrotti.mysql.pythonanywhere-services.com",
                user="lorenzopedrotti",
                passwd="shannara71",
                database="lorenzopedrotti$myvar"
                )
    if exists("/home/pi/WWW/scratchext"):
        return mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="emberlee1",
                database="pyany01"
                )

def check_cookie(ckname):
    if ckname in request.cookies:
        return request.cookies.get(ckname)
    else:
        return 'X'

def check_session_cookie():
    return check_cookie('session_id')

def check_user_cookie():
    return check_cookie('user_id')

def is_PRO(db):
    #check if a user is a PRO user
    sql = "select count(id) from users where id = {} and groups like '%PRO%'".format(check_user_cookie())
    cur = db.cursor()
    cur.execute(sql)
    #print_debug(sql)
    if cur.fetchone()[0] == 1:
        return True
    else:
        return False

def fetch_single_value(db,sql):
    cur = db.cursor()
    cur.execute(sql)
    return cur.fetchone()[0]

def count_session_vars(db):
    #counts the variables defined in this session
    sql = "select count(id) from myvar where session_id = '{}'".format(check_session_cookie())
    return int(fetch_single_value(db,sql))

def count_user_sessions(db):
    #counts how many sessions are owned by the current user
    sql = "select count(id) from sessions where user_id = {}".format(check_user_cookie())
    return int(fetch_single_value(db,sql))

@app.route("/")
def index():
    #print_debug(request.user_agent.platform)
    #platforms = "Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini"
    if check_user_cookie() == 'X': return logon()

    htdata = {'menu':'main'}
    return render_template("index.html", data = htdata)

@app.route("/testchart")
def testchart():
    if check_user_cookie() == 'X': return logon()
    if check_session_cookie() == 'X': return mysessions()
    htdata = {'menu':'variables'}
    line_chart = pygal.Line()
    line_chart.title = 'Test chart'
    line_chart.x_labels = ["a","b","c"]
    line_chart.add('Peppers', [ 46.3, 42.8, 37.1])
    line_chart.add('Roses',  [ 10.8, 23.8, 35.3])
    htdata["chart"] = line_chart.render_data_uri()
    return render_template("testchart.html", data = htdata)

@app.route("/varlist")
def varlist():
    if check_user_cookie() == 'X': return logon()
    if check_session_cookie() == 'X': return mysessions()

    htdata = {'menu':'variables'}
    #get the list from DB
    db = opendb()
    htdata['session'] = check_session_cookie()
    #retrieve the prittyname
    sql = "select prittyname from sessions where session_id = '{}'".format(check_session_cookie())
    cur = db.cursor()
    cur.execute(sql)
    rows = cur.fetchone()
    htdata['prittyname'] = rows[0]
    #retrieve the variables
    sql = "select id, session_id, varname, varvalue from myvar where session_id = '{}'".format(check_session_cookie())
    cur.execute(sql)
    rows = cur.fetchall()
    db.close()
    htdata['rows'] = rows
    htdata['widths'] = [30,180,100,250]
    htdata['formelements'] = ['text','text','input','input']
    htdata['names'] = ['id','session_id','varname','varvalue']
    return render_template("varlist.html", data = htdata)

@app.route("/tablist")
def tablist():
    if check_user_cookie() == 'X': return logon()
    if check_session_cookie() == 'X': return mysessions()

    htdata = {'menu':'variables'}
    #get the list from DB
    db = opendb()
    htdata['session'] = check_session_cookie()
    #retrieve the prittyname
    sql = "select prittyname from sessions where session_id = '{}'".format(check_session_cookie())
    cur = db.cursor()
    cur.execute(sql)
    rows = cur.fetchone()
    htdata['prittyname'] = rows[0]
    # retrieve the tables
    sql = "select id, session_id, tab_name, f1_name, f2_name,f3_name,"\
          "f4_name,f5_name,f6_name,f7_name,f8_name,f9_name "\
           "from table_defs where session_id='{}'".format(check_session_cookie())
    cur.execute(sql)
    rows = cur.fetchall()
    db.close()
    htdata['rows'] = rows
    htdata['widths'] = [30,180,100,100,100,100,100,100,100,100,100,100]
    htdata['headers'] = [' ',' ',' ','Table name','Field 1','Field 2','Field 3','Field 4','Field 5','Field 6','Field 7','Field 8','Field 9']
    htdata['formelements'] = ['text','text','input','input','input','input','input','input','input','input','input','input']
    htdata['names'] = ['id','session_id','tab_name','f1_name','f2_name','f3_name','f4_name','f5_name','f6_name','f7_name','f8_name','f9_name']
    return render_template("tablist.html", data = htdata)



@app.route("/newsession",methods=["POST","GET"])
def newsession():
    if check_user_cookie() == 'X': return logon()
    htdata = {'menu':'sessions'} #this will be redefined in case we call mysessions()

    if request.method == 'POST':
        db = opendb()
        if is_PRO(db) or count_user_sessions(db) < 1:
            letters = string.ascii_lowercase + string.ascii_uppercase
            newid = ''.join(random.choice(letters) for i in range(12))
            sql = "insert into sessions (session_id, user_id) values ('{}','{}')"
            sql = sql.format(newid,check_user_cookie())
            cur = db.cursor()
            cur.execute(sql)
            db.commit()
            db.close()
            return mysessions()
        else:
            db.close()
            htdata['info'] = "You must have a PRO account to add more than ONE session"

    return render_template("newsession.html", data = htdata)

@app.route("/setsession/<session_id>")
def setsession(session_id):
    if check_user_cookie() == 'X': return logon()

@app.route("/mysessions")
def mysessions():
    if check_user_cookie() == 'X': return logon()

    #get the list of sessions and pass to the template
    htdata = {'menu':'sessions'}
    sql = "select id, session_id, prittyname from sessions where user_id = {}".format(check_user_cookie())
    db = opendb()
    cur = db.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    db.close()
    htdata['rows'] = rows
    htdata['widths'] = [30,180,300]
    htdata['names'] = ['id','session_id','prittyname']
    htdata['formelements'] = ['text','text','input']
    return render_template("mysessions.html", data = htdata)

@app.route("/newvar", methods=["POST","GET"])
def newvar():
    if check_user_cookie() == 'X': return logon()
    if check_session_cookie() == 'X': return mysessions()
    htdata = {'menu':'variables'} #this will be redefined in case we call varlist()

    if request.method == 'POST':
        db = opendb()

        if is_PRO(db) or count_session_vars(db) < 4:
            sql = "insert into myvar (session_id, varname, varvalue) values ('{}','{}','{}')"
            sql = sql.format(check_session_cookie(), request.form['varname'], request.form['varvalue'])
            cur = db.cursor()
            cur.execute(sql)
            db.commit()
            db.close()
            return varlist()
        else:
            db.close()
            htdata['info'] = "You must have a PRO account to add more than 4 variables"

    htdata['session'] = check_session_cookie()
    return render_template("newvar.html", data = htdata)

@app.route("/newtab", methods=["POST","GET"])
def newtab():
    if check_user_cookie() == 'X': return logon()
    if check_session_cookie() == 'X': return mysessions()
    htdata = {'menu':'variables'} #this will be redefined in case we call varlist()

    if request.method == 'POST':
        db = opendb()

        if is_PRO(db) or count_session_vars(db) < 4:
            sql = "insert into table_defs (session_id, tab_name) values ('{}','{}')"
            sql = sql.format(check_session_cookie(), request.form['tabname'])
            cur = db.cursor()
            cur.execute(sql)
            db.commit()
            db.close()
            return tablist()
        else:
            db.close()
            htdata['info'] = "You must have a PRO account to add more than 4 variables"

    htdata['session'] = check_session_cookie()
    return render_template("newtab.html", data = htdata)


@app.route("/delvar/<var_id>")
def delvar(var_id):
    if check_user_cookie() == 'X': return logon()
    if check_session_cookie() == 'X': return mysessions()
    htdata = {'menu':'variables'} #this will be redefined in case we call varlist()

    if request.method == 'GET':
        db = opendb()
        sql = "delete from myvar where id = {}"
        sql = sql.format(var_id)
        cur = db.cursor()
        cur.execute(sql)
        db.commit()
        db.close()
        return varlist()

    htdata['session'] = check_session_cookie()
    return varlist()




@app.route("/logon", methods=["POST","GET"])
def logon():
    #is there a logon attempt?
    if request.method == 'POST':
        sql = "select id, name from users where name = '{}' and passwd = '{}'".format(request.form['login'],request.form['password'])
        db = opendb()
        cur = db.cursor()
        cur.execute(sql)
        user = cur.fetchone()
        db.close()
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
    db = opendb()
    val = fetch_single_value(db,sql)
    db.close()
    return make_response(val)

@app.route("/delsession/<id>")
def delete_session(id): #the ID is the auto_number of the table in this case
    if check_user_cookie() == 'X': return logon()
    db = opendb()
    cur = db.cursor()
    cur.execute("select session_id from sessions where id = {}".format(id))
    id_tx = cur.fetchone()[0]
    cur = db.cursor()
    cur.execute("delete from sessions where id = {}".format(id))
    cur.execute("delete from myvar where session_id = '{}'".format(id_tx))
    db.commit()
    #check how many sessions are left and decide to which page redirect
    sql = "select count(id) from sessions where user_id = '{}'" \
                            .format(check_user_cookie())
    numsessions = db.execute(sql).fetchone()[0]
    db.close()
    if numsessions == 0:
        return 'newsession'
    else:
        return 'mysessions'

@app.route("/updatedb", methods=["POST"])
def updatedb():
    db = opendb()
    sql = "update {} set {} = '{}' where id = {}".format(
                request.form['table'],request.form['field'],
                request.form['value'],request.form['rowid'])
    #print_debug(sql)
    try:
        cur = db.cursor()
        cur.execute(sql)
        db.commit()
        db.close()
        return request.form['itemid']
    except:
        db.close() #will also rollback
        return "err"


##EXTERNAL CALLS
# @app.route("/getlib/<session_id>/<js_file>")
# def getlibrary(session_id, js_file):
#     return render_template(js_file,data={'session_id': session_id})

# @app.route("/crossdomain.xml")
# def crossdomain():
#     return render_template("crossdomain.xml")

@app.route("/getvar/<session_id>/<varname>")
def getvar(session_id, varname):
    try:
        db = opendb()
        sql = "select varvalue from myvar where varname = '{}' and session_id = '{}'".format(varname,session_id)
        val = fetch_single_value(db,sql)
        db.close()
        return val
    except:
        return 'error!'

@app.route("/putvar/<session_id>/<varname>/<varvalue>")
def putvar(session_id, varname, varvalue):
    try:
        db = opendb()
        cur = db.cursor()
        sql = "update myvar set varvalue = '{}'  where varname = '{}' and session_id = '{}'".format(varvalue,varname,session_id)
        cur.execute(sql)
        db.commit()
        db.close()
        return 'saved'
    except:
        return 'error!'

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(pathjoin(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

#commented to run under pythonanywhere.com

if __name__ == "__main__":
    if exists("/home/lorenzopedrotti/www"):
        app.run(debug=False)
    else:
        app.run(host='192.168.1.30',debug=True)

