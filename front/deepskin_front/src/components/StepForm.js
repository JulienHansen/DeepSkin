import React, { useState } from 'react';
import Step1Sex from './Step1Sex';
import Step2Age from './Step2Age';
import Step3Localization from './Step3Localization';
import Step4ImageUpload from './Step4ImageUpload';
import axios from 'axios';
import diagnosisInfo from '../data/DiagnosisInfo';

const StepForm = ({ onPredict }) => {
  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState({
    sex: '',
    age: '',
    localization: '',
    image: null,
  });
  const [loading, setLoading] = useState(false);

  const next = () => setStep((s) => s + 1);
  const back = () => setStep((s) => s - 1);

  const [iframeSrc, setIframeSrc] = useState(null);
  const handleSubmit = async (e) => {
    e.preventDefault();
  
    const data = new FormData();
    data.append('sex', formData.sex);
    data.append('age', formData.age);
    data.append('localization', formData.localization);
    data.append('image', formData.image);
  
    setLoading(true);
    try {
      const response = await axios.post('/predict', data, {
        responseType: 'blob', // Get raw HTML as a blob
      });
  
      const htmlBlob = new Blob([response.data], { type: 'text/html' });
      const iframeURL = URL.createObjectURL(htmlBlob);
      setIframeSrc(iframeURL);  // <- This triggers the iframe to load
    } catch (err) {
      console.error('Prediction error:', err);
      alert('Prediction failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      {step === 1 && <Step1Sex next={next} formData={formData} setFormData={setFormData} />}
      {step === 2 && <Step2Age next={next} back={back} formData={formData} setFormData={setFormData} />}
      {step === 3 && <Step3Localization next={next} back={back} formData={formData} setFormData={setFormData} />}
      {step === 4 && (
        <Step4ImageUpload
          back={back}
          formData={formData}
          setFormData={setFormData}
          handleSubmit={handleSubmit}
          loading={loading}
        />
      )}
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

export default StepForm;
