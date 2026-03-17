import React from 'react';
import { Globe } from 'lucide-react';
import { LANGUAGES } from '../utils/constants';

const LanguageSelector = ({ selectedLanguage, onLanguageChange }) => {
  return (
    <div className="mb-6">
      <label className="flex items-center text-gray-700 font-semibold mb-3">
        <Globe className="w-5 h-5 mr-2" />
        Select Language
      </label>
      <select
        value={selectedLanguage}
        onChange={(e) => onLanguageChange(e.target.value)}
        className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
      >
        {LANGUAGES.map((lang) => (
          <option key={lang.code} value={lang.code}>
            {lang.name}
          </option>
        ))}
      </select>
    </div>
  );
};

export default LanguageSelector;