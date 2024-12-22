# importing Flask and other modules
from flask import Flask, request, render_template

# Flask constructor
app = Flask(__name__)


# A decorator used to tell the application
# which URL is associated function
@app.route('/', methods=["GET", "POST"])
def gfg():
    if request.method == "POST":
        wg=""
        one = request.form.get("1")
        if one is not None:
            wg="agфы"
        text = request.form.get("Text")
        return render_template("index1.html",data="cipher"+text+wg)
    return render_template("index1.html",data="")
@app.route('/success', methods = ['POST'])
def success():
    if request.method == 'POST':
        f = request.files['file']
        f.save(f.filename)
        return render_template("Acknowledgement.html", name = f.filename)

if __name__ == '__main__':
    app.run()