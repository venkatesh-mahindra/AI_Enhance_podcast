import React from 'react';
import { Users, Volume2 } from 'lucide-react';
import { MULTI_NARRATOR_VOICE_SETS, VOICE_OPTIONS } from '../utils/constants';

const MultiNarratorVoiceSelector = ({ 
  selectedVoiceSet, 
  onVoiceSetChange, 
  characterInfo,
  enableMultiNarrator 
}) => {
  // Don't show if multi-narrator is disabled or no characters
  if (!enableMultiNarrator || !characterInfo || characterInfo.total_characters === 0) {
    return null;
  }

  const getVoicePreview = (voiceSet) => {
    const voices = voiceSet.voices;
    const maleVoices = voices.male || [];
    const femaleVoices = voices.female || [];
    
    const getMaleVoiceName = () => {
      if (maleVoices.length === 0) return 'No male voice';
      const voiceId = maleVoices[0];
      const voice = VOICE_OPTIONS.find(v => v.id === voiceId);
      return voice ? voice.name.split(' (')[0] : voiceId;
    };
    
    const getFemaleVoiceName = () => {
      if (femaleVoices.length === 0) return 'No female voice';
      const voiceId = femaleVoices[0];
      const voice = VOICE_OPTIONS.find(v => v.id === voiceId);
      return voice ? voice.name.split(' (')[0] : voiceId;
    };
    
    return {
      male: getMaleVoiceName(),
      female: getFemaleVoiceName(),
      maleCount: maleVoices.length,
      femaleCount: femaleVoices.length
    };
  };

  return (
    <div className="mb-8">
      <div className="flex items-center mb-4">
        <Users className="w-5 h-5 mr-2 text-purple-600" />
        <h3 className="text-lg font-semibold text-gray-800">
          Multi-Narrator Voice Selection
        </h3>
      </div>
      
      <div className="p-4 bg-gradient-to-r from-purple-50 to-pink-50 rounded-lg border-2 border-purple-200 mb-4">
        <div className="flex items-center mb-2">
          <span className="text-2xl mr-2">🎭</span>
          <h4 className="font-semibold text-purple-900">
            Characters Detected: {characterInfo.total_characters}
          </h4>
        </div>
        <p className="text-sm text-purple-800 mb-2">
          📊 {characterInfo.male_characters} male • {characterInfo.female_characters} female characters
        </p>
        <p className="text-xs text-purple-700">
          Choose a voice set to assign different voices to each character for engaging conversations
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {MULTI_NARRATOR_VOICE_SETS.map((voiceSet) => {
          const preview = getVoicePreview(voiceSet);
          const isSelected = selectedVoiceSet === voiceSet.id;
          
          return (
            <div
              key={voiceSet.id}
              onClick={() => onVoiceSetChange(voiceSet.id)}
              className={`p-4 rounded-lg border-2 cursor-pointer transition-all ${
                isSelected
                  ? 'border-purple-600 bg-purple-100 shadow-lg'
                  : 'border-gray-300 bg-white hover:border-purple-400 hover:shadow-md'
              }`}
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <h4 className="font-semibold text-gray-800 mb-1">
                    {voiceSet.name}
                  </h4>
                  <p className="text-sm text-gray-600 mb-3">
                    {voiceSet.description}
                  </p>
                  
                  {/* Voice Preview */}
                  <div className="space-y-2">
                    <div className="flex items-center text-xs">
                      <span className="text-blue-600 font-medium mr-2">👨 Male characters:</span>
                      <span className="text-gray-700">
                        {preview.male}
                        {preview.maleCount > 1 && ` (+${preview.maleCount - 1} more)`}
                      </span>
                    </div>
                    <div className="flex items-center text-xs">
                      <span className="text-pink-600 font-medium mr-2">👩 Female characters:</span>
                      <span className="text-gray-700">
                        {preview.female}
                        {preview.femaleCount > 1 && ` (+${preview.femaleCount - 1} more)`}
                      </span>
                    </div>
                  </div>
                </div>
                
                {isSelected && (
                  <div className="ml-2">
                    <div className="w-6 h-6 bg-purple-600 rounded-full flex items-center justify-center">
                      <svg className="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                      </svg>
                    </div>
                  </div>
                )}
              </div>
              
              {/* Special callouts */}
              {voiceSet.id === 'all_indian_free' && (
                <div className="mt-2 p-2 bg-green-100 rounded text-xs text-green-800">
                  💰 Completely FREE - No API costs!
                </div>
              )}
              {voiceSet.id === 'all_us_professional' && (
                <div className="mt-2 p-2 bg-blue-100 rounded text-xs text-blue-800">
                  🇺🇸 Features US Female voice as requested
                </div>
              )}
            </div>
          );
        })}
      </div>
      
      {/* Info about voice assignment */}
      <div className="mt-4 p-3 bg-gray-50 rounded-lg">
        <h5 className="text-sm font-medium text-gray-700 mb-1">
          🎯 How Voice Assignment Works:
        </h5>
        <ul className="text-xs text-gray-600 space-y-1">
          <li>• Each character gets assigned a voice based on their detected gender</li>
          <li>• Multiple voices per gender create variety when you have many characters</li>
          <li>• Narrator voice is used for non-dialogue content (descriptions, etc.)</li>
        </ul>
      </div>
    </div>
  );
};

export default MultiNarratorVoiceSelector;
