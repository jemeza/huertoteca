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
        if request.form["submit_button"] == "tormenta":
            # CONTROL_CENTER.poner_show()
            print("poniendo show")
            if CONTROL_CENTER.horario_en_pausa:
                return render_template('tormenta_en_pausa.html')
            else: 
                return render_template('home.html')
        elif request.form["submit_button"] == "pausar":
            print("pausando")
            if CONTROL_CENTER.horario_en_pausa != True:
                # CONTROL_CENTER.clear_schedule()
                CONTROL_CENTER.horario_en_pausa = True
            return render_template('tormenta_en_pausa.html')
        
        elif request.form["submit_button"] == "continuar":
            print("continuando")
            if CONTROL_CENTER.horario_en_pausa:
                # CONTROL_CENTER.set_schedule()
                CONTROL_CENTER.horario_en_pausa = False
                pass
            return render_template('home.html')
        
    if CONTROL_CENTER.horario_en_pausa:
        return render_template('tormenta_en_pausa.html') 
    return render_template('home.html')

if __name__ == '__main__':
    
    app.run()
    

