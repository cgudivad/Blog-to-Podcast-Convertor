# Blog-to-Podcast-Convertor

This web application is designed to facilitate podcast-style content creation, including conversation generation, AI audio generation, and AI video generation derived from blog content.

**Guidelines on utilizing this web application effectively:**

Clone the repository and modify API keys in **api_keys.py** file and run **app.py** with python interpreter in order to start the web application.

**This is how the interface looks:**

![image](https://github.com/cgudivad/Blog-to-Podcast-Convertor/assets/126507537/10e2f753-b193-4445-a8d6-faf6ad0f0364)

**Step - 1:** You can paste the blog in the textbox or you can upload the blog from .txt file.

![image](https://github.com/cgudivad/Blog-to-Podcast-Convertor/assets/126507537/2ae06806-8300-4022-8d9c-25da8e3d1f45)

**Step - 2:** On clicking generate conversation button, system uses OpenAI API to convert the blog into conversation and populate it in the web apllication which looks like this:

![image](https://github.com/cgudivad/Blog-to-Podcast-Convertor/assets/126507537/5f835672-8547-447d-85ba-80f4c5ba255b)

**Step - 3:** On clicking generate audio button, system uses elevenLabs API to generate audio with two AI Voices from the conversation.

![image](https://github.com/cgudivad/Blog-to-Podcast-Convertor/assets/126507537/ff99d2f8-b7c7-4d47-afd7-8b3ec8fb3808)

**Step - 4:** On clicking generate video button, system uses Heygen API to summarize the blog into a short conversation video with two AI Avatars.

![image](https://github.com/cgudivad/Blog-to-Podcast-Convertor/assets/126507537/5ffb30a2-3778-485a-91db-4ed554437ac5)
