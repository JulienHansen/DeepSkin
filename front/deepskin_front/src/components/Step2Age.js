const Step2Age = ({ next, back, formData, setFormData }) => (
    <div>
      <h2>Enter Age</h2>
      <input
        type="number"
        value={formData.age}
        onChange={(e) => setFormData({ ...formData, age: e.target.value })}
        min={0}
      />
      <br /><br />
      <div className="button-group">
        <button onClick={back}>Back</button>
        <button disabled={!formData.age} onClick={next}>Next</button>
      </div>
    </div>
  );
  export default Step2Age;
  