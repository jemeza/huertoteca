from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/', methods=["POST", "GET"])
def home():
    if request.method == "POST":
        print(request.form["name"])
        print(request.form["email"])
        return render_template('home.html')
    return render_template('home.html')

if __name__ == '__main__':
   app.run()