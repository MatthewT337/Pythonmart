from flask import Flask, Blueprint
from static.views import main
from static.config import app

app.register_blueprint(main)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == "__main__":
    app.run(debug=True)
