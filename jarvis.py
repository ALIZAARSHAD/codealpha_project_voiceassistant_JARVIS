import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os 
import requests
from bs4 import BeautifulSoup
import operator


API_KEY = '8b8c03542f87c6209e998ea4523219c6'


def get_weather(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
    response = requests.get(url)
    data = response.json()
    if data['cod'] == 200:
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        return f"The weather in {city} is {weather_description} with a temperature of {temperature} degrees Celsius."
    else:
        return "Sorry, unable to fetch weather information."


#for voices
engine = pyttsx3.init('sapi5')
voices= engine.getProperty('voices')
#print(voices[0].id)
engine.setProperty('voice', voices[0].id)



def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishme():
    hour=int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak('good morning')
    elif hour>=12 and hour<18:
        speak('good afternoon')
    else :
        speak('good evening')
    speak('hello i am jarvis how can i help you ')    
        
def meaning():
    meanby = query.split("by",1)
    try:
        soup= BeautifulSoup(requests.get(f"https://www.google.com//search?q={meanby[1]}+means").text , "html.parser")
        word = soup.find("div",class_="v9i61e")
        words =["noun", "exclamation"]
        word_list= word.text.split()
        speak(meanby[1] +" "+' '.join([i for i in word_list  if i not in words]))
        print(meanby[1] +" "+' '.join([i for i in word_list  if i not in words]))
        
        
    except:
        soup= BeautifulSoup(requests.get(f"https://www.google.com//search?q={meanby[1]}+means").text ,"html.parser")
        word = soup.find("div",class_="BNeawe s3v9rd AP7Wnd")
        words =["noun", "exclamation"]
        word_list= word.text.split()
        speak(meanby[1] +" "+' '.join([i for i in word_list  if i not in words]))
        print(meanby[1] +" "+' '.join([i for i in word_list  if i not in words]))
           

    r = sr.Recognizer()
    with sr.Microphone() as source:
        speak("what do you want to calculate")
        print("listening...")
        r.adjust_for_ambient_noise(source)
        r.pause_threshold = 1 
        audio = r.listen(source)

    mystring= r.recognize_google(audio, language="en-IN")
    print(mystring)
    
    def get_operator_fn(op):
        return{
            "+" : operator.add,
            "-" : operator.sub,
            "*" : operator.mul,
            "divide" : oeprator.truediv, 
        }[op]
    def eval_binary_expr(op1,oper,op2):
        op1,op2 =int(op1),int(op2)
        return get_operator_fn(oper)(op1,op2)
    try:
        result = eval_binary_expr(*(mystring.split()))
        speak(f"Your result is {result}")
        print("Result:", result)  # Print the result for debugging
    except Exception as e:
        speak("Sorry, I couldn't calculate that.")
    

def calculation():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        speak("What do you want to calculate?")
        print("Listening...")
        r.adjust_for_ambient_noise(source)
        r.pause_threshold = 1 
        audio = r.listen(source)

    try:
        mystring = r.recognize_google(audio, language="en-IN")
        print("Recognized input:", mystring)

        operators = {
            "+" : operator.add,
            "-" : operator.sub,
            "x" : operator.mul,
            "/" : operator.truediv,
        }

        op1, operator_symbol, op2 = mystring.split()
        result = operators[operator_symbol](float(op1), float(op2))
        speak(f"Your result is {result}")
        print("Result:", result)  # Print the result for debugging
    except Exception as e:
        print("Error:", e)
        speak("Sorry, I couldn't calculate that.")
                   

def takeCommand():
    """Takes user command from microphone and returns as string output."""
    # Create a recognizer object
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source)
        r.pause_threshold = 1 
        audio = r.listen(source)

    try:
        print("Recognizing...")
        # Specify the language parameter here
        query = r.recognize_google(audio, language="en-IN")
        print(f"User said: {query}")
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand what you said")
       
        return "None"
    except sr.RequestError as e:
        print(f"Error: {e}")
        return "None"

    return query
    

         

                    
if __name__ == '__main__':
    #speak('harry ')
    wishme()
    while True:
        
     query = takeCommand().lower()
     
     
     #logic for executing task based on query
     
     #searching results from wikipedia 
     if 'wikipedia' in query:
         speak('searching wikipedia...')
         query = query.replace("wikipedia","")
         results = wikipedia.summary(query, sentences=2)
         speak('according to wikipedia ')
         print(results)
         speak(results)
         
     #search any web    
     elif 'open youtube' in query:
         webbrowser.open("youtube.com")
         
     elif 'open google' in query:
         webbrowser.open("google.com")
         
     elif 'open facebook' in query:
             webbrowser.open("facebook.com")    
         
        
     #asking current time 
     elif'time' in query:
         strttime = datetime.datetime.now().strftime("%H:%M:%S")
         speak(f"sir the time is {strttime}")
         print(f"sir the time is {strttime}\n")
         
     #opening app
     elif'open code' in query :
         codepath = "C:\\Users\\KKT\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
         os.startfile(codepath)
         
     elif'open chrome' in query :
         codepath = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
         os.startfile(codepath) 
         
     elif'open file explorer' in query :
         codepath = "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"
         os.startfile(codepath) 
             
         
     #asking WEATHER
     elif 'weather' in query:
            speak('Sure, which city\'s weather would you like to know?')
            city = takeCommand().lower()
            weather_info = get_weather(city)
            speak(weather_info)  
            print(weather_info)     
         
     #DICTIONARY
     elif 'mean' in query:
         meaning()    
    
     #calculation
     elif 'calculate' in query:
         calculation()
    