import React, { useState, useEffect, useRef } from 'react';

const WebcamCapture = () => {
  const [isCapturing, setIsCapturing] = useState(false);
  const [images, setImages] = useState([]);
  const [error, setError] = useState(null);
  const videoRef = useRef(null);
  const streamRef = useRef(null);
  const timerRef = useRef(null);

  // Request camera access and setup video stream
  const startCamera = async () => {
    try {
      // Clear previous error
      setError(null);
      
      // Try to get camera with more detailed constraints
      const stream = await navigator.mediaDevices.getUserMedia({
        video: {
          width: { ideal: 320 },
          height: { ideal: 240 },
          facingMode: "user"
        }
      });
      
      // If we get here, permission was granted
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        streamRef.current = stream;
        setIsCapturing(true);
        startCaptureTimer();
      }
    } catch (err) {
      console.error("Camera access error:", err);
      
      if (err.name === "NotAllowedError") {
        setError("Camera access was denied. Please check your browser settings and try again.");
      } else if (err.name === "NotFoundError") {
        setError("No camera was found on your device.");
      } else {
        setError("Could not access camera: " + err.message);
      }
      
      setIsCapturing(false);
    }
  };

  // Stop capturing and release camera
  const stopCamera = () => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop());
      streamRef.current = null;
    }
    
    if (timerRef.current) {
      clearInterval(timerRef.current);
      timerRef.current = null;
    }
    
    setIsCapturing(false);
  };

  // Start timer to capture images
  const startCaptureTimer = () => {
    // Capture immediately when starting
    captureImage();
    
    // Then set interval for every 2 seconds for testing (change to longer time for production)
    timerRef.current = setInterval(captureImage, 2000);
  };

  // Capture image from video stream
  const captureImage = () => {
    if (!videoRef.current || !isCapturing || !videoRef.current.videoWidth) return;

    const canvas = document.createElement('canvas');
    canvas.width = videoRef.current.videoWidth;
    canvas.height = videoRef.current.videoHeight;
    
    const ctx = canvas.getContext('2d');
    ctx.drawImage(videoRef.current, 0, 0, canvas.width, canvas.height);
    
    const imageData = canvas.toDataURL('image/jpeg', 0.8);
    const timestamp = new Date().toLocaleTimeString();
    
    setImages(prevImages => [...prevImages, { data: imageData, time: timestamp }]);
    
    // Save to Chrome storage
    if (typeof chrome !== 'undefined' && chrome.storage) {
      chrome.storage.local.get("images", (data) => {
        const storedImages = data.images || [];
        storedImages.push({ data: imageData, time: timestamp });
        chrome.storage.local.set({ images: storedImages });
      });
    }
  };

  // Clean up on component unmount
  useEffect(() => {
    return () => {
      stopCamera();
    };
  }, []);

  const openCameraSettings = () => {
    // This will show how to open Chrome's camera settings in a new tab
    if (chrome && chrome.tabs) {
      chrome.tabs.create({ url: 'chrome://settings/content/camera' });
    } else {
      window.open('chrome://settings/content/camera', '_blank');
    }
  };

  return (
    <div style={{ padding: "16px", maxWidth: "400px", margin: "0 auto" }}>
      <h1 style={{ fontSize: "20px", fontWeight: "bold", marginBottom: "16px", textAlign: "center" }}>
        Webcam Capture Extension
      </h1>
      
      {error && (
        <div style={{ 
          backgroundColor: "#FEE2E2", 
          border: "1px solid #F87171", 
          color: "#B91C1C", 
          padding: "10px", 
          marginBottom: "16px", 
          borderRadius: "4px" 
        }}>
          {error}
        </div>
      )}
      
      <div style={{ marginBottom: "16px", textAlign: "center" }}>
        {isCapturing ? (
          <button 
            onClick={stopCamera} 
            style={{ 
              backgroundColor: "#EF4444", 
              color: "white", 
              padding: "10px 20px", 
              borderRadius: "4px", 
              border: "none", 
              cursor: "pointer",
              fontSize: "16px"
            }}
          >
            Stop Camera
          </button>
        ) : (
          <button 
            onClick={startCamera} 
            style={{ 
              backgroundColor: "#3B82F6", 
              color: "white", 
              padding: "10px 20px", 
              borderRadius: "4px", 
              border: "none", 
              cursor: "pointer",
              fontSize: "16px"
            }}
          >
            Enable Camera
          </button>
        )}
      </div>
      
      {isCapturing && (
        <div style={{ 
          marginBottom: "16px", 
          backgroundColor: "#F3F4F6", 
          padding: "8px", 
          borderRadius: "4px" 
        }}>
          <video 
            ref={videoRef} 
            autoPlay 
            playsInline 
            muted 
            style={{ width: "100%", height: "auto", borderRadius: "4px" }}
          />
        </div>
      )}
      
      {error && (
        <div style={{ textAlign: "center", marginBottom: "16px" }}>
          <button
            onClick={openCameraSettings}
            style={{
              backgroundColor: "#6B7280",
              color: "white",
              padding: "8px 16px",
              borderRadius: "4px",
              border: "none",
              cursor: "pointer",
              fontSize: "14px"
            }}
          >
            Open Camera Settings
          </button>
        </div>
      )}
      
      {images.length > 0 && (
        <div>
          <h2 style={{ fontSize: "18px", fontWeight: "600", marginBottom: "8px" }}>Captured Images ({images.length}):</h2>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(2, 1fr)", gap: "8px" }}>
            {images.map((img, index) => (
              <div key={index} style={{ border: "1px solid #E5E7EB", borderRadius: "4px", padding: "4px" }}>
                <img 
                  src={img.data} 
                  alt={`Captured at ${img.time}`} 
                  style={{ width: "100%" }}
                />
                <p style={{ fontSize: "12px", textAlign: "center", marginTop: "4px" }}>{img.time}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default WebcamCapture;