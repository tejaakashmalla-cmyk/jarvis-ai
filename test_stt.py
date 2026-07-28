from voice.stt import JarvisSTT

stt = JarvisSTT()

text = stt.listen()

print()

print("You Said:")

print(text)