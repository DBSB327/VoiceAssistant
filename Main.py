import speech_recognition as sr
import pyttsx3 
from fuzzywuzzy import fuzz 
import datetime
import webbrowser
from os import system
import random
import sys

nrem = ['Арго', 'Арг', 'Аргоу', 'ладно']

commands = ['текущее время', 'сейчас времени', 'который час', 'открой браузер', 'запусти браузер', 'пока', 'вырубись'
            ,'привет','здравствуй', 'выключи компьютер', 'выруби компьютер']

r = sr.Recognizer()
engine = pyttsx3.init()
text = ''
j = 0
num_task = 0

def talk(speech):
    print(speech)
    engine.say(speech)
    engine.runAndWait()

def fuzzy_recognizer(rec): 
    global j
    ans = ''
    for i in range(len(commands)):
        k = fuzz.ratio(rec, commands[i])   
        if(k > 70) & (k > j):
            ans = commands[i]
            j = k
    return str(ans)

def clear_task():
    global text
    for i in nrem:
        text = text.replace(i, '').strip()
    text = text.replace('','').strip()

def listen(): 
    global text
    text = ''
    with sr.Microphone() as source:
        print("Скажите что-нибудь...")
        r.adjust_for_ambient_noise(source) 
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio, language="ru-RU").lower()
        except sr.UnknownValueError:
            pass
    system('cls')
    clear_task()
    return text

def cmd_init():
    global text, num_task
    text = fuzzy_recognizer(text)
    print(text)
    if text in cmds:
        if text not in ('пока', 'привет', 'который час', 'сейчас времени', 'который час', 'здравствуй'):
            k = ['Секунду', 'Сейчас сделаю', 'Выполняю']
            talk(random.choice(k))
        cmds[text]()
    elif text == '':
        print('Команда не распознана')
    num_task += 1
    if num_task % 10 == 0:
        talk('У вас есть еще вопросы?')
    engine.runAndWait()
    engine.stop

def time():
    now = datetime.datetime.now()
    talk("Сейчас " + str(now.hour) + ":" + str(now.minute))

def open_brows():
    webbrowser.open('https://google.com')
    talk('Браузер открыт!')

def quite():
    x = ['Пакед', 'бб', 'До скорого!']
    talk(random.choice(x))
    engine.stop()
    system('cls')
    sys.exit(0)
 
def shut():
    global text
    talk('Подтвердите действие!')
    text = listen()
    print(text)
    if fuzz.ratio(text, 'подтвердить') > 70 or fuzz.ratio(text, 'подтверждаю') > 70:
        talk('Дейтсвие подтверждено')
        system('shutdown /s /f /t 10')
        quite()
    elif fuzz.ratio(text, 'отмена') > 60:
        talk('Действие не подтверждено')
    else:
        talk('Действие не подтверждено')

def hello():
    k = ['Ку!', 'Здравстуйте!', 'Привет!']
    talk(random.choice(k))

cmds = {
     'текущее время': time, 'сейчас время': time, 'который час': time,
     'открой браузер': open_brows,'запусти браузер': open_brows,
     'пока': quite, 'отключись': quite,
     'привет': hello, 'здравстуй': hello,
     'выключи компьютер': shut, 'выруби компьютер': shut,
} 

def main(): 
    global text, j
    try:
        listen()
        if text != '':
            cmd_init()
            j = 0
    except UnboundLocalError:
        pass
    except NameError:
        pass
    except TypeError:
        pass

while True: 
    main()
