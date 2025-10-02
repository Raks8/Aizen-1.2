from flask import Flask, request, jsonify
from flask_cors import CORS
from functions import *
from commands import *
import webbrowser

app = Flask(__name__)
CORS(app)  # Allow HTML to connect from browser

@app.route('/api/command', methods=['POST'])
def process_command():
    data = request.json
    query = data.get('query', '').lower()
    
    # Website commands
    sites = [
        ["youtube", "https://www.youtube.com"],
        ["wikipedia", "https://www.wikipedia.com"],
        ["google", "https://www.google.com"]
    ]
    
    for site in sites:
        if f"open {site[0]}" in query:
            webbrowser.open(site[1])
            return jsonify({
                'success': True,
                'response': f"Opening {site[0]}...",
                'action': 'open_website',
                'url': site[1]
            })
    
    # Music command
    if any(phrase in query for phrase in music_triggers):
        return jsonify({
            'success': True,
            'response': 'Playing music...',
            'action': 'play_music'
        })
    
    # Time command
    if any(phrase in query for phrase in time_triggers):
        hour = datetime.datetime.now().strftime("%H")
        min = datetime.datetime.now().strftime("%M")
        response = f"Sir time is {hour} bajke {min} minutes"
        say(response)
        return jsonify({
            'success': True,
            'response': response,
            'action': 'time'
        })
    
    # VS Code command
    if any(phrase in query for phrase in vscode_triggers):
        say("Opening VS Code")
        file_path = "E:\\Microsoft VS Code\\Code.exe"
        try:
            os.startfile(file_path)
            return jsonify({
                'success': True,
                'response': 'Opening VS Code...',
                'action': 'open_vscode'
            })
        except:
            return jsonify({
                'success': False,
                'response': 'Could not open VS Code',
                'action': 'error'
            })
    
    # PyCharm command
    if any(phrase in query for phrase in pycharm_triggers):
        say("Opening PyCharm")
        file_path = "C:\\Program Files\\JetBrains\\PyCharm Community Edition 2024.2.3\\bin\\pycharm64.exe"
        try:
            os.startfile(file_path)
            return jsonify({
                'success': True,
                'response': 'Opening PyCharm...',
                'action': 'open_pycharm'
            })
        except:
            return jsonify({
                'success': False,
                'response': 'Could not open PyCharm',
                'action': 'error'
            })
    
    # Weather command
    if any(phrase in query for phrase in temperature_triggers):
        say("Collecting data from web")
        API_KEY = "9b3990207e3d3a8fd233c1c38cfb2164"
        city = "Buxwaha"
        weather = get_weather(city, API_KEY)
        
        if weather:
            response = f"Location: {weather['city']}, {weather['country']}\n"
            response += f"Temperature: {weather['temperature']}°C\n"
            response += f"Humidity: {weather['humidity']}%\n"
            response += f"Wind Speed: {weather['wind_speed']} m/s\n"
            response += f"Weather: {weather['description']}"
            
            return jsonify({
                'success': True,
                'response': response,
                'action': 'weather',
                'data': weather
            })
        else:
            return jsonify({
                'success': False,
                'response': 'Could not fetch weather data',
                'action': 'error'
            })
    
    # News command
    if any(phrase in query for phrase in headlines_triggers):
        say("Collecting data from web")
        API_KEY = "5b2ac3f42e704252a3483d9c2e5382e5"
        country = "in"
        articles = get_headlines(API_KEY, country)
        
        if articles:
            response = "Top Headlines:\n"
            for i, article in enumerate(articles[:5], 1):
                response += f"{i}. {article['title']}\n"
            
            return jsonify({
                'success': True,
                'response': response,
                'action': 'news',
                'data': articles[:5]
            })
        else:
            return jsonify({
                'success': False,
                'response': 'Could not fetch news',
                'action': 'error'
            })
    
    # YouTube command
    if any(phrase in query for phrase in youtube_triggers):
        video = query.replace("play", "").replace("on youtube", "").strip()
        play_youtube_video(video)
        return jsonify({
            'success': True,
            'response': f"Playing {video} on YouTube...",
            'action': 'youtube',
            'video': video
        })
    # Door command
    if any(phrase in query for phrase in door_triggers):
        try:
            ser = serial.Serial('COM3', 9600, timeout=1)
            time.sleep(2)
            ser.write(b'1')
            time.sleep(2)
            ser.write(b'0')
            ser.close()
            return jsonify({
                'success': True,
                'response': 'Door opened!',
                'action': 'door'
            })
        except:
            return jsonify({
                'success': False,
                'response': 'Could not connect to door',
                'action': 'error'
            })
    
# Fallback: Send to Gemini only if query is not empty
    if query.strip():  # only proceed if user actually said something
        try:
            response = ai_gemini(query)
            return jsonify({
            'success': True,
            'response': response if response else 'I could not process that request.',
            'action': 'ai_fallback'
        })
        except Exception as e:
            return jsonify({
            'success': False,
            'response': f'Command not recognized. AI Error: {str(e)}',
            'action': 'error'
        })
    else:
        # Empty query means frontend ping or silence → no Gemini call
        return jsonify({
        'success': False,
        'response': 'Awaiting your command...',
        'action': 'no_input'
    })


@app.route('/api/speak', methods=['POST'])
def speak_text():
    data = request.json
    text = data.get('text', '')
    say(text)
    return jsonify({'success': True})

@app.route('/api/listen', methods=['GET'])
def listen():
    query = takeCommand()
    return jsonify({
        'success': True,
        'query': query
    })

if __name__ == '__main__':
    print("🚀 Jarvis Flask Server Started!")
    print("📡 Open your HTML file in browser")
    print("🔗 Server running on http://localhost:5000")
    app.run(debug=True, port=5000)