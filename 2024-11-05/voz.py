import speech_recognition as sr

r = sr.Recognizer()
while True:
    with sr.Microphone(device_index=2) as source:
        print("Hola, soy asistente por voz: ")
        audio = r.listen(source)
        try: 
            text = r.recognize_google(audio, language="es-ES")
            print("Has dicho: {}".format(text))
            print(text)
        except:
            print("No te he entendido")