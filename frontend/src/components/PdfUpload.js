import React from 'react';
import { Upload, FileText } from 'lucide-react';

const PdfUpload = ({ onUpload, processing, pdfFile }) => {
  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      onUpload(file);
    }
  };

  return (
    <div className="bg-white rounded-2xl shadow-xl p-8">
      <div className="flex items-center mb-6">
        <FileText className="w-8 h-8 text-purple-600 mr-3" />
        <h2 className="text-2xl font-bold text-gray-800">Upload Your PDF</h2>
      </div>

      <div className="border-4 border-dashed border-gray-300 rounded-xl p-12 text-center hover:border-purple-400 transition-colors">
        <Upload className="w-16 h-16 text-gray-400 mx-auto mb-4" />
        <p className="text-gray-600 mb-4">
          Drag and drop your PDF here or click to browse
        </p>
        <input
          type="file"
          accept=".pdf"
          onChange={handleFileChange}
          className="hidden"
          id="pdf-upload"
          disabled={processing}
        />
        <label
          htmlFor="pdf-upload"
          className={`inline-block px-6 py-3 bg-purple-600 text-white rounded-lg cursor-pointer hover:bg-purple-700 transition-colors ${
            processing ? 'opacity-50 cursor-not-allowed' : ''
          }`}
        >
          {processing ? 'Uploading...' : 'Choose File'}
        </label>
      </div>

      {pdfFile && (
        <div className="mt-4 p-4 bg-green-50 rounded-lg">
          <p className="text-green-700">✓ {pdfFile.name} uploaded successfully</p>
        </div>
      )}
    </div>
  );
};

export default PdfUpload;