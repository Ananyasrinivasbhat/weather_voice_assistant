import React, { useState } from 'react';

interface MicrophoneButtonProps {
  onVoiceInput: (text: string) => void;
}

const MicrophoneButton: React.FC<MicrophoneButtonProps> = ({ onVoiceInput }) => {
  const [listening, setListening] = useState(false);

  const handleMicrophoneClick = () => {
    if (!('webkitSpeechRecognition' in window)) {
      alert('Your browser does not support speech recognition.');
      return;
    }

    const recognition = new (window as any).webkitSpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;

    recognition.onstart = () => {
      setListening(true);
    };

    recognition.onresult = (event: any) => {
      const transcript = event.results[0][0].transcript;
      onVoiceInput(transcript);
      setListening(false);
    };

    recognition.onerror = (event: any) => {
      console.error('Speech recognition error:', event.error);
      setListening(false);
    };

    recognition.onend = () => {
      setListening(false);
    };

    recognition.start();
  };

  return (
    <button
      onClick={handleMicrophoneClick}
      className={`p-4 rounded-full ${
        listening ? 'bg-red-500' : 'bg-blue-500'
      } text-white`}
    >
      {listening ? 'Listening...' : '🎤'}
    </button>
  );
};

export default MicrophoneButton;