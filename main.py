from flask import Flask, render_template, request
from controlCenter import ControlCenter
import datetime


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
        tiempo_actual = datetime.datetime.now().timestamp()
        CONTROL_CENTER.schedule.enterabs(tiempo_actual, 2, CONTROL_CENTER.evento_poner_show, kwargs = {"scheduled_time":None, "duracion":.25 * 60})
        return render_template('home.html')
    return render_template('home.html')

if __name__ == '__main__':
    
    app.run()
    

