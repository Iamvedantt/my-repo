from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def hello():
    return "<h1>DevOps Pipeline Successful!</h1><p>Running on-prem VMs</p>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
