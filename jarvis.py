import speech_recognition as aa
import pyttsx3
import pywhatkit
import datetime
import webbrowser
import smtplib
import pyowm
import random
from email.mime.text import MIMEText
import requests
from bs4 import BeautifulSoup
from playsound import playsound

listener = aa.Recognizer()
machine = pyttsx3.init()

def talk(text):
    machine.say(text)
    machine.runAndWait()

def input_instruction():
    instruction = ""
    try:
        with aa.Microphone() as origin:
            print("Listening....")
            speech = listener.listen(origin)
        instruction = listener.recognize_google(speech)
        instruction = instruction.lower()
        if "jarvis" in instruction:
            instruction = instruction.replace('jarvis', '')
        print(instruction)
    except:
        pass
    return instruction

def play_Jarvis():
    while True:
        instruction = input_instruction()
        print(instruction)
        if "play" in instruction:
            song = instruction.replace('play',"")
            talk("Playing "+song)
            pywhatkit.playonyt(song)

        elif "time" in instruction:
            current_time = datetime.datetime.now().strftime('%I:%M %p')
            talk('Current time is ' + current_time)

        elif 'date' in instruction:
            current_date = datetime.datetime.now().strftime('%d /%m /%Y')
            talk("Today's date is " + current_date)

        elif 'how are you' in instruction:
            talk('I am fine, how about you')

        elif 'what is your name' in instruction:
            talk('I am Jarvis, What can I do for you?')

        elif 'search' in instruction:
            search_term = instruction.replace('search', '')
            talk(f"Searching for {search_term} on Google.")
            webbrowser.open_new_tab(f"https://www.google.com/search?q={search_term}")

        elif 'weather' in instruction:
            
            talk("enter city name")
            city = input()
            url = "https://www.google.com/search?q="+"weather"+city
            html = requests.get(url).content
            soup = BeautifulSoup(html, 'html.parser')
            temp = soup.find('div', attrs={'class': 'BNeawe iBp4i AP7Wnd'}).text
            str = soup.find('div', attrs={'class': 'BNeawe tAd8D AP7Wnd'}).text
            data = str.split('\n')
            time = data[0]
            sky = data[1]
            listdiv = soup.findAll('div', attrs={'class': 'BNeawe s3v9rd AP7Wnd'})
            strd = listdiv[5].text
            pos = strd.find('Wind')
            other_data = strd[pos:]

            print("Temperature is", temp)
            print("Time: ", time)
            print("Sky Description: ", sky)
            print(other_data)

            talk(f"The current temperature is {temp}")
            talk(f"The current time is {time}")
            talk(f"The current climate is {sky}")
            break  

        elif 'send email' in instruction:
            try:
                talk("What should I say?")
                content = input()
                talk("Who is the recipient?")
                recipient = input()  
                sender = "akamesh579@gmail.com"
                password = "cnrx izde xceq ydbn"
                msg = MIMEText(content)
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                    server.ehlo()
                    server.login(sender, password)
                    server.sendmail(sender, recipient, msg.as_string())
                    server.close()
                    talk("Email sent successfully.")
            except Exception as e:
                print(e)
                talk("Sorry. I am unable to send the email.")

        elif 'send whatsapp message' in instruction:
            try:
                talk("Whom should I send the message?")
                recipient_number = input()
                talk("What is the message?")
                message_content = input()
                
                talk("At what time should I send the message? Please specify the hour, minute, and meridiem.")
                talk("For example, you can give '1 30 PM' for 1:30 PM.")
                hour = int(input())
                minute = int(input())
                
                pywhatkit.sendwhatmsg(recipient_number,message_content,hour,minute)
                talk("Message sent successfully.")
            except Exception as e:
                print(e)
                talk("Sorry. I am unable to send the message.")

        elif 'sleep' in instruction:
            try:
                talk("Enter the time the alarm to be set")
                alarmHour= int(input())
                alarmMin = int (input())
                alarmAm = input()
                if alarmAm=="pm":
                    alarmHour+=12
                while True:
                    if alarmHour==datetime.now().hour and alarmMin==datetime.datetime.now().minute:
                        talk("ALARM !!!! GET UP IT'S TIME") 
                        playsound('wakeup-alarm-tone-21497.mp3')
                        break   
            except Exception as e:
                print(e)
                talk("Error occurred while setting the alarm.")

        elif 'set reminder' in instruction:
            talk("What should I remind you about?")
            reminder_text = input_instruction()
            talk("When should I remind you?")
            reminder_time = input_instruction()

        elif 'tell a joke' in instruction:
            jokes = [
                "Why don't scientists trust atoms? Because they make up everything!",
                "Parallel lines have so much in common. It's a shame they'll never meet.",
                "Why did the scarecrow win an award? Because he was outstanding in his field!",
                "I told my wife she was drawing her eyebrows too high. She looked surprised.",
                "I'm reading a book on anti-gravity. It's impossible to put down!",
            ]
            joke = random.choice(jokes)
            talk(joke)

        elif 'exit' in instruction:
            talk("Goodbye!")
            break  

play_Jarvis()
