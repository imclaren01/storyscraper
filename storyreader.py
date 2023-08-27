from gtts import gTTS as gt
import json


with open("stories/stories.json", "r") as f:
    data = json.load(f)

for story in data:

    tts = gt(story, lang="en", tld="co.uk")
    tts.save(f"audiostories/{data[story]['Title'][:15]}.mp3")


