# importing Flask and other modules
from transliterate import translit
from flask import Flask, request, render_template, Response

from Crypton import encrypt, decrypt

# Flask constructor
app = Flask(__name__)


# A decorator used to tell the application
# which URL is associated function
@app.route('/')
def home():
    return render_template("index1.html")


@app.route('/convert_text', methods=["POST"])
def convert_text():
    if request.method == "POST":
        input_text = ""
        encode_button = request.form.get("Encode")
        decode_button = request.form.get("Decode")
        text = request.form.get("Text")
        key = request.form.get("Text1")
        if encode_button is not None:
            input_text = encrypt(text, key)
        if decode_button is not None:
            input_text = decrypt(text, key)

        return render_template("index1.html", data=input_text, data1=key)
    return render_template("index1.html", data="", data1="")


@app.route('/convert_file', methods=["POST"])
def convert_file():
    file = request.files['file']
    key = request.form.get("Text2")
    if file:
        file_content = file.read()
        name_of_file = translit(file.filename, "ru", reversed=True)
        str_file_content = str(file_content)
        str_file_content = str_file_content[2:len(str(str_file_content)) - 1].encode('ascii').decode(
            'unicode_escape').encode('latin-1').decode('utf-8')
        encode_button = request.form.get("Encode")
        decode_button = request.form.get("Decode")
        if encode_button is not None:
            return Response(
                encrypt(str_file_content, key),
                mimetype='text/plain',
                headers={'Content-disposition': f"attachment; filename={"Encryted_" + name_of_file}"})
        if decode_button is not None:
            return Response(
                decrypt(str_file_content, key),
                mimetype='text/plain',
                headers={'Content-disposition': f"attachment; filename={"Decrypted_" + name_of_file}"})
    return render_template("index1.html", data2=key)


if __name__ == '__main__':
    app.run()
