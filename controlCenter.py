import RPi.GPIO as GPIO
# from playsound import playsound
import datetime
import time
import sched
import threading

DURACION = .25 * 60 #3 * 60

class ControlCenter():
    def __init__(self, luces=4, agua=27, horas_programadas = None) -> None:
        if horas_programadas is None: 
            horas_programadas = []
            ahora = datetime.datetime.now()
            for i in range(1, 4):
                horas_programadas.append(ahora.minute + i)
        self.luces=luces
        self.agua=agua
        self.horas_programadas = self.gather_times(horas_programadas)
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.luces, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(self.agua, GPIO.OUT, initial=GPIO.HIGH)
        self.luces_on = False
        self.agua_on= False
        
        self.schedule = sched.scheduler(time.time, time.sleep)
        self.set_schedule()
        t1 = threading.Thread(target = self.schedule.run)
        t1.start()
        
    def evento_poner_show(self, scheduled_time, duracion=DURACION):
        next_time = scheduled_time + datetime.timedelta(minutes=3)
        if scheduled_time is not None:
            self.schedule.enterabs(next_time.timestamp(), 1, self.evento_poner_show, kwargs = {"scheduled_time":next_time})
        self.poner_show(duracion)
        
    def poner_show(self, duracion=DURACION):
        print("poniendo show")
        self.prender_agua()
        self.prender_luces()
        self.tocar_sonido(duracion)
        self.apagar_agua()
        self.apagar_luces()
        
    def prender_luces(self):
        if self.luces_on == False:
            self.toggle_luces()
    
    def apagar_luces(self):
        if self.luces_on == True:
            self.toggle_luces()
    
    def prender_agua(self):
        if self.agua == False:
            self.toggle_agua()

    def apagar_agua(self):
        if self.agua == True:
            self.toggle_agua()
            
    def tocar_sonido(self, duracion=DURACION):
        time.sleep(duracion)
        # playsound('audio.mp3')
            
    def toggle_luces(self):
        if self.luces_on == False:
            GPIO.output(self.luces, GPIO.LOW)
            self.luces_on = True
        else:
            GPIO.output(self.luces, GPIO.HIGH)
            self.luces_on = False
    
    def toggle_agua(self):
        if self.agua_on == False:
            GPIO.output(self.agua, GPIO.LOW)
            print("on")
            self.agua_on = True
        else:
            GPIO.output(self.agua, GPIO.HIGH)
            print("off")
            self.agua_on = False
    
    
    
    
    
    def set_schedule(self):
        for time_of_event in self.horas_programadas:
            self.schedule.enterabs(time_of_event.timestamp(), 1, self.evento_poner_show, kwargs = {"scheduled_time":time_of_event})
        
    def print_schedule(self, scheduled_time):
        print("printing")
        next_time = scheduled_time+ datetime.timedelta(minutes=3)
        self.schedule.enterabs(next_time.timestamp(), 1, self.evento_poner_show, kwargs = {"scheduled_time":next_time})
    
    def gather_times(self, times) -> list:
        curr_time = datetime.datetime.now()
        time_array = []
        for minute in times:
            if minute > 60:
                minute %=60
            if minute < curr_time.minute:
                #schedule for the next day
                # add one day
                # TODO: change for prod
                next_time = curr_time + datetime.timedelta(days=1)
                next_time = datetime.datetime(year=next_time.year, 
                                              month=next_time.month, 
                                              day=next_time.day, 
                                              hour=next_time.hour, 
                                              minute=minute)
            else:
                next_time = datetime.datetime(year=curr_time.year, 
                                              month=curr_time.month, 
                                              day=curr_time.day, 
                                              hour=curr_time.hour, 
                                              minute=minute)
            time_array.append(next_time)
        return time_array

    
    