import speech_recognition as sr

def main():
    r = sr.Recognizer()
    
    print('Say something... say \'exit\' to exit')
    
    while True:
        # Exception handling to handle exceptions at the runtime
        try:
            # Use the microphone as source for input
            with sr.Microphone() as source:
                # Wait for a second to let the recognizer
                # adjust the energy threshold based on
                # the surrounding noise level
                r.adjust_for_ambient_noise(source, duration=0.2)
                
                # Listens for the user's input
                out = r.listen(source)
                
                # Using google to recognize audio
                text = r.recognize_google(out).lower()

                if text == 'exit':
                    break
                
                print(text)
                
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
        except sr.UnknownValueError:
            print("unknown error occurred")


if __name__ == '__main__':
    main()