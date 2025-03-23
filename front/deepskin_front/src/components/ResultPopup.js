import React from 'react';
import diagnosisInfo from '../data/DiagnosisInfo';
import './components_css/ResultPopup.css';

const ResultPopup = ({ code, onClose }) => {
  const info = diagnosisInfo[code];

  if (!info) return null;

  return (
    <div className="popup-backdrop" onClick={onClose}>
      <div className="popup-card" onClick={(e) => e.stopPropagation()}>
        <h3>{info.name}</h3>
        <p>{info.description}</p>
        <button onClick={onClose}>Close</button>
      </div>
    </div>
  );
};

export default ResultPopup;
