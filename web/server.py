from flask import Flask
import flask

app = Flask(__name__)

@app.route('/')
def index():
    return flask.jsonify(message='Flask test', num = 5)

if __name__ == '__main__':
    app.run()