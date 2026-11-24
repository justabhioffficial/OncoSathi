import React, { useState } from 'react';

interface AudioPlayerProps {
  text: string;
  language: string;
}

export const AudioPlayer: React.FC<AudioPlayerProps> = ({ text, language }) => {
  const [isPlaying, setIsPlaying] = useState(false);
  const [isPaused, setIsPaused] = useState(false);

  const playSpeech = () => {
    if (!('speechSynthesis' in window)) {
      alert('Your browser does not support audio speech output.');
      return;
    }
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    const isBn = language === 'bengali' || language === 'bn' || /[\u0980-\u09FF]/.test(text);
    utterance.lang = isBn ? 'bn-IN' : 'en-IN';
    utterance.rate = isBn ? 0.85 : 0.95;

    const voices = window.speechSynthesis.getVoices();
    if (voices.length > 0) {
      const match = voices.find(v => isBn ? v.lang.startsWith('bn') : v.lang.startsWith('en'));
      if (match) utterance.voice = match;
    }

    utterance.onstart = () => { setIsPlaying(true); setIsPaused(false); };
    utterance.onend = () => { setIsPlaying(false); setIsPaused(false); };
    utterance.onerror = () => { setIsPlaying(false); setIsPaused(false); };

    window.speechSynthesis.speak(utterance);
  };

  const pauseSpeech = () => {
    if (window.speechSynthesis.speaking && !isPaused) {
      window.speechSynthesis.pause();
      setIsPaused(true);
    } else if (isPaused) {
      window.speechSynthesis.resume();
      setIsPaused(false);
    }
  };

  const stopSpeech = () => {
    window.speechSynthesis.cancel();
    setIsPlaying(false);
    setIsPaused(false);
  };

  return (
    <div className="flex items-center justify-between p-2.5 bg-[#F7F8F6] rounded border border-[#E3E8E5] text-xs">
      <div className="flex items-center space-x-2 text-[#586563]">
        <span className="font-medium">Audio explanation ({language === 'bengali' ? 'বাংলা কন্ঠ' : 'English Voice'}):</span>
      </div>
      <div className="flex items-center space-x-1.5">
        {!isPlaying ? (
          <button
            onClick={playSpeech}
            className="px-2.5 py-1 bg-[#176B63] hover:bg-[#124E49] text-white rounded font-medium text-xs transition-colors"
          >
            Play audio
          </button>
        ) : (
          <>
            <button
              onClick={pauseSpeech}
              className="px-2 py-1 bg-slate-200 text-[#202A2A] rounded text-xs font-medium"
            >
              {isPaused ? 'Resume' : 'Pause'}
            </button>
            <button
              onClick={stopSpeech}
              className="px-2 py-1 bg-red-100 text-red-800 rounded text-xs font-medium"
            >
              Stop
            </button>
          </>
        )}
      </div>
    </div>
  );
};
