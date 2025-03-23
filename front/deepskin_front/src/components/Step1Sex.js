const Step1Sex = ({ next, formData, setFormData }) => (
    <div>
      <h2>Select Sex</h2>
      <select value={formData.sex} onChange={(e) => setFormData({ ...formData, sex: e.target.value })}>
        <option value="">-- Select --</option>
        <option value="male">Male</option>
        <option value="female">Female</option>
        <option value="other">Other</option>
      </select>
      <br /><br />
      <button disabled={!formData.sex} onClick={next}>Next</button>
    </div>
  );
  export default Step1Sex;
  