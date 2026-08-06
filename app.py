from flask import Flask, redirect

app = Flask(__name__)

@app.route("/")
def home():
    return ('teste')

if __name__ == "__main__":
    app.run(port=5001)