import { useEffect, useRef, useState } from "react";
import { motion } from "framer-motion";
import { useNavigate } from "react-router-dom";
import "../home.css";

export default function Home() {
  const navigate = useNavigate();
  const homeRef = useRef(null);
  const titleRef = useRef(null);
  const [showHome, setShowHome] = useState(false);

  useEffect(() => {
    setTimeout(() => {
      setShowHome(true);
    }, 1500); // Delay for the animation
  }, []);

  return (
    <>
      {/* Animated ZEROTAGE Title */}
      <h1 className="title">
        ZEROTAGE
      </h1>

      {/* Home content appears after O animation */}
      {showHome && (
        <motion.div
          ref={homeRef}
          className="home-container"
          initial={{ x: -50, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          transition={{ duration: 1, ease: "easeOut", delay: 0.5 }}
        >
          <p className="description"> <strong style={{fontSize:60}}>Our AI-powered License Plate Enhancement and Recognition System</strong><br/> is designed to process CCTV footage for accurate vehicle detection, license plate enhancement, and text extraction.
This system utilizes advanced technologies like computer vision, deep learning, and OCR (Optical Character Recognition) to enhance the readability of license plates, even from low-resolution or blurry footage.
<br/>
 <strong style={{fontSize:40}}>Tech Stack:</strong><br/>
 <strong style={{fontSize:30}}>Frontend: </strong>React.js (for an interactive and responsive UI)<br/>

 <strong style={{fontSize:30}}>Backend:</strong> Python with FastAPI (for handling video processing and AI integration)<br/>

 <strong style={{fontSize:30}}>AI & Computer Vision Models Used:</strong> YOLO (You Only Look Once): Real-time vehicle and license plate detection<br/>

 <strong style={{fontSize:30}}>OCR (Optical Character Recognition):</strong> Extracts text from license plates<br/>

 <strong style={{fontSize:30}}>OpenCV:</strong> Enhances image clarity and improves recognition accuracy<br/>

This cutting-edge system ensures high precision in vehicle identification and license plate recognition, making it ideal for traffic monitoring, law enforcement, and security applications. 
</p>
          <button className="navigate-btn" onClick={() => navigate("/upload")}>
            Get Started
          </button>
        </motion.div>
      )}
    </>
  );
}
