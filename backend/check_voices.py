import pyttsx3

engine = pyttsx3.init()
voices = engine.getProperty("voices")

print("Available TTS Voices on System:")
print("=" * 60)
for i, v in enumerate(voices):
    print(f"\n{i+1}. Voice ID: {v.id}")
    print(f"   Name: {v.name}")
    print(f'   Languages: {getattr(v, "languages", "N/A")}')
    print(f'   Gender: {getattr(v, "gender", "N/A")}')
    print(f'   Age: {getattr(v, "age", "N/A")}')
print("=" * 60)
