import React, { useState, useEffect } from 'react';
import './App.css';
import PdfUpload from './components/PdfUpload';
import VoiceSelector from './components/VoiceSelector';
import CharacterDisplay from './components/CharacterDisplay';
import MultiNarratorVoiceSelector from './components/MultiNarratorVoiceSelector';
import LanguageSelector from './components/LanguageSelector';
import PodcastPlayer from './components/PodcastPlayer';
import ProgressIndicator from './components/ProgressIndicator';
import { FileText, Volume2, Globe } from 'lucide-react';
import { uploadPdf, uploadVoice, generatePodcast, analyzeCharacters, getAvailableVoices } from './utils/api';
import { VOICE_OPTIONS } from './utils/constants';

function App() {
  const [step, setStep] = useState(1);
  const [pdfFile, setPdfFile] = useState(null);
  const [voiceFile, setVoiceFile] = useState(null);
  const [jobId, setJobId] = useState('');
  const [language, setLanguage] = useState('en');
  const [voiceType, setVoiceType] = useState('indian_male');
  const [enableMultiNarrator, setEnableMultiNarrator] = useState(false);
  const [multiNarratorVoiceSet, setMultiNarratorVoiceSet] = useState('diverse_professional');
  const [characterInfo, setCharacterInfo] = useState(null);
  const [availableVoices, setAvailableVoices] = useState(null);
  const [processing, setProcessing] = useState(false);
  const [podcastUrl, setPodcastUrl] = useState('');
  const [error, setError] = useState('');
  const [pdfPreview, setPdfPreview] = useState('');
  const [isMultiNarrator, setIsMultiNarrator] = useState(false);

  useEffect(() => {
    fetchAvailableVoices();
  }, []);

  const fetchAvailableVoices = async () => {
    try {
      const data = await getAvailableVoices();
      setAvailableVoices(data);
    } catch (err) {
      console.error('Failed to fetch voices:', err);
    }
  };

  const handlePdfUpload = async (file) => {
    setPdfFile(file);
    setError('');
    setProcessing(true);

    try {
      const data = await uploadPdf(file);
      const newJobId = data.job_id;
      setJobId(newJobId);
      setPdfPreview(data.preview);
      
      // Check if there's a saved voice selection for this job
      const savedVoiceType = localStorage.getItem(`voiceType_${newJobId}`);
      const savedVoiceFile = localStorage.getItem(`voiceFile_${newJobId}`);
      if (savedVoiceType === 'custom' && savedVoiceFile) {
        setVoiceType('custom');
        console.log(`Restored voice selection: ${savedVoiceFile}`);
      }
      
      await analyzeCharactersInPdf(newJobId);
      
      setStep(2);
    } catch (err) {
      setError(err.message || 'Failed to upload PDF');
    } finally {
      setProcessing(false);
    }
  };

  const analyzeCharactersInPdf = async (jobIdToAnalyze) => {
    try {
      const data = await analyzeCharacters(jobIdToAnalyze);
      if (data.has_dialogue) {
        setCharacterInfo(data.character_summary);
        setEnableMultiNarrator(true);
      }
    } catch (err) {
      console.log('Character analysis failed, continuing with single narrator');
    }
  };

  const handleVoiceUpload = async (file) => {
    setVoiceFile(file);
    setError('');
    setProcessing(true);

    try {
      const data = await uploadVoice(file, jobId);
      const quality = data.voice_profile?.analysis?.quality || 'unknown';
      const gender = data.voice_profile?.is_female ? 'Female' : 'Male';
      const pitch = data.voice_profile?.pitch?.mean || 0;
      
      alert(`Voice uploaded successfully!\n\nGender: ${gender}\nPitch: ${pitch.toFixed(0)} Hz\nQuality: ${quality}\n\nNow click "Generate Podcast" to use your voice!`);
      
      // Set to custom and save to localStorage
      setVoiceType('custom');
      localStorage.setItem(`voiceType_${jobId}`, 'custom');
      localStorage.setItem(`voiceFile_${jobId}`, file.name);
    } catch (err) {
      setError(err.message || 'Failed to upload voice');
    } finally {
      setProcessing(false);
    }
  };

  const handleGeneratePodcast = async () => {
    setError('');
    setProcessing(true);

    try {
      const data = await generatePodcast(jobId, language, voiceType, enableMultiNarrator, enableMultiNarrator ? multiNarratorVoiceSet : null);
      setPodcastUrl(data.audio_url);
      setIsMultiNarrator(data.is_multi_narrator || false);
      if (data.characters) {
        setCharacterInfo(data.characters);
      }
      setStep(3);
    } catch (err) {
      setError(err.message || 'Failed to generate podcast');
    } finally {
      setProcessing(false);
    }
  };

  const handleReset = () => {
    setStep(1);
    setPdfFile(null);
    setVoiceFile(null);
    setJobId('');
    setPodcastUrl('');
    setVoiceType('indian_male');
    setMultiNarratorVoiceSet('diverse_professional');
    setCharacterInfo(null);
    setEnableMultiNarrator(true);
    setIsMultiNarrator(false);
    setError('');
    setPdfPreview('');
  };

  return (
    <div className="App min-h-screen bg-gradient-to-br from-purple-50 via-blue-50 to-pink-50 p-8">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12 fade-in">
          <h1 className="text-5xl font-bold text-gray-800 mb-4">
            PDF to Podcast Converter
          </h1>
          <p className="text-gray-600 text-lg">
            Transform your documents into engaging audio podcasts with AI
          </p>
        </div>

        {/* Progress Steps */}
        <ProgressIndicator currentStep={step} />

        {/* Error Display */}
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6 fade-in">
            {error}
          </div>
        )}

        {/* Step 1: Upload PDF */}
        {step === 1 && (
          <div className="fade-in">
            <PdfUpload 
              onUpload={handlePdfUpload}
              processing={processing}
              pdfFile={pdfFile}
            />
          </div>
        )}

        {/* Step 2: Customize */}
        {step === 2 && (
          <div className="bg-white rounded-2xl shadow-xl p-8 fade-in">
            <h2 className="text-2xl font-bold text-gray-800 mb-6">Customize Your Podcast</h2>

            {pdfPreview && (
              <div className="mb-6 p-4 bg-gray-50 rounded-lg">
                <h3 className="font-semibold text-gray-700 mb-2">Document Preview:</h3>
                <p className="text-sm text-gray-600">{pdfPreview.substring(0, 200)}...</p>
              </div>
            )}

            <CharacterDisplay 
              characterInfo={characterInfo}
              enableMultiNarrator={enableMultiNarrator}
              onToggleMultiNarrator={setEnableMultiNarrator}
            />

            <LanguageSelector 
              selectedLanguage={language}
              onLanguageChange={setLanguage}
            />

            <VoiceSelector 
              selectedVoice={voiceType}
              onVoiceChange={setVoiceType}
              onVoiceUpload={handleVoiceUpload}
              processing={processing}
              voiceFile={voiceFile}
            />

            <MultiNarratorVoiceSelector 
              selectedVoiceSet={multiNarratorVoiceSet}
              onVoiceSetChange={setMultiNarratorVoiceSet}
              characterInfo={characterInfo}
              enableMultiNarrator={enableMultiNarrator}
            />

            <button
              onClick={handleGeneratePodcast}
              disabled={processing}
              className={`w-full py-4 bg-gradient-to-r from-purple-600 to-pink-600 text-white rounded-lg font-bold text-lg hover:from-purple-700 hover:to-pink-700 transition-all ${
                processing ? 'opacity-50 cursor-not-allowed' : ''
              }`}
            >
              {processing ? (
                <span className="flex items-center justify-center">
                  <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-white mr-3"></div>
                  Generating Podcast...
                </span>
              ) : (
                'Generate Podcast'
              )}
            </button>

            <button
              onClick={() => setStep(1)}
              className="w-full mt-4 py-3 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors"
            >
              Back
            </button>
          </div>
        )}

        {/* Step 3: Download */}
        {step === 3 && podcastUrl && (
          <div className="fade-in">
            <PodcastPlayer 
              podcastUrl={podcastUrl}
              isMultiNarrator={isMultiNarrator}
              characterInfo={characterInfo}
              onReset={handleReset}
            />
          </div>
        )}

        {/* Features */}
        <div className="mt-12 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div className="bg-white rounded-xl p-6 shadow-lg card-hover">
            <FileText className="w-8 h-8 text-purple-600 mb-3" />
            <h3 className="font-bold text-gray-800 mb-2">Smart Content Analysis</h3>
            <p className="text-sm text-gray-600">
              AI understands and describes diagrams, charts, and images
            </p>
          </div>

          <div className="bg-white rounded-xl p-6 shadow-lg card-hover">
            <Volume2 className="w-8 h-8 text-blue-600 mb-3" />
            <h3 className="font-bold text-gray-800 mb-2">Multiple Voice Options</h3>
            <p className="text-sm text-gray-600">
              Choose from professional male/female voices, AI-generated options, or clone your own voice
            </p>
          </div>

          <div className="bg-white rounded-xl p-6 shadow-lg card-hover">
            <div className="text-3xl mb-3">🎭</div>
            <h3 className="font-bold text-gray-800 mb-2">Multi-Narrator Detection</h3>
            <p className="text-sm text-gray-600">
              Automatically detects characters and assigns gender-appropriate voices to dialogues
            </p>
          </div>

          <div className="bg-white rounded-xl p-6 shadow-lg card-hover">
            <Globe className="w-8 h-8 text-green-600 mb-3" />
            <h3 className="font-bold text-gray-800 mb-2">Multi-Language</h3>
            <p className="text-sm text-gray-600">
              Generate podcasts in 9+ different languages
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;