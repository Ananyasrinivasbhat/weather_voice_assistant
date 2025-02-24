import React, { useState, useEffect } from "react";
import '../styles/animations.css';
import '../styles/global.css';
import { WeatherData } from "../hooks/useweather";


interface WeatherCardProps {
  data?: WeatherData;
}

const getWeatherEmoji = (condition: string) => {
  const lowerCondition = condition.toLowerCase();
  if (lowerCondition.includes("sun")) return "☀️";
  if (lowerCondition.includes("cloud") && lowerCondition.includes("sun")) return "🌤️";
  if (lowerCondition.includes("cloud")) return "☁️";
  if (lowerCondition.includes("rain")) return "🌧️";
  if (lowerCondition.includes("storm")) return "⛈️";
  return "🌍"; // Default icon
};

const speakWeather = (data: WeatherData) => {
  if (!data || !("speechSynthesis" in window)) return;

  const speech = new SpeechSynthesisUtterance();
  speech.text = `The weather in ${data.city} is ${data.condition}. The temperature is ${data.temperature} degrees Celsius, with a humidity of ${data.humidity} percent and wind speed of ${data.windSpeed} meters per second.`;

  const voices = window.speechSynthesis.getVoices();
  const voice = voices.find((v) => v.lang === "en-US");
  if (voice) speech.voice = voice;

  window.speechSynthesis.speak(speech);
};

const WeatherCard: React.FC<WeatherCardProps> = ({ data }) => {
  const [flipped, setFlipped] = useState(false);

  useEffect(() => {
    if (data) speakWeather(data);
  }, [data]);

  if (!data) {
    return <p className="text-center text-red-500 text-lg">No weather data available.</p>;
  }

  return (
    <div className="weather-card perspective-1000" onClick={() => setFlipped(!flipped)}>
      <div className={`weather-card-inner transform-style-preserve-3d ${flipped ? "rotate-y-180" : ""}`}>
        {/* Front Side */}
        <div className="weather-card-front bg-white p-4">
          <h2 className="text-xl font-bold">{data.city}</h2>
          <div className="text-5xl">{getWeatherEmoji(data.condition)}</div>
          <p className="text-lg">{data.temperature}°C</p>
        </div>

        {/* Back Side */}
        <div className="weather-card-back bg-blue-100 p-4">
          <p>Condition: {data.condition}</p>
          <p>Humidity: {data.humidity}%</p>
          <p>Wind Speed: {data.windSpeed} m/s</p>
        </div>
      </div>
    </div>
  );
};

export default WeatherCard;