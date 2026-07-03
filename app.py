#python -m venv venv ou python3 -m venv venv
#source -m venv venv
#pip install flask
from flask import *

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
