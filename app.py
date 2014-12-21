from flask import Flask

from rhyme import Rhyme


app = Flask(__name__)


@app.route("/")
def index():
    return open('templates/index.html').read()

@app.route('/rhyme/<word>')
def rhyme(word):
    return str(Rhyme(word))


if __name__ == "__main__":
    app.debug = True
    app.run()
