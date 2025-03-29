// import { useState } from "react";
// import "./App.css";

// export default function App() {
//   const [video, setVideo] = useState(null);
//   const [carsDetected, setCarsDetected] = useState(0);
//   const [results, setResults] = useState([]);

//   const handleUpload = (event) => {
//     const file = event.target.files[0];
//     if (file) {
//       setVideo(URL.createObjectURL(file));

//       // Simulating detection result
//       setTimeout(() => {
//         setCarsDetected(3);
//         setResults([
//           { id: 1, screenshot: "screenshot1.jpg", enhanced: "enhanced1.jpg", license: "ABC123" },
//           { id: 2, screenshot: "screenshot2.jpg", enhanced: "enhanced2.jpg", license: "XYZ789" },
//           { id: 3, screenshot: "screenshot3.jpg", enhanced: "enhanced3.jpg", license: "LMN456" },
//         ]);
//       },0);
//     }
//   };

//   return (
//     <>
//     <header className="app-header">ZEROTAGE</header>

//     <div className="container">
//       <div className="upload-box">
//         <h1>Upload Video</h1>
//         <label htmlFor="file-upload" className="custom-file-upload">File here</label>
//         <input id="file-upload" type="file" accept="video/*" onChange={handleUpload} />
//         {video && <video src={video} controls className="video-preview" />}
//       </div>

//       {results.length > 0 && (
//         <div className="results-box">
//           <h2>Cars Detected: {carsDetected}</h2>
//           <table>
//             <thead>
//               <tr>
//                 <th>Screenshot</th>
//                 <th>Enhanced Image</th>
//                 <th>License Number</th>
//               </tr>
//             </thead>
//             <tbody>
//               {results.map((car) => (
//                 <tr key={car.id}>
//                   <td><img src={car.screenshot} alt="Screenshot" className="table-image" /></td>
//                   <td><img src={car.enhanced} alt="Enhanced" className="table-image" /></td>
//                   <td>{car.license}</td>
//                 </tr>
//               ))}
//             </tbody>
//           </table>
//         </div>
//       )}
//     </div>
//     </>
//   );
// }


import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./components/home";
import Upload from "./components/upload";
import "./App.css";

export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/upload" element={<Upload />} />
      </Routes>
    </Router>
  );
}

