from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def opendb():
    return sqlite3.connect(app.root_path + '/flask.db')
 
@app.route("/")
def index():
    #conn = sqlite3.connect(app.root_path + '/flask.db')
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


    
##The next TWO functions are used to deliver the scratch extension
@app.route("/testext")
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
#    app.run(host='0.0.0.0',debug=True)     