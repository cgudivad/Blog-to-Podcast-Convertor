import requests
import re
from openai import OpenAI
from datetime import datetime
import json
import urllib.request
import api_keys
import time

client = OpenAI(
    api_key = api_keys.open_AI_API_key
)

prompts = ["Transform the following blog into a conversation between two persons named Adam and Jennifer, making it sound natural by incorporating non-speech sounds like hmm, hm!, ummm, huh?, ouch!, wow!, awww!, ahem!, eh?, eww, oops, phew!, yahoo!, hmph, brrr as appropriate.", "Could you please summarize the blog provided into a 45-second conversation between two persons named Adam and Jennifer. Each character should not have more than 5 dialogues. Make it sound natural, and include non-speech sounds to add authenticity to the dialogue. Use sounds like 'hmm,' 'ummm,' 'ouch,' 'wow,' 'awww,' 'ahem,' 'eh,' 'eww,' 'oops,' 'phew,' 'yahoo,' 'hmph,' and 'brrr' as appropriate."]

def generate_conversation(p_index, content):

    model = api_keys.open_AI_GPT_model

    chat_completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system",
            "content": prompts[p_index]},
            {"role": "user",
            "content": "Blog: " + content}
        ]
    )

    conversation = chat_completion.choices[0].message.content
    conversation = conversation.strip().split("\n\n")
    conversation = [re.sub(r'\([^)]*\)|\[[^]]*\]|\*[^*]*\*', '', convo) for convo in conversation if re.sub(r'\([^)]*\)|\[[^]]*\]|\*[^*]*\*', '', convo) not in ['Adam: ', 'Jennifer: ']]
    print(prompts[p_index], ':', conversation)

    return conversation

    # return ["Mark: Hey Sarah, what's up? You look a bit down.", "Sarah: Oh, Mark. I've been thinking about my love life lately."]


def generate_audio(script):

    audio_file_name = 'audio_'+str(datetime.now().strftime("%Y-%m-%d %H-%M-%S"))+".mp3"

    chunk_size = 1024
    url = "https://api.elevenlabs.io/v1/text-to-speech/"
    speaker_lookup = {"Adam": "IKne3meq5aSn9XLyUdCD", "Jennifer": "EXAVITQu4vr4xnSDxMaL"}

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": api_keys.elevenlabs_API_key
    }

    with open('static\generated_audio\\'+audio_file_name, 'wb') as f:

        for sentence in script:
            try:
                person, dialogue = sentence.strip().split(": ", 1)
            except:
                continue
            data = {
                "text": dialogue,
                "model_id": "eleven_multilingual_v2",
                "voice_settings": {
                    "stability": 0.2,
                    "similarity_boost": 0.65
                }
            }

            response = requests.post(url + speaker_lookup[person], json=data, headers=headers)

            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)

    return audio_file_name

    # return '2023-11-01 18-34-40.mp3'

def generate_video(conversation):

    video_file_name = 'video_'+str(datetime.now().strftime("%Y-%m-%d %H-%M-%S"))+".mp4"
    url = "https://api.heygen.com/v2/video/generate"
    status_url = "https://api.heygen.com/v1/video_status.get?video_id="

    avatars = {
        "Adam": {"avatar_id": "Mido-lite-20221128", "scale": 3.2, "voice_id": "d86b76fb74ae4121b7dc13de81daf4ed"},
        "Jennifer": {"avatar_id": "Vlada-lite-20221129", "scale": 1, "voice_id": "d67ce67060fe4d9b99ab7d968ec230b0"}
    }

    video_inputs = []
    scene_index = 0

    for sentence in conversation:
        try:
            person, dialogue = sentence.strip().split(": ", 1)
        except:
            continue
        scene = {
            "character": {
                "type": "avatar",
                "avatar_id": avatars[person]["avatar_id"],
                "scale": avatars[person]["scale"],
                "avatar_style": "normal"
            },
            "voice": {
                "type": "text",
                "input_text": dialogue,
                "voice_id": avatars[person]["voice_id"]
            }
        }
        video_inputs.append(scene)
        if scene_index >= 9:
            break
        else:
            scene_index += 1    

    payload = {
        "test": False,
        "caption": False,
        "video_inputs": video_inputs,
        "dimension": {
            "width": 1080,
            "height": 1920
        }
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "x-api-key": api_keys.heygen_API_key
    }

    response = requests.post(url, json=payload, headers=headers)

    response = json.loads(response.text)

    print(response)

    video_id = response['data']['video_id']

    status = "processing"

    while status != "completed" and status != "failed":

        response = requests.get(status_url + video_id, headers=headers)
        response = json.loads(response.text)
        status = response['data']['status']
        if status == "completed":
            video_url = response['data']['video_url']
        time.sleep(10)

    urllib.request.urlretrieve(video_url, 'static\generated_video\\'+video_file_name)

    return video_file_name

    # return "video_2023-11-01 21-17-28.mp4"

def beautify(flag, content):

    html_content = ""
    colors = {"Adam": "rgb(26, 144, 187)", "Jennifer": "rgb(6, 148, 49)"}

    if flag == "conversation":

        html_content = """<div class="card chat-box">
        <div class="card-header">Conversation Between <b style="color: rgb(26, 144, 187);">Adam</b> and <b style="color: rgb(6, 148, 49);">Jennifer</b></div>
        <div class="card-body chat-messages">"""

        for sentence in content:
            person, dialogue = sentence.strip().split(": ", 1)
            html_content += """<div class="message recipient"> <small style="color: """ + colors[person] + """;"><b>""" + person + """</b></small><p>""" + dialogue + """</p></div>"""
            
        html_content += """</div></div>"""

    elif flag == "audio":

        html_content = """<audio controls="controls" class="w-100">
                    <source src=\"""" + content + """" type="audio/mp3">
                    Your browser does not support the audio tag.
                </audio>"""

    elif flag == "video":

        html_content = """<video width="360" height="640" controls class="w-100">
                    <source src=\"""" + content + """" type="video/mp4">
                    Your browser does not support the video tag.
                </video>"""

    return html_content