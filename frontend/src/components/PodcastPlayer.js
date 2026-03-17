import React from 'react';
import { Play, Download } from 'lucide-react';

const PodcastPlayer = ({ podcastUrl, isMultiNarrator, characterInfo, onReset }) => {
  const hasCharacters =
    isMultiNarrator &&
    characterInfo &&
    Number.isFinite(characterInfo.male_characters) &&
    Number.isFinite(characterInfo.female_characters) &&
    Array.isArray(characterInfo.characters) &&
    characterInfo.characters.length > 0;

  // Convert relative URL to absolute for downloads (bypasses proxy)
  const getAbsoluteUrl = (url) => {
    if (url.startsWith('http')) return url;
    return `http://localhost:5000${url}`;
  };

  const downloadUrl = getAbsoluteUrl(podcastUrl);

  return (
    <div className="bg-white rounded-2xl shadow-xl p-8 text-center">
      <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-6">
        <Play className="w-10 h-10 text-green-600" />
      </div>

      <h2 className="text-3xl font-bold text-gray-800 mb-4">
        Your Podcast is Ready! 🎉
      </h2>

      <p className="text-gray-600 mb-8">
        Your PDF has been converted into an engaging audio podcast
        {isMultiNarrator && ' with multiple narrators'}
      </p>

      {hasCharacters && (
        <div className="mb-6 p-4 bg-purple-50 rounded-lg border border-purple-200">
          <div className="flex items-center mb-2">
            <span className="text-2xl mr-2">🎭</span>
            <h3 className="font-semibold text-purple-900">Multi-Narrator Podcast</h3>
          </div>
          <p className="text-sm text-purple-800 mb-2">
            This podcast features {characterInfo.male_characters} male and {characterInfo.female_characters} female voices
          </p>
          <div className="flex flex-wrap gap-2">
            {characterInfo.characters.slice(0, 5).map((char, idx) => (
              <span
                key={idx}
                className="px-2 py-1 bg-white rounded-md text-xs border border-purple-200"
              >
                {char.gender === 'male' ? '👨' : '👩'} {char.name}
              </span>
            ))}
          </div>
        </div>
      )}

      <div className="mb-8 p-6 bg-gray-50 rounded-xl">
        <audio controls className="w-full" src={podcastUrl}>
          Your browser does not support the audio element.
        </audio>
      </div>

      <div className="flex flex-col sm:flex-row gap-4 justify-center">
        <a
          href={`${downloadUrl}?download=1`}
          download="podcast.wav"
          className="inline-flex items-center justify-center px-6 py-3 bg-purple-600 text-white rounded-lg font-semibold hover:bg-purple-700 transition-colors"
        >
          <Download className="w-5 h-5 mr-2" />
          Download WAV
        </a>
        
        <a
          href={`${downloadUrl}?format=mp3&download=1`}
          download="podcast.mp3"
          className="inline-flex items-center justify-center px-6 py-3 bg-indigo-600 text-white rounded-lg font-semibold hover:bg-indigo-700 transition-colors"
        >
          <Download className="w-5 h-5 mr-2" />
          Download MP3
        </a>
      </div>
      
      <p className="text-xs text-gray-500 mt-3">
        💡 WAV: High quality, larger file • MP3: Compressed, smaller file
      </p>

      <button
        onClick={onReset}
        className="w-full mt-6 py-3 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors"
      >
        Create Another Podcast
      </button>
    </div>
  );
};

export default PodcastPlayer;
