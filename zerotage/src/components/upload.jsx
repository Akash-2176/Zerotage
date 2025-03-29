import { useState } from "react";
import "../upload.css";

export default function Upload() {
  const [video, setVideo] = useState(null);
  const [carsDetected, setCarsDetected] = useState(0);
  const [results, setResults] = useState([]);
  const [fileUploaded, setFileUploaded] = useState(false);
  const [loading, setLoading] = useState(false); // New state for loader

  // Function to upload the video and get the response
  const handleUpload = async (event) => {
    const file = event.target.files[0];
    if (file) {
      const videoURL = URL.createObjectURL(file);
      setVideo(videoURL);
      setFileUploaded(true);
      setLoading(true); // Show loader when uploading starts

      // Create form data and send to API
      const formData = new FormData();
      formData.append("video", file);

      try {
        const response = await fetch("http://127.0.0.1:8000/process_video/", {
          method: "POST",
          body: formData,
        });

        if (!response.ok) {
          throw new Error("Error processing the video.");
        }

        const data = await response.json();

        // Process the response from the backend
        const vehicles = data.vehicles.map((vehicle, index) => ({
          id: index + 1,
          screenshot: vehicle,
          enhanced: data.preprocessed_plates[index] || "",
          license: data.ocr_results[Object.keys(data.ocr_results)[index]] || "No License Plate Detected",
        }));

        setResults(vehicles);
        setCarsDetected(vehicles.length);
      } catch (error) {
        console.error("Error uploading video:", error);
      } finally {
        setLoading(false); // Hide loader when response is received
      }
    }
  };

  const handleReset = () => {
    setVideo(null);
    setResults([]);
    setCarsDetected(0);
    setFileUploaded(false);
    setLoading(false);
  };

  return (
    <>
      <header className="app-header">ZEROTAGE</header>

      <div className="container">
        {!fileUploaded ? (
          <div className="upload-box">
            <h1>Upload Video</h1>
            <label htmlFor="file-upload" className="custom-file-upload">
              Upload File
            </label>
            <input
              id="file-upload"
              type="file"
              accept="video/*"
              onChange={handleUpload}
            />
          </div>
        ) : (
          <>
            <h2 className="results-heading">Results</h2>
            {video && <video src={video} controls className="video-preview" />}
          </>
        )}

        {loading && (
          <div className="loader-container">
            <div className="spinner"></div>
            <p>Processing Results...</p>
          </div>
        )}

        {!loading && results.length > 0 && (
          <div className="results-box">
            <button className="close-btn" onClick={handleReset}>
              ✖
            </button>
            <h2>Cars Detected: {carsDetected}</h2>
            <table>
              <thead>
                <tr>
                  <th>Screenshot</th>
                  <th>Enhanced Image</th>
                  <th>License Number</th>
                </tr>
              </thead>
              <tbody>
                {results.map((car) => (
                  <tr key={car.id}>
                    <td>
                      <img
                        src={car.screenshot}
                        alt="Screenshot"
                        className="table-image"
                      />
                    </td>
                    <td>
                      <img
                        src={car.enhanced}
                        alt="Enhanced"
                        className="table-image"
                      />
                    </td>
                    <td>{car.license}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </>
  );
}
