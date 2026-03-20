# 🧠 Aizen – The AI-Powered Smart Assistant

Aizen is an AI-powered smart assistant inspired by **Jarvis** from *Iron Man*. It can understand voice commands, interact through speech, and control real-world devices like **smart door locks** using Arduino. Combining **Python**, **Flask**, and **Generative AI**, Aizen bridges intelligent software with physical automation.

---

## 🚀 Features

- 🎤 **Voice Recognition** – Listens and executes voice commands using `SpeechRecognition`.  
- 💬 **AI Conversations** – Integrated with **Gemini AI** for natural, human-like responses.  
- 🔐 **Smart Door Lock** – Controls door locking/unlocking through Arduino.  
- 🌐 **Flask API** – Enables communication between AI, Python backend, and hardware.  
- 🔁 **Real-Time Interaction** – Responds instantly with text-to-speech feedback.  
- 🧩 **Modular Design** – Organized Python modules for clean, scalable code.

---

## ⚙️ Tech Stack

| Component | Technology |
|------------|-------------|
| **Language** | Python, C++ (Arduino) |
| **Frameworks** | Flask, Arduino IDE |
| **AI** | Google Gemini API |
| **Libraries** | `speech_recognition`, `pyttsx3`, `requests`, `google-generativeai` |
| **Hardware** | Arduino UNO / ESP32, Servo Motor, Microphone, Speaker |

---

## 🛠️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/<your-username>/Aizen.git
cd Aizen

2. Install Dependencies
pip install -r requirements.txt

3. Configure API Key

Replace your Gemini API key in the configuration file:

genai.configure(api_key="YOUR_API_KEY")

4. Upload Arduino Code

Open Arduino IDE.

Upload the aizen_arduino.ino file to your board.

Connect the servo motor and ensure COM port is set correctly.

5. Run Flask Server
python app.py

6. Launch Aizen
python main.py

🧠 How It Works

Voice Input: Aizen continuously listens for commands.

AI Processing: Sends query to Gemini for intelligent responses.

Command Handling: Executes actions via Python modules or Flask endpoints.

Device Control: Arduino receives serial commands to perform actions (e.g., door lock).

🔮 Future Enhancements

🧠 Add contextual memory

📱 Mobile dashboard for remote control

🧭 Face recognition for access

⚡ IoT smart home integration

💡 Emotion-based responses

🤖 Author

Jarvis (Student Developer)
🚀 Passionate about AI, automation, and creating smart assistants.

📜 License

This project is open-source under the MIT License.


---
