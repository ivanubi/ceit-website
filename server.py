from flask import Flask
from flask import render_template, request, redirect, url_for, g
app = Flask("CEIT Development Server")
# En produccíon utiliza el CEIT Production Server.

# Routes

@app.route('/')
@app.route('/index')
@app.route('/index.html')
def index():
    file = open("static/python/last_post_caption.txt", "r")
    if file.mode == "r":
        instagram_text = repr(file.read())
        instagram_text = instagram_text.replace('\\n.\\n', ' <br> ')
        instagram_text = instagram_text.replace('\\n', ' <br> ')
        instagram_text = instagram_text.replace("'", '')
        return render_template("index.html", instagram_text=instagram_text)
    file.close()
    return render_template("index.html")

@app.route('/telematica')
@app.route('/telematica')
@app.route('/telematica.html')
def telematica():
    return render_template("telematica.html")

@app.route('/nosotros')
@app.route('/nosotros')
@app.route('/nosotros.html')
def nosotros():
    return render_template("nosotros.html")

@app.route('/contacto')
@app.route('/contacto')
@app.route('/contacto.html')
def contacto():
    return render_template("contacto.html")

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)
