import React from 'react';

const CharacterDisplay = ({ characterInfo, enableMultiNarrator, onToggleMultiNarrator }) => {
  if (!characterInfo || characterInfo.total_characters === 0) {
    return null;
  }

  return (
    <div className="mb-6 p-4 bg-gradient-to-r from-purple-50 to-pink-50 rounded-lg border-2 border-purple-200">
      <div className="flex items-start">
        <div className="text-3xl mr-3">🎭</div>
        <div className="flex-1">
          <h3 className="font-bold text-purple-900 mb-2">
            🎉 Dialogue Detected! Multi-Narrator Available
          </h3>
          <p className="text-sm text-purple-800 mb-3">
            We found <strong>{characterInfo.total_characters} characters</strong> in your document:
          </p>
          <div className="flex flex-wrap gap-2 mb-3">
            {characterInfo.characters.slice(0, 5).map((char, idx) => (
              <span key={idx} className="px-3 py-1 bg-white rounded-full text-sm border border-purple-300">
                {char.gender === 'male' ? '👨' : char.gender === 'female' ? '👩' : '👤'} {char.name}
              </span>
            ))}
            {characterInfo.total_characters > 5 && (
              <span className="px-3 py-1 bg-white rounded-full text-sm border border-purple-300">
                +{characterInfo.total_characters - 5} more
              </span>
            )}
          </div>
          
          <div className="flex items-center mt-3">
            <input
              type="checkbox"
              id="multi-narrator"
              checked={enableMultiNarrator}
              onChange={(e) => onToggleMultiNarrator(e.target.checked)}
              className="w-5 h-5 text-purple-600 rounded focus:ring-purple-500"
            />
            <label htmlFor="multi-narrator" className="ml-3 text-sm font-medium text-purple-900">
              Enable Multi-Narrator (Each character gets their own voice based on gender)
            </label>
          </div>
          
          {!enableMultiNarrator && (
            <p className="text-xs text-purple-700 mt-2 ml-8">
              Disabled: Will use single voice for entire podcast
            </p>
          )}
        </div>
      </div>
    </div>
  );
};

export default CharacterDisplay;