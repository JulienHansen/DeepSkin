const Result = ({ result }) => (
    <div>
      <h2>Prediction Result</h2>
      {result.error ? (
        <p style={{ color: 'red' }}>{result.error}</p>
      ) : (
        <pre>{JSON.stringify(result, null, 2)}</pre>
      )}
    </div>
  );
  export default Result;
  