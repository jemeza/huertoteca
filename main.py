from flask import Flask, render_template, request
from controlCenter import ControlCenter


PIN_DE_LUCES = 4
PIN_DE_AGUA = 27



CONTROL_CENTER = ControlCenter(PIN_DE_LUCES, PIN_DE_AGUA)
# SCHEDULER = Scheduler()
app = Flask(__name__)




@app.route('/', methods=["POST", "GET"])
def home():
    if request.method == "POST":
        print(request.form["name"])
        print(request.form["email"])
        CONTROL_CENTER.poner_show()
        return render_template('home.html')
    return render_template('home.html')

if __name__ == '__main__':
    
    app.run()
    

