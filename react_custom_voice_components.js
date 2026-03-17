/**
 * React Components for ElevenLabs Custom Voice Integration
 * For your Speech-to-Text project
 */

import React, { useState, useRef, useEffect } from 'react';

// Custom Voice Creator Component
const CustomVoiceCreator = () => {
  const [isRecording, setIsRecording] = useState(false);
  const [audioFiles, setAudioFiles] = useState([]);
  const [voiceName, setVoiceName] = useState('');
  const [isCreating, setIsCreating] = useState(false);
  const [createdVoiceId, setCreatedVoiceId] = useState(null);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorderRef.current = new MediaRecorder(stream);
      audioChunksRef.current = [];

      mediaRecorderRef.current.ondataavailable = (event) => {
        audioChunksRef.current.push(event.data);
      };

      mediaRecorderRef.current.onstop = () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/wav' });
        const audioFile = new File([audioBlob], `voice_sample_${Date.now()}.wav`, { type: 'audio/wav' });
        setAudioFiles(prev => [...prev, audioFile]);
      };

      mediaRecorderRef.current.start();
      setIsRecording(true);
      
      // Auto-stop after 30 seconds
      setTimeout(() => {
        if (mediaRecorderRef.current && isRecording) {
          stopRecording();
        }
      }, 30000);

    } catch (error) {
      console.error('Error starting recording:', error);
      alert('Could not access microphone');
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      mediaRecorderRef.current.stream.getTracks().forEach(track => track.stop());
      setIsRecording(false);
    }
  };

  const removeAudioFile = (index) => {
    setAudioFiles(prev => prev.filter((_, i) => i !== index));
  };

  const createCustomVoice = async () => {
    if (!voiceName || audioFiles.length === 0) {
      alert('Please provide a voice name and record at least one sample');
      return;
    }

    setIsCreating(true);
    const formData = new FormData();
    formData.append('voice_name', voiceName);
    
    audioFiles.forEach((file, index) => {
      formData.append('files', file);
    });

    try {
      const response = await fetch('/api/voice/create', {
        method: 'POST',
        body: formData
      });

      const result = await response.json();
      
      if (result.success) {
        setCreatedVoiceId(result.voice_id);
        alert(`Custom voice "${result.voice_name}" created successfully!`);
        // Reset form
        setAudioFiles([]);
        setVoiceName('');
      } else {
        alert(`Error: ${result.error}`);
      }
    } catch (error) {
      console.error('Error creating voice:', error);
      alert('Failed to create custom voice');
    } finally {
      setIsCreating(false);
    }
  };

  return (
    <div className="custom-voice-creator">
      <h2>🎙️ Create Custom Voice</h2>
      
      {/* Voice Name Input */}
      <div className="voice-name-section">
        <label>Voice Name:</label>
        <input
          type="text"
          value={voiceName}
          onChange={(e) => setVoiceName(e.target.value)}
          placeholder="e.g., My Custom Voice"
          className="voice-name-input"
        />
      </div>

      {/* Recording Section */}
      <div className="recording-section">
        <h3>📢 Record Voice Samples</h3>
        <p>Record 2-3 samples of 10-30 seconds each for best quality</p>
        
        <button
          onClick={isRecording ? stopRecording : startRecording}
          className={`record-button ${isRecording ? 'recording' : ''}`}
          disabled={isCreating}
        >
          {isRecording ? '⏹️ Stop Recording' : '🎤 Start Recording'}
        </button>
        
        {isRecording && (
          <div className="recording-indicator">
            🔴 Recording... (max 30 seconds)
          </div>
        )}
      </div>

      {/* Audio Files List */}
      {audioFiles.length > 0 && (
        <div className="audio-files-section">
          <h3>🎵 Recorded Samples ({audioFiles.length})</h3>
          {audioFiles.map((file, index) => (
            <div key={index} className="audio-file-item">
              <span>📄 {file.name}</span>
              <button
                onClick={() => removeAudioFile(index)}
                className="remove-button"
              >
                ❌ Remove
              </button>
            </div>
          ))}
        </div>
      )}

      {/* Create Voice Button */}
      <button
        onClick={createCustomVoice}
        disabled={!voiceName || audioFiles.length === 0 || isCreating}
        className="create-voice-button"
      >
        {isCreating ? '⏳ Creating Voice...' : '✨ Create Custom Voice'}
      </button>

      {/* Success Message */}
      {createdVoiceId && (
        <div className="success-message">
          ✅ Custom voice created! Voice ID: {createdVoiceId}
        </div>
      )}
    </div>
  );
};

// Text-to-Speech Component with Custom Voice
const CustomTextToSpeech = () => {
  const [text, setText] = useState('');
  const [voices, setVoices] = useState([]);
  const [selectedVoiceId, setSelectedVoiceId] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [audioUrl, setAudioUrl] = useState(null);

  // Load available voices
  useEffect(() => {
    loadVoices();
  }, []);

  const loadVoices = async () => {
    try {
      const response = await fetch('/api/voice/list');
      const result = await response.json();
      setVoices(result.voices || []);
      
      // Select first custom voice by default
      const customVoices = result.voices?.filter(v => v.category === 'cloned') || [];
      if (customVoices.length > 0) {
        setSelectedVoiceId(customVoices[0].voice_id);
      }
    } catch (error) {
      console.error('Error loading voices:', error);
    }
  };

  const generateSpeech = async () => {
    if (!text || !selectedVoiceId) {
      alert('Please enter text and select a voice');
      return;
    }

    setIsGenerating(true);
    setAudioUrl(null);

    try {
      const response = await fetch('/api/voice/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: text,
          voice_id: selectedVoiceId
        })
      });

      if (response.ok) {
        const audioBlob = await response.blob();
        const url = URL.createObjectURL(audioBlob);
        setAudioUrl(url);
      } else {
        const error = await response.json();
        alert(`Error: ${error.error}`);
      }
    } catch (error) {
      console.error('Error generating speech:', error);
      alert('Failed to generate speech');
    } finally {
      setIsGenerating(false);
    }
  };

  const downloadAudio = () => {
    if (audioUrl) {
      const a = document.createElement('a');
      a.href = audioUrl;
      a.download = 'generated_speech.wav';
      a.click();
    }
  };

  return (
    <div className="custom-text-to-speech">
      <h2>🔊 Text-to-Speech with Custom Voice</h2>

      {/* Voice Selection */}
      <div className="voice-selection">
        <label>Select Voice:</label>
        <select
          value={selectedVoiceId}
          onChange={(e) => setSelectedVoiceId(e.target.value)}
          className="voice-select"
        >
          <option value="">Choose a voice...</option>
          {voices.map(voice => (
            <option key={voice.voice_id} value={voice.voice_id}>
              {voice.name} {voice.category === 'cloned' ? '(Custom)' : '(Built-in)'}
            </option>
          ))}
        </select>
        <button onClick={loadVoices} className="refresh-button">
          🔄 Refresh
        </button>
      </div>

      {/* Text Input */}
      <div className="text-input-section">
        <label>Text to Convert:</label>
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Enter the text you want to convert to speech..."
          rows={4}
          className="text-input"
        />
        <div className="char-count">
          {text.length} characters
        </div>
      </div>

      {/* Generate Button */}
      <button
        onClick={generateSpeech}
        disabled={!text || !selectedVoiceId || isGenerating}
        className="generate-button"
      >
        {isGenerating ? '⏳ Generating...' : '🎵 Generate Speech'}
      </button>

      {/* Audio Player */}
      {audioUrl && (
        <div className="audio-result">
          <h3>🎉 Generated Audio:</h3>
          <audio controls src={audioUrl} className="audio-player">
            Your browser does not support the audio element.
          </audio>
          <br />
          <button onClick={downloadAudio} className="download-button">
            💾 Download Audio
          </button>
        </div>
      )}
    </div>
  );
};

// Voice Management Component
const VoiceManager = () => {
  const [voices, setVoices] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadVoices();
  }, []);

  const loadVoices = async () => {
    setLoading(true);
    try {
      const response = await fetch('/api/voice/list');
      const result = await response.json();
      setVoices(result.voices || []);
    } catch (error) {
      console.error('Error loading voices:', error);
    } finally {
      setLoading(false);
    }
  };

  const deleteVoice = async (voiceId, voiceName) => {
    if (!confirm(`Are you sure you want to delete "${voiceName}"?`)) {
      return;
    }

    try {
      const response = await fetch(`/api/voice/delete/${voiceId}`, {
        method: 'DELETE'
      });

      if (response.ok) {
        alert('Voice deleted successfully');
        loadVoices(); // Refresh list
      } else {
        const error = await response.json();
        alert(`Error: ${error.error}`);
      }
    } catch (error) {
      console.error('Error deleting voice:', error);
      alert('Failed to delete voice');
    }
  };

  const customVoices = voices.filter(v => v.category === 'cloned');
  const builtInVoices = voices.filter(v => v.category !== 'cloned');

  return (
    <div className="voice-manager">
      <h2>🎛️ Voice Management</h2>
      
      <button onClick={loadVoices} disabled={loading} className="refresh-button">
        {loading ? '⏳ Loading...' : '🔄 Refresh Voices'}
      </button>

      {/* Custom Voices */}
      <div className="voice-section">
        <h3>🎤 Custom Voices ({customVoices.length})</h3>
        {customVoices.length === 0 ? (
          <p>No custom voices created yet.</p>
        ) : (
          <div className="voice-list">
            {customVoices.map(voice => (
              <div key={voice.voice_id} className="voice-item custom">
                <div className="voice-info">
                  <strong>{voice.name}</strong>
                  <span className="voice-id">ID: {voice.voice_id}</span>
                </div>
                <button
                  onClick={() => deleteVoice(voice.voice_id, voice.name)}
                  className="delete-button"
                >
                  🗑️ Delete
                </button>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Built-in Voices */}
      <div className="voice-section">
        <h3>🎵 Built-in Voices ({builtInVoices.length})</h3>
        <div className="voice-list">
          {builtInVoices.slice(0, 5).map(voice => (
            <div key={voice.voice_id} className="voice-item builtin">
              <div className="voice-info">
                <strong>{voice.name}</strong>
                <span className="voice-accent">{voice.labels?.accent || 'N/A'}</span>
              </div>
            </div>
          ))}
          {builtInVoices.length > 5 && (
            <div className="more-voices">
              ... and {builtInVoices.length - 5} more
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

// Main App Component
const CustomVoiceApp = () => {
  const [activeTab, setActiveTab] = useState('create');

  return (
    <div className="custom-voice-app">
      <header>
        <h1>🎙️ Custom Voice Generator</h1>
        <p>Create and use custom voices with ElevenLabs API</p>
      </header>

      <nav className="tab-navigation">
        <button
          onClick={() => setActiveTab('create')}
          className={activeTab === 'create' ? 'active' : ''}
        >
          Create Voice
        </button>
        <button
          onClick={() => setActiveTab('generate')}
          className={activeTab === 'generate' ? 'active' : ''}
        >
          Generate Speech
        </button>
        <button
          onClick={() => setActiveTab('manage')}
          className={activeTab === 'manage' ? 'active' : ''}
        >
          Manage Voices
        </button>
      </nav>

      <main className="tab-content">
        {activeTab === 'create' && <CustomVoiceCreator />}
        {activeTab === 'generate' && <CustomTextToSpeech />}
        {activeTab === 'manage' && <VoiceManager />}
      </main>
    </div>
  );
};

export default CustomVoiceApp;
export { CustomVoiceCreator, CustomTextToSpeech, VoiceManager };
