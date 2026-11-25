import React, { useState, useRef } from 'react';
import { API_BASE } from '../services/api';

interface AudioPlayerProps {
  text: string;
  language: string;
}

export const AudioPlayer: React.FC<AudioPlayerProps> = ({ text, language }) => {
  const [isPlaying, setIsPlaying] = useState(false);
  const [isPaused, setIsPaused] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const audioRef = useRef<HTMLAudioElement | null>(null);

  const isBn = language === 'bengali' || language === 'bn' || /[\u0980-\u09FF]/.test(text);

  const playSpeech = async () => {
    if (!text) return;
    setIsLoading(true);

    // Try server-side native audio stream first (provides real native Bengali TTS)
    try {
      const streamUrl = `${API_BASE}/api/tts/stream?text=${encodeURIComponent(text)}&language=${isBn ? 'bn' : 'en'}`;
      
      if (audioRef.current) {
        audioRef.current.pause();
      }

      const audio = new Audio(streamUrl);
      audioRef.current = audio;

      audio.onplaying = () => {
        setIsLoading(false);
        setIsPlaying(true);
        setIsPaused(false);
      };

      audio.onpause = () => {
        if (!audio.ended) {
          setIsPaused(true);
        }
      };

      audio.onended = () => {
        setIsPlaying(false);
        setIsPaused(false);
        setIsLoading(false);
      };

      audio.onerror = () => {
        // Fallback to browser Web Speech API
        fallbackToBrowserSpeech();
      };

      await audio.play();
    } catch {
      fallbackToBrowserSpeech();
    }
  };

  const fallbackToBrowserSpeech = () => {
    setIsLoading(false);
    if (!('speechSynthesis' in window)) {
      alert('Your browser does not support audio speech output.');
      return;
    }
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
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
    if (audioRef.current && !audioRef.current.paused) {
      audioRef.current.pause();
      setIsPaused(true);
    } else if (audioRef.current && isPaused) {
      audioRef.current.play();
      setIsPaused(false);
    } else if (window.speechSynthesis.speaking && !isPaused) {
      window.speechSynthesis.pause();
      setIsPaused(true);
    } else if (isPaused) {
      window.speechSynthesis.resume();
      setIsPaused(false);
    }
  };

  const stopSpeech = () => {
    if (audioRef.current) {
      audioRef.current.pause();
      audioRef.current.currentTime = 0;
    }
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
    }
    setIsPlaying(false);
    setIsPaused(false);
    setIsLoading(false);
  };

  return (
    <div className="flex items-center justify-between p-2.5 bg-[#F7F8F6] rounded border border-[#E3E8E5] text-xs">
      <div className="flex items-center space-x-2 text-[#586563]">
        <span className="font-medium">
          Audio explanation ({isBn ? 'বাংলা কণ্ঠস্বর (Bengali Voice)' : 'English Voice'}):
        </span>
      </div>
      <div className="flex items-center space-x-1.5">
        {isLoading ? (
          <span className="px-2.5 py-1 text-slate-500 font-medium text-xs">
            Loading audio...
          </span>
        ) : !isPlaying ? (
          <button
            onClick={playSpeech}
            className="px-2.5 py-1 bg-[#176B63] hover:bg-[#124E49] text-white rounded font-medium text-xs transition-colors flex items-center gap-1"
          >
            <span>▶</span>
            <span>Play audio</span>
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
