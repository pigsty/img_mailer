from flask import Flask
app = Flask(__name__)
app.config_from_pyfile("/config/mailer.cfg")


@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run()
