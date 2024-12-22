from flask import Flask, request, render_template
app = Flask(__name__)
test = "1234"
def foo(data):
   return data+"red"
# @app.route("/")
# def index():
#    return render_template("index1.html", data = test)
@app.route('/', methods =["GET", "POST"])
def gfg():
    if request.method == "POST":
        # getting input with name = fname in HTML form
        first_name = request.form.get("fname")
    return render_template("index1.html")
if __name__ == '__main__':
   app.run(debug = True)