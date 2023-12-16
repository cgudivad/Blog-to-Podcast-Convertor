from flask import Flask, render_template, request, session
from mymodule import generate_conversation, generate_audio, generate_video, beautify

app = Flask(__name__)
app.config['STATIC_FOLDER'] = 'static'
app.secret_key = '89f093aef2f4bd1ea042bf47335fa5df8fcda06ceb77a93cbacfa558cc2bd07f'

@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":
        try:

            session['blog'] = request.form['blog']
            if session['blog'] == '':
                try:
                    session['blog'] = request.files["file"].read().decode('utf-8')
                except:
                    raise Exception('Invalid File Type. Only txt files are allowed')
            session['error_message'] = ''

            if request.form.get('action') == 'Generate Conversation':
                conversation = generate_conversation(0, session['blog'])
                session['script'] = conversation
                session['conversation'] = beautify('conversation', conversation)
                session['audioButtonFlag'] = True
                session['videoButtonFlag'] = True
                session['audioDisplayFlag'] = False
                session['videoDisplayFlag'] = False
                print('inside generate_conversation', session['conversation'])
                
            elif request.form.get('action') == 'Generate Audio':
                audio_filename = generate_audio(session['script'])
                audio_url = app.static_url_path + '/generated_audio/' + audio_filename
                session['audio_url'] = beautify('audio', audio_url)
                session['audioDisplayFlag'] = True
                print('audio_url', session['audio_url'])
                
            elif request.form.get('action') == 'Generate Video':
                summarized_conversation = generate_conversation(1, session['blog'])
                video_filename = generate_video(summarized_conversation)
                video_url = app.static_url_path + '/generated_video/' + video_filename
                session['video_url'] = beautify('video', video_url)
                session['videoDisplayFlag'] = True
                print('video_url', session['video_url'])
        except Exception as e:
            session['error_message'] = f"An error occurred: {str(e)}"  # Capture the error message
   
    return render_template("index.html",
                       blog=session.get('blog', ''),
                       conversation=session.get('conversation', ''),
                       audio_url=session.get('audio_url', ''),
                       video_url=session.get('video_url', ''),
                       audioButtonFlag=session.get('audioButtonFlag', False),
                       videoButtonFlag=session.get('videoButtonFlag', False),
                       audioDisplayFlag=session.get('audioDisplayFlag', False),
                       videoDisplayFlag=session.get('videoDisplayFlag', False),
                       error_message=session.get('error_message', ''))

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000)