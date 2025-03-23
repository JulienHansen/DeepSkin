import React from 'react';
import diagnosisInfo from '../data/DiagnosisInfo';
import './components_css/DiagnosisMenu.css';

const DiagnosisMenu = () => (
  <div className="menu">
    <h3>Skin Condition Categories</h3>
    <ul>
      {Object.entries(diagnosisInfo).map(([key, val]) => (
        <li key={key}>
          <strong>{val.name}</strong><br />
          <span>{val.description}</span>
        </li>
      ))}
    </ul>
  </div>
);

export default DiagnosisMenu;
