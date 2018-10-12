from flask import Flask


app = Flask(__name__)


@app.route("/")
def home_page():
    return "Enes, Ali ve Perit!"


if __name__ == "__main__":
    app.run()
