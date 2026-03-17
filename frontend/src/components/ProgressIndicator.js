import React from 'react';

const ProgressIndicator = ({ currentStep }) => {
  const steps = [
    { number: 1, label: 'Upload PDF' },
    { number: 2, label: 'Customize' },
    { number: 3, label: 'Get Podcast' }
  ];

  return (
    <div className="flex justify-between mb-12">
      {steps.map((step, index) => (
        <React.Fragment key={step.number}>
          <div className="flex flex-col items-center flex-1">
            <div className={`w-12 h-12 rounded-full flex items-center justify-center font-bold text-lg transition-all ${
              currentStep >= step.number 
                ? 'bg-purple-600 text-white scale-110' 
                : 'bg-gray-300 text-gray-600'
            }`}>
              {step.number}
            </div>
            <div className="text-sm mt-2 text-gray-600 font-medium">
              {step.label}
            </div>
          </div>
          {index < steps.length - 1 && (
            <div className="flex items-center justify-center" style={{ width: '100px', marginTop: '24px' }}>
              <div className={`h-1 w-full transition-all ${
                currentStep > step.number ? 'bg-purple-600' : 'bg-gray-300'
              }`}></div>
            </div>
          )}
        </React.Fragment>
      ))}
    </div>
  );
};

export default ProgressIndicator;