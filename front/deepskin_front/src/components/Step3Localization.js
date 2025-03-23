const localizations = [
    'scalp', 'ear', 'face', 'back', 'trunk', 'chest', 'upper extremity', 'abdomen',
    'unknown', 'lower extremity', 'genital', 'neck', 'hand', 'foot', 'acral',
  ];
  
  const Step3Localization = ({ next, back, formData, setFormData }) => (
    <div>
      <h2>Select Localization</h2>
      <select value={formData.localization} onChange={(e) => setFormData({ ...formData, localization: e.target.value })}>
        <option value="">-- Select --</option>
        {localizations.map((loc) => <option key={loc} value={loc}>{loc}</option>)}
      </select>
      <br /><br />
      <div className="button-group">
        <button onClick={back}>Back</button>
        <button disabled={!formData.localization} onClick={next}>Next</button>
      </div>
    </div>
  );
  export default Step3Localization;
  