from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)
 
@app.route("/")
def index():
    #conn = sqlite3.connect('/home/lorenzopedrotti/flask.db')
    htdata = {'menu':'main'}
    return render_template("index.html", data = htdata)

@app.route("/i2")
def index2():
    htdata = {'menu':'super'}
    return render_template("index.html", data = htdata)

@app.route("/S4")
def super_quattro():
    htdata = {'menu':'super', 'active':'#CMD-S4'}
    return render_template("S4.html", data = htdata)
    
    
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