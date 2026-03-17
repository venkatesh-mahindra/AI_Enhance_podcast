const API_URL = process.env.REACT_APP_API_URL || '/api';

export const uploadPdf = async (file) => {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch(`${API_URL}/upload-pdf`, {
    method: 'POST',
    body: formData
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.error || 'Failed to upload PDF');
  }

  return await response.json();
};

export const uploadVoice = async (file, jobId) => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('job_id', jobId);

  const response = await fetch(`${API_URL}/upload-voice`, {
    method: 'POST',
    body: formData
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.error || 'Failed to upload voice');
  }

  return await response.json();
};

export const generatePodcast = async (jobId, language, voiceType, enableMultiNarrator, multiNarratorVoiceSet = null) => {
  const response = await fetch(`${API_URL}/generate-podcast`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      job_id: jobId,
      language: language,
      voice_type: voiceType,
      enable_multi_narrator: enableMultiNarrator,
      multi_narrator_voice_set: multiNarratorVoiceSet
    })
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.error || 'Failed to generate podcast');
  }

  return await response.json();
};

export const analyzeCharacters = async (jobId) => {
  const response = await fetch(`${API_URL}/analyze-characters`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ job_id: jobId })
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.error || 'Failed to analyze characters');
  }

  return await response.json();
};

export const getAvailableVoices = async () => {
  const response = await fetch(`${API_URL}/voices`);

  if (!response.ok) {
    throw new Error('Failed to fetch available voices');
  }

  return await response.json();
};

export const getJobStatus = async (jobId) => {
  const response = await fetch(`${API_URL}/job-status/${jobId}`);

  if (!response.ok) {
    throw new Error('Failed to get job status');
  }

  return await response.json();
};