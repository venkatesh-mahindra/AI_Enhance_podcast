export const LANGUAGES = [
    { code: 'en', name: 'English' },
    { code: 'es', name: 'Spanish' },
    { code: 'fr', name: 'French' },
    { code: 'de', name: 'German' },
    { code: 'it', name: 'Italian' },
    { code: 'pt', name: 'Portuguese' },
    { code: 'zh-cn', name: 'Chinese' },
    { code: 'ja', name: 'Japanese' },
    { code: 'ko', name: 'Korean' }
  ];
  
  export const VOICE_OPTIONS = [
    {
      id: 'indian_male',
      name: '🇮🇳 Natural Indian Male (FREE)',
      description: '🎯 Human-like Indian English - Male voice (Non-robotic, No API costs) ⭐',
      icon: '🇮🇳👨'
    },
    {
      id: 'indian_female',
      name: '🇮🇳 Natural Indian Female (FREE)',
      description: '🎯 Human-like Indian English - Female voice (Non-robotic, No API costs) ⭐',
      icon: '🇮🇳👩'
    },
    {
      id: 'custom',
      name: '🎤 Your Voice (FREE AI Cloning)',
      description: '✨ Upload 10s audio → AI clones your voice perfectly! (Powered by Coqui XTTS - ₹0 cost)',
      icon: '🎤✨'
    },
    {
      id: 'male',
      name: 'Professional Male (US)',
      description: 'Deep, authoritative voice - American accent',
      icon: '👨'
    },
    {
      id: 'female',
      name: 'Professional Female (US)',
      description: 'Clear, engaging voice - American accent',
      icon: '👩'
    },
    {
      id: 'ai_neutral',
      name: 'AI Neutral (US)',
      description: 'Modern AI-generated voice - American accent',
      icon: '🤖'
    },
    {
      id: 'ai_energetic',
      name: 'AI Energetic (US)',
      description: 'Upbeat, enthusiastic AI voice - American accent',
      icon: '⚡'
    }
  ];

  export const MULTI_NARRATOR_VOICE_SETS = [
    {
      id: 'all_us_professional',
      name: '🇺🇸 All US Professional (Recommended for Testing)',
      description: 'Classic American voices - Male & Female characters with distinct voices',
      voices: {
        male: ['male', 'ai_neutral'],
        female: ['female', 'ai_energetic'],
        narrator: 'male'
      }
    },
    {
      id: 'diverse_professional',
      name: '🎭 Diverse Professional',
      description: 'Mix of Indian and US voices for natural conversations',
      voices: {
        male: ['indian_male', 'male', 'ai_neutral'],
        female: ['indian_female', 'female', 'ai_energetic'],
        narrator: 'indian_male'
      }
    },
    {
      id: 'all_indian_free',
      name: '🇮🇳 All Indian Voices (FREE)',
      description: 'All characters use natural Indian voices - completely free',
      voices: {
        male: ['indian_male'],
        female: ['indian_female'],
        narrator: 'indian_male'
      }
    },
    {
      id: 'mixed_variety',
      name: '🌟 Maximum Variety',
      description: 'Uses all available voice types for unique character distinction',
      voices: {
        male: ['indian_male', 'male', 'ai_neutral'],
        female: ['indian_female', 'female', 'ai_energetic'],
        narrator: 'ai_neutral'
      }
    }
  ];
  
  export const API_ENDPOINTS = {
    UPLOAD_PDF: '/upload-pdf',
    UPLOAD_VOICE: '/upload-voice',
    GENERATE_PODCAST: '/generate-podcast',
    ANALYZE_CHARACTERS: '/analyze-characters',
    GET_VOICES: '/voices',
    JOB_STATUS: '/job-status'
  };