from flask import Flask, render_template
app = Flask(__name__)
 
@app.route("/")
def index():
    return "<html><body><h1>Test site running under Flask</h1></body></html>"

@app.route("/testext")
def textext():
    return render_template("testext.js")

@app.route("/testget")
def testget(A,B):
    return "{} + {}".format(A,B)

#commented to run under pythonanywhere.com    
#if __name__ == "__main__":
#    app.run(host='0.0.0.0',debug=True) 
#    #app.run(host='10.115.202.155',debug=True)  