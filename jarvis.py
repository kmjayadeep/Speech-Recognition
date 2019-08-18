# Enter in bash
# export GOOGLE_APPLICATION_CREDENTIALS=credentials.json

import pyttsx3
import speech_recognition as sr
import datetime
from datetime import date

DIALOGFLOW_PROJECT_ID = 'jarvis-ndaali'
DIALOGFLOW_LANGUAGE_CODE = 'en-US'
SESSION_ID = 'current-user-id'

recognizer = sr.Recognizer()
recognizer.pause_threshold=1
engine = pyttsx3.init()
voices = engine.getProperty('voices')

def find_voice(voices):
    for voice in voices:
        if('en_GB' in voice.languages):
            return voice
    return voices[0]

engine.setProperty('voice', find_voice(voices))

def detect_intent_texts(text):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""

    import dialogflow_v2 as dialogflow
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
    print('Session path: {}\n'.format(session))

    
    text_input = dialogflow.types.TextInput(
        text=text, language_code=DIALOGFLOW_LANGUAGE_CODE)

    query_input = dialogflow.types.QueryInput(text=text_input)

    return session_client.detect_intent(
        session=session, query_input=query_input)

    
def greetMe():
    currentH = int(datetime.datetime.now().hour)
    if currentH >= 0 and currentH < 12:
        speak('Good Morning!')
    if currentH >= 12 and currentH < 16:
        speak('Good Afternoon!')
    if currentH >= 16 and currentH != 0:
        speak('Good Evening!')


def speak(audio):
    print('Computer: ' + audio)
    engine.say(audio)
    engine.runAndWait()


def getCommand():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print('Listening...')
        audio=recognizer.listen(source)

    try:
        query = recognizer.recognize_google(audio)
        print ('User: ' + query + '\n')	

    except sr.UnknownValueError:
        speak('Sorry! I didn\'t get that. Try typing the command!')
        query = str(input('Command: '))

    return query


if __name__ == '__main__':
    greetMe()
    speak('Hello, I am your lady assistant "Sophie..."')
    speak('How may I help you?')
    while True:
        command = getCommand()
        if 'nothing' in command or 'stop' in command or 'bye' in command:
            speak('okay')
            speak('Bye Bye, have a good day.')
            break;

        response = detect_intent_texts(command)

        print(response)

        print('=' * 20)
        print('Query text: {}'.format(response.query_result.query_text))
        print('Detected intent: {} (confidence: {})\n'.format(
            response.query_result.intent.display_name,
            response.query_result.intent_detection_confidence))
        print('Fulfillment text: {}\n'.format(
            response.query_result.fulfillment_text))
