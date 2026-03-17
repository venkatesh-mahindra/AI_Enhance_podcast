import React from 'react';
import { Volume2, Mic } from 'lucide-react';
import { VOICE_OPTIONS } from '../utils/constants';

const VoiceSelector = ({ selectedVoice, onVoiceChange, onVoiceUpload, processing, voiceFile }) => {
  const handleVoiceFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      onVoiceUpload(file);
    }
  };

  return (
    <div className="mb-8">
      <label className="flex items-center text-gray-700 font-semibold mb-4">
        <Volume2 className="w-5 h-5 mr-2" />
        Select Voice Style
      </label>
      
      {/* Indian Voices Section - Highlighted */}
      <div className="mb-4 p-3 bg-gradient-to-r from-orange-50 to-green-50 rounded-lg border-2 border-orange-200">
        <h3 className="text-sm font-bold text-orange-700 mb-2 flex items-center">
          🇮🇳 Local Indian Voices (FREE & OFFLINE) 
        </h3>
        <p className="text-xs text-green-700 mb-3 font-medium">
          💰 No API costs • 🚀 Instant generation • 🔒 Complete privacy
        </p>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {VOICE_OPTIONS.filter(v => v.id.startsWith('indian')).map((voice) => (
            <div
              key={voice.id}
              onClick={() => onVoiceChange(voice.id)}
              className={`p-4 rounded-lg border-2 cursor-pointer transition-all ${
                selectedVoice === voice.id
                  ? 'border-orange-600 bg-orange-100 shadow-lg'
                  : 'border-orange-300 bg-white hover:border-orange-400 hover:shadow'
              }`}
            >
              <div className="flex items-start">
                <span className="text-3xl mr-3">{voice.icon}</span>
                <div className="flex-1">
                  <h4 className="font-semibold text-gray-800 mb-1">{voice.name}</h4>
                  <p className="text-sm text-gray-600">{voice.description}</p>
                </div>
                {selectedVoice === voice.id && (
                  <div className="ml-2">
                    <div className="w-5 h-5 bg-orange-600 rounded-full flex items-center justify-center">
                      <svg className="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                      </svg>
                    </div>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Other Voices Section - Collapsible */}
      <details className="mb-4">
        <summary className="cursor-pointer text-sm font-semibold text-gray-600 mb-3 hover:text-gray-800 p-2 bg-gray-50 rounded">
          Other Voice Options (US Accent & Custom) ▼
        </summary>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-3">
          {VOICE_OPTIONS.filter(v => !v.id.startsWith('indian')).map((voice) => (
            <div
              key={voice.id}
              onClick={() => onVoiceChange(voice.id)}
              className={`p-4 rounded-lg border-2 cursor-pointer transition-all ${
                selectedVoice === voice.id
                  ? 'border-purple-600 bg-purple-50'
                  : 'border-gray-300 hover:border-purple-300'
              }`}
            >
              <div className="flex items-start">
                <span className="text-3xl mr-3">{voice.icon}</span>
                <div className="flex-1">
                  <h4 className="font-semibold text-gray-800 mb-1">{voice.name}</h4>
                  <p className="text-sm text-gray-600">{voice.description}</p>
                </div>
                {selectedVoice === voice.id && (
                  <div className="ml-2">
                    <div className="w-5 h-5 bg-purple-600 rounded-full flex items-center justify-center">
                      <svg className="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                      </svg>
                    </div>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      </details>

      {/* Custom Voice Upload Section - Coqui XTTS */}
      {selectedVoice === 'custom' && (
        <div className="p-4 bg-gradient-to-r from-purple-50 to-blue-50 rounded-lg border-2 border-purple-400">
          <p className="text-lg text-purple-900 mb-2 font-bold flex items-center">
            🎤✨ FREE AI Voice Cloning Selected!
          </p>
          <p className="text-sm text-green-700 mb-2 font-bold">
            💰 Powered by Coqui XTTS • Zero Cost Forever • Professional Quality
          </p>
          <p className="text-sm text-purple-800 mb-3 font-semibold">
            📝 Upload Your Voice Sample (10+ seconds)
          </p>
          <p className="text-sm text-purple-700 mb-3">
            Upload 10+ seconds of clear audio. AI will perfectly clone your voice for the entire podcast! Speak naturally with varied tone for best results.
          </p>
          <input
            type="file"
            accept=".mp3,.wav,.ogg"
            onChange={handleVoiceFileChange}
            className="hidden"
            id="voice-upload"
            disabled={processing}
          />
          <label
            htmlFor="voice-upload"
            className={`inline-block px-6 py-3 bg-blue-600 text-white rounded-lg cursor-pointer hover:bg-blue-700 transition-colors ${
              processing ? 'opacity-50 cursor-not-allowed' : ''
            }`}
          >
            <Mic className="w-4 h-4 inline mr-2" />
            {processing ? 'Processing...' : voiceFile ? '✓ Voice Uploaded' : 'Upload Voice'}
          </label>
          {voiceFile && (
            <p className="text-sm text-green-700 mt-2">✓ {voiceFile.name} uploaded successfully</p>
          )}
        </div>
      )}
    </div>
  );
};

export default VoiceSelector;