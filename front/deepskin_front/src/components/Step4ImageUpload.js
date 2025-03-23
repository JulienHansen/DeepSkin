const Step4ImageUpload = ({ back, formData, setFormData, handleSubmit, loading }) => (
    <div>
      <h2>Upload Skin Mark Image</h2>
      <input
        type="file"
        accept="image/*"
        onChange={(e) => setFormData({ ...formData, image: e.target.files[0] })}
      />
      <br /><br />
      <div className="button-group">
        <button onClick={back}>Back</button>
        <button disabled={!formData.image || loading} onClick={handleSubmit}>
          {loading ? 'Predicting...' : 'Submit'}
        </button>
      </div>
    </div>
  );
  export default Step4ImageUpload;
  