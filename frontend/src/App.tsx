import { useState, useEffect, useRef } from 'react';
import SearchBar from '../src/components/SearchBar';
import WeatherCard from '../src/components/WeatherCard';
import MicrophoneButton from './components/MicrophoneButton';
import LoadingSpinner from '../src/components/Loadingspinner';
import ErrorModal from '../src/components/ErrorModal';
import './styles/animations.css';
import './styles/global.css';

// Define types for the weather data and backend response
interface WeatherData {
  city: string;
  temperature: number;
  humidity: number;
  windSpeed: number;
  condition: string;
}

interface BackendResponse {
  intent: string;
  city: string;
  weather: WeatherData;
}

function App() {
  const [weatherData, setWeatherData] = useState<BackendResponse | null>(null);
  const [currentLocationWeather, setCurrentLocationWeather] = useState<WeatherData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [recentSearches, setRecentSearches] = useState<BackendResponse[]>([]);
  const [_isSpeaking, setIsSpeaking] = useState(false);
  const weatherCardRef = useRef<HTMLDivElement>(null);

  // Fetch current location weather (e.g., Bengaluru)
  useEffect(() => {
    const fetchCurrentLocationWeather = async () => {
      try {
        const response = await fetch('/api/process', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ text: 'Bengaluru' }),
        });

        if (!response.ok) {
          throw new Error('Failed to fetch current location weather');
        }

        const data: BackendResponse = await response.json();
        setCurrentLocationWeather(data.weather);
      } catch (err) {
        setError('Failed to fetch current location weather');
      }
    };

    fetchCurrentLocationWeather();
  }, []);

  // Function to read out the weather condition
  const speakWeather = (data: WeatherData) => {
    if (!('speechSynthesis' in window)) {
      console.error('Text-to-speech is not supported in this browser.');
      return;
    }

    const speech = new SpeechSynthesisUtterance();
    speech.text = `The weather in ${data.city} is ${data.condition}. The temperature is ${data.temperature} degrees Celsius, with a humidity of ${data.humidity} percent and wind speed of ${data.windSpeed} meters per second.`;

    // Optional: Configure voice and language
    const voices = window.speechSynthesis.getVoices();
    const voice = voices.find((v) => v.lang === 'en-US'); // Use an English voice
    if (voice) {
      speech.voice = voice;
    }

    // Handle errors
    speech.onerror = (event) => {
      console.error('Speech synthesis error:', event.error);
    };

    // Start speaking
    setIsSpeaking(true);
    window.speechSynthesis.speak(speech);

    // Trigger pop animation when speech starts
    if (weatherCardRef.current) {
      weatherCardRef.current.classList.add('pop-animation');
    }

    // Stop pop animation when speech ends
    speech.onend = () => {
      setIsSpeaking(false);
      if (weatherCardRef.current) {
        weatherCardRef.current.classList.remove('pop-animation');
      }
    };
  };

  // Trigger speech when weatherData changes
  useEffect(() => {
    if (weatherData && weatherData.weather) {
      speakWeather(weatherData.weather);
    }
  }, [weatherData]);

  // Fetch weather data from backend
  const fetchWeather = async (city: string) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch('/api/process', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: city }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to fetch weather data');
      }

      const data: BackendResponse = await response.json();
      setWeatherData(data);

      // Update recent searches (keep only last 3)
      setRecentSearches((prev) => {
        const newSearches = [data, ...prev.filter((w) => w.city !== data.city)].slice(0, 3);
        return newSearches;
      });
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError('An unexpected error occurred.');
      }
    }
    finally {
      setLoading(false);
    }
  };

  // Callback for voice input
  const handleVoiceInput = (text: string) => {
    fetchWeather(text);
  };

  // Callback for search input
  const handleSearch = (city: string) => {
    fetchWeather(city);
  };

  return (
    <div className="container">
      {/* Heading */}
      <div className="header">
        <h1 className="text-4xl font-bold mb-8">Voice Weather Assistant</h1>
      </div>

      {/* Main Content */}
      <div className="main-content">
        {/* Current Location Weather */}
        <div className="current-location-weather">
          <h2 className="text-2xl font-semibold mb-4">Current Location Weather</h2>
          {currentLocationWeather ? (
            <WeatherCard data={currentLocationWeather} />
          ) : (
            <p>Loading current location weather...</p>
          )}
        </div>

        {/* Search and Microphone Box */}
        <div className="search-mic-box">
          <SearchBar onSearch={handleSearch} />
          <MicrophoneButton onVoiceInput={handleVoiceInput} />
        

        {/* Loading and Error Handling */}
        {loading && <LoadingSpinner />}
        {error && <ErrorModal message={error} onClose={() => setError(null)} />}

        {/* Display Searched Weather */}
        {weatherData && weatherData.weather && (
          <div className="mb-8" ref={weatherCardRef}>
            <WeatherCard data={weatherData.weather} />
          </div>
        )}
      </div>
      </div>

      <div className="recent-searches">
  <h2 className="text-xl font-semibold mb-4">Recent Searches</h2>
  <div className="cards-container">
    {recentSearches.map((search) => (
      <div key={search.city} className="flip-card-container">
        <div
          className="flip-card"
          onClick={() => fetchWeather(search.city)}
        >
          <div className="flip-card-inner">
            <div className="flip-card-front">
              <h3 className="text-lg font-semibold">{search.city}</h3>
            </div>
            <div className="flip-card-back">
              {search.weather ? (
                <>
                  <p>Temperature: {search.weather.temperature}°C</p>
                  <p>Humidity: {search.weather.humidity}%</p>
                  <p>Wind Speed: {search.weather.windSpeed} km/h</p>
                  <p>Condition: {search.weather.condition}</p>
                </>
              ) : (
                <p>Weather data not available.</p>
              )}
            </div>
          </div>
        </div>
      </div>
    ))}
  </div>
</div>
    </div>
  );
}

export default App;