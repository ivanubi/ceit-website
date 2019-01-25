from flask import Flask
from flask import render_template, request, redirect, url_for, g
import py_compile

app = Flask("CEIT Web Server")

# Routes:

@app.route('/')
@app.route('/index')
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
def telematica():
    return render_template("telematica.html")


@app.route('/nosotros')
def nosotros():
    return render_template("nosotros.html")


@app.route('/contacto')
def contacto():
    return render_template("contacto.html")

@app.errorhandler(404)
def page_not_found(error):
    return render_template('index.html')

exec(open("./static/python/instagram-scraper.py").read())

if __name__ == '__main__':
    app.run()
