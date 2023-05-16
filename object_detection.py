import RPi.GPIO as GPIO         # подключение библиотеки для работы с контактами ввода/вывода
import time                     # подключение библиотеки для работы с задержками

GPIO.setwarnings(False)         # отключаем показ любых предупреждений
GPIO.setmode(GPIO.BCM)          # мы будем программировать контакты GPIO по их функциональным номерам (BCM)
TRIG = 17
ECHO = 27
led = 22
m11 = 16
m12 = 12
m21 = 21
m22 = 20
GPIO.setup(TRIG, GPIO.OUT)        # инициализируем GPIO TRIG в качестве цифрового выхода
GPIO.setup(ECHO, GPIO.IN)         # инициализируем GPIO ECHO в качестве цифрового входа
GPIO.setup(led, GPIO.OUT)
GPIO.setup(m11, GPIO.OUT)
GPIO.setup(m12, GPIO.OUT)
GPIO.setup(m21, GPIO.OUT)
GPIO.setup(m22, GPIO.OUT)
GPIO.output(led, 1)
time.sleep(5)

def stop():
    print("СТОП")
    GPIO.output(m11, 0)
    GPIO.output(m12, 0)
    GPIO.output(m21, 0)
    GPIO.output(m22, 0)

def forward():
    GPIO.output(m11, 1)
    GPIO.output(m12, 0)
    GPIO.output(m21, 1)
    GPIO.output(m22, 0)
    print("Вперед")

def back():
    GPIO.output(m11, 0)
    GPIO.output(m12, 1)
    GPIO.output(m21, 0)
    GPIO.output(m22, 1)
    print("Назад")

def left():
    GPIO.output(m11, 0)
    GPIO.output(m12, 0)
    GPIO.output(m21, 1)
    GPIO.output(m22, 0)
    print("Влево")

def right():
    GPIO.output(m11, 1)
    GPIO.output(m12, 0)
    GPIO.output(m21, 0)
    GPIO.output(m22, 0)
    print("Вправо")

stop()
count = 0

while True:
 i = 0
 avgDistance = 0

 for i in range(5):
  GPIO.output(TRIG, False)                   # устанавливаем на TRIG уровень LOW
  time.sleep(0.1)
  GPIO.output(TRIG, True)                    # устанавливаем на TRIG уровень HIGH
  time.sleep(0.00001)
  GPIO.output(TRIG, False)                   # устанавливаем на TRIG уровень LOW

  while GPIO.input(ECHO) == 0:                 # проверяем что на ECHO уровень LOW
       GPIO.output(led, False)
  pulse_start = time.time()

  while GPIO.input(ECHO) == 1:                 # проверяем что на ECHO уровень HIGH
       GPIO.output(led, False)
  pulse_end = time.time()
  pulse_duration = pulse_end - pulse_start   # время между передачей и приемом ультразвуковой волны
  distance = pulse_duration * 17150          # умножаем это время на 17150 (34300/2), чтобы рассчитать расстояние
  distance = round(distance, 2)               # округляем до двух точек после запятой
  avgDistance = avgDistance + distance
 avgDistance = avgDistance/5
 print(avgDistance)
 flag = 0

 if avgDistance < 15:                        # проверяем меньше ли 15 см расстояние до препятствия
    count = count+1
    stop()
    time.sleep(1)
    back()
    time.sleep(1.5)
    if (count % 3 == 1) & (flag == 0):
     right()
     flag = 1
    else:
     left()
     flag = 0
    time.sleep(1.5)
    stop()
    time.sleep(1)
 else:
    forward()
    flag = 0