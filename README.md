# **Voice Weather Assistant 🎙️🌦️**  

Welcome to the **Voice Weather Assistant**! This smart application provides real-time weather updates using **voice commands** or text input, making weather forecasts more interactive and accessible.  

🚀 **Just ask, and it speaks back!** The assistant listens to your query, fetches the weather details, and **reads out the results** for a hands-free experience.  

---

## **Key Features 🎤✨**  

✅ **Voice-Powered Weather Updates** – Ask about the weather, and the assistant responds with spoken results.  
✅ **Text-Based Search** – Prefer typing? Simply enter the city name.  
✅ **Auto-Detection of Location** – Get weather updates instantly for your current location.  
✅ **Recent Searches History** – Quickly access previously searched locations.  
✅ **Smart NLP for Query Processing** – Recognizes city names even with typos using spell checking and Named Entity Recognition (NER).  
✅ **Real-Time Data Fetching** – Retrieves up-to-date weather reports from the **OpenWeather API**.  

---

## **Tech Stack 🛠️**  

- **🎙️ Voice Processing**: Web Speech API (for listening & reading responses)  
- **🌐 Frontend**: React  
- **🚀 Backend**: FastAPI  
- **📊 Database**: MongoDB Atlas  
- **📡 APIs**: OpenWeather API, Geolocation API  
- **🧠 NLP (Natural Language Processing)**: `spaCy`, `pyspellchecker`, `re (Regex)`  
- **📦 Deployment**: Docker  

---

## **How It Works 🎙️➡️🌍**  

1. **User Interaction**  
   - Speak into the microphone: "What’s the weather in Paris?"  
   - Or type: "Weather in New York."  

2. **NLP & Query Processing**  
   - The system **extracts the city name** using NLP.  
   - If there's a typo, it **auto-corrects** it.  
   - Validates the city name via **OpenWeather API**.  

3. **Fetching Weather Data**  
   - Queries OpenWeather API for real-time weather details.  

4. **Voice Response & Display**  
   - The app **reads the weather report aloud** for a seamless hands-free experience.  
   - The result is also displayed on-screen.  

---

## **Installation & Setup 🚀**  

### **Prerequisites**  
- **Docker** installed on your machine.  
- An API key from **[OpenWeather](https://openweathermap.org/api)**.  

### **Steps to Run the App**  

1️⃣ Clone the repository:  
```sh
git clone https://github.com/ananyasrinivasbhat/weather_voice_assistant.git
cd voice_weather_assistant
```

2️⃣ Add your OpenWeather API key:  
- Create a **.env** file inside the `backend` folder.  
- Add the following line:  
  ```sh
  OPENWEATHER_API_KEY=your_api_key_here
  ```

3️⃣ Build & run the app using Docker:  
```sh
docker-compose up --build
```

4️⃣ Access the app:  
- **Frontend**: Open **[http://localhost:5173](http://localhost:5173)**  
- **Backend API docs**: Open **[http://localhost:8000/docs](http://localhost:8000/docs)**  

---

## **Usage 🖥️**  

🎤 **Voice Input (Main Feature!)**  
- Click the **microphone icon**, ask a weather query, and **the assistant will speak back the response**!  

⌨️ **Text Input**  
- Type a city name, and the weather details will be displayed.  

📍 **Current Location Detection**  
- Automatically shows weather updates for your current location.  

📝 **Recent Searches**  
- View previously searched cities for quick access.  

---

## **Challenges & Solutions 🛠️**  

### **Challenge 1: Handling voice input & extracting accurate city names.**  
✅ **Solution**: Used **NLP techniques** like spell checking and Named Entity Recognition (NER).  

### **Challenge 2: Integrating multiple APIs (Voice, Geolocation, OpenWeather, MongoDB).**  
✅ **Solution**: Utilized **FastAPI’s asynchronous capabilities** for smooth API handling.  

---

## **Acknowledgments 🙏**  

🎉 Thanks to **OpenWeather** for providing real-time weather data.  
💙 Huge appreciation for **React, FastAPI, MongoDB, and Docker** for making this possible.  

---

## **Contact 📧**  

📌 **Name**: Ananya  
📌 **Email**: ananyas.bsc22@rvu.edu.in  

🚀 **Try it out and let your voice control the weather updates!** 🎙️🌦️

## ** video demo**
<video src="video.mp4" controls width="600"></video>
