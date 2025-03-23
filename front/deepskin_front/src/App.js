import React, { useState } from 'react';
import SkinForm from './components/SkinForm';
import StepForm from './components/StepForm';
import DiagnosisMenu from './components/DiagnosisMenu';
import ResultPopup from './components/ResultPopup';
import './App.css';

const App = () => {
  const [mode, setMode] = useState('single'); // 'single' or 'steps'
  const [popupCode, setPopupCode] = useState(null);

  const handlePrediction = (code) => {
    setPopupCode(code);
  };

  return (
    <div className="App">
      <header>
        <h1>Skin Mark AI Classifier</h1>
      </header>
  
      <main className="main-layout">
        <aside className="sidebar">
          <DiagnosisMenu />
        </aside>
  
        <section className="form-section">
          <div className="form-header">
            <h2>Skin Mark Prediction</h2>
            <div className="button-group">
              <button onClick={() => setMode('single')} disabled={mode === 'single'}>
                Single Page Form
              </button>
              <button onClick={() => setMode('steps')} disabled={mode === 'steps'}>
                Step-by-Step Form
              </button>
            </div>
          </div>
  
          {mode === 'single' ? (
            <SkinForm onPredict={handlePrediction} />
          ) : (
            <StepForm onPredict={handlePrediction} />
          )}
        </section>
      </main>
  
      {popupCode && <ResultPopup code={popupCode} onClose={() => setPopupCode(null)} />}
    </div>
  );
  
};

export default App;


