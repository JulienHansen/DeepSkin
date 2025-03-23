import React, { useState } from 'react';
import axios from 'axios';
import diagnosisInfo from '../data/DiagnosisInfo';

const localizations = [
  'scalp', 'ear', 'face', 'back', 'trunk', 'chest', 'upper extremity', 'abdomen',
  'unknown', 'lower extremity', 'genital', 'neck', 'hand', 'foot', 'acral',
];

const SkinForm = ({ onPredict }) => {
  const [formData, setFormData] = useState({
    sex: '',
    age: '',
    localization: '',
    image: null,
  });
  const [loading, setLoading] = useState(false);

  const [iframeSrc, setIframeSrc] = useState(null);
  const handleSubmit = async (e) => {
    e.preventDefault();
  
    const data = new FormData();
    data.append('sex', formData.sex);
    data.append('age', formData.age);
    data.append('localization', formData.localization);
    data.append('image', formData.image);
  
    setLoading(true);
    // console.log("Loading!");
      
    try {
      const response = await axios.post('/predict', data, {
        responseType: 'blob', // Get raw HTML as a blob
      });
      // console.log("Response: ", response);
  
      const htmlBlob = new Blob([response.data], { type: 'text/html' });
      const iframeURL = URL.createObjectURL(htmlBlob);
      setIframeSrc(iframeURL);  // <- This triggers the iframe to load
    } catch (err) {
      // console.log("Error!");
      console.error('Prediction error:', err);
      alert('Prediction failed. Please try again.');
    } finally {
      // console.log("Done!!");
      setLoading(false);
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <div className="form_field">
          <label>Sex:</label>
          <select
            value={formData.sex}
            onChange={(e) => setFormData({ ...formData, sex: e.target.value })}
            required
          >
            <option value="">-- Select --</option>
            <option value="male">Male</option>
            <option value="female">Female</option>
            <option value="other">Other</option>
          </select>
        </div>
        <div className="form_field">
          <label>Age:</label>
          <input
            type="number"
            min={0}
            value={formData.age}
            onChange={(e) => setFormData({ ...formData, age: e.target.value })}
            required
          />
        </div>
        <div className="form_field">
          <label>Localization:</label>
          <select
            value={formData.localization}
            onChange={(e) => setFormData({ ...formData, localization: e.target.value })}
            required
          >
            <option value="">-- Select --</option>
            {localizations.map((loc) => (
              <option key={loc} value={loc}>{loc}</option>
            ))}
          </select>
        </div>
        <div className="form_field">
          <label>Image:</label>
          <input
            type="file"
            accept="image/*"
            onChange={(e) => setFormData({ ...formData, image: e.target.files[0] })}
            required
          />
        </div>
        <div>
          <button type="submit" disabled={loading || !formData.image}>
            {loading ? 'Predicting...' : 'Submit'}
          </button>
        </div>
      </form>
      {iframeSrc && (
        <div style={{ marginTop: 30 }}>
          <h3>Diagnosis Result</h3>
          <iframe
            title="Prediction Result"
            src={iframeSrc}
            style={{
              width: '100%',
              height: '600px',
              border: '1px solid #ccc',
              borderRadius: '8px',
            }}
          />
        </div>
      )}
    </div>
  );
};

export default SkinForm;
