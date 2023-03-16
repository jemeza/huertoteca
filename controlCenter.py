import RPi.GPIO as GPIO
import pygame
import datetime
import time
import sched
import threading
from threading import Lock

DURACION = 60 # No tocar


##################################################################
##### LO QUE SE PUEDE MODIFICAR
##### NO TOCAR NADA FUERA DE ESTOS RENGLONES

MINUTOS = 3 # Cambiar aqui el numero de minutos

# (hora, minuto)

HORARIO = [
    (12, 30),
    (14, 0),
    (21, 20),
    (21, 24),
    (21, 26)
]


#################################################################


class ControlCenter():
    def __init__(self, luces=4, agua=27) -> None:
        self.luces=luces
        self.agua=agua
        
        pygame.mixer.init()
       
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.luces, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(self.agua, GPIO.OUT, initial=GPIO.HIGH)
        self.luces_on = False
        self.agua_on= False
        
        self.horario_en_pausa = False
        
        self.show_mutex = Lock()
        self.schedule = sched.scheduler(time.time, time.sleep)
        self.set_schedule()
        t1 = threading.Thread(target = self.schedule.run)
        t1.start()
        
    def evento_poner_show(self, scheduled_time, duracion=DURACION):
        if scheduled_time is not None:
            next_time = scheduled_time + datetime.timedelta(days=1)
            self.schedule.enterabs(next_time.timestamp(), 1, self.evento_poner_show, kwargs = {"scheduled_time":next_time})
        self.poner_show(duracion)
        
    def poner_show(self, duracion=DURACION):
        print("poniendo show")
        self.show_mutex.acquire()
        
        self.poner_agua()
        self.prender_luces()
        self.tocar_sonido(duracion)
        self.apagar_agua()
        self.apagar_luces()
        
        self.show_mutex.release()
        
    def prender_luces(self):
        if self.luces_on == False:
            self.toggle_luces()
    
    def apagar_luces(self):
        if self.luces_on == True:
            self.toggle_luces()
    
    def poner_agua(self):
        print("prender agua")
        if self.agua_on == False:
            self.toggle_agua()

    def apagar_agua(self):
        if self.agua_on == True:
            self.toggle_agua()
            
    def tocar_sonido(self, duracion=DURACION):
        pygame.mixer.music.load("sonido_lluvia_y_trueno.mp3")
        for _ in range(MINUTOS):
            pygame.mixer.music.play()
            time.sleep(duracion)
        pygame.mixer.music.stop()
            
    def toggle_luces(self):
        if self.luces_on == False:
            GPIO.output(self.luces, GPIO.LOW)
            self.luces_on = True
        else:
            GPIO.output(self.luces, GPIO.HIGH)
            self.luces_on = False
    
    def toggle_agua(self):
        print("in adding time")
        if self.agua_on == False:
            GPIO.output(self.agua, GPIO.LOW)
            print("on")
            self.agua_on = True
        else:
            GPIO.output(self.agua, GPIO.HIGH)
            print("off")
            self.agua_on = False
    
    
    
    
    
    def set_schedule(self):
        self.horas_programadas = self.gather_times()
        sched_queue = self.schedule.queue
        if len(sched_queue) != 0:
            return
        for time_of_event in self.horas_programadas:
            self.schedule.enterabs(time_of_event.timestamp(), 1, self.evento_poner_show, kwargs = {"scheduled_time":time_of_event})
        print(self.schedule.queue)
    
    def clear_schedule(self):
        sched_queue = self.schedule.queue
        if len(sched_queue) == 0:
            return
        for scheduled_event in sched_queue:
            self.schedule.cancel(scheduled_event)
        print("scheduled times cleared", self.schedule.queue)
        
    def print_schedule(self, scheduled_time):
        print("printing")
        next_time = scheduled_time+ datetime.timedelta(minutes=3)
        self.schedule.enterabs(next_time.timestamp(), 1, self.evento_poner_show, kwargs = {"scheduled_time":next_time})
    
    def gather_times(self) -> list:
        curr_time = datetime.datetime.now()
        time_array = []
        for hour, minute in HORARIO:
            if minute >= 60:
                minute %=60
            if hour >= 24:
                hour %= 24
            if hour < curr_time.hour  or (hour == curr_time.hour and minute < curr_time.minute):
                next_time = curr_time + datetime.timedelta(days=1)
                next_time = datetime.datetime(year=next_time.year, 
                                              month=next_time.month, 
                                              day=next_time.day, 
                                              hour=hour, 
                                              minute=minute)
            else:
                next_time = datetime.datetime(year=curr_time.year, 
                                              month=curr_time.month, 
                                              day=curr_time.day, 
                                              hour=hour, 
                                              minute=minute)
            time_array.append(next_time)
        return time_array

    
    