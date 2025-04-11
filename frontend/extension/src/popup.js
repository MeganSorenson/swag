const video = document.getElementById("video");
const canvas = document.getElementById("canvas");
const imageContainer = document.getElementById("image-container");
const startBtn = document.getElementById("start-btn");

let stream;
let captureInterval;

startBtn.addEventListener("click", async () => {
  try {
    stream = await navigator.mediaDevices.getUserMedia({ video: true });

    // Display the webcam feed
    video.srcObject = stream;

    // Capture images every 2 seconds
    captureInterval = setInterval(captureImage, 2000);
  } catch (error) {
    console.error("Error accessing webcam:", error);
    alert("Please allow webcam access.");
  }
});

function captureImage() {
  if (!canvas || !video) return;

  const ctx = canvas.getContext("2d");
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

  const imageData = canvas.toDataURL("image/png");

  // Display the image
  const img = new Image();
  img.src = imageData;
  img.classList.add("thumbnail");
  imageContainer.appendChild(img);

  // Save to local storage (optional)
  chrome.storage.local.get("images", (data) => {
    const images = data.images || [];
    images.push(imageData);
    chrome.storage.local.set({ images });
  });
}

// Clean up when the extension closes
window.addEventListener("unload", () => {
  if (stream) {
    stream.getTracks().forEach(track => track.stop());
  }
  if (captureInterval) {
    clearInterval(captureInterval);
  }
});