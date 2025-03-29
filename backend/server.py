from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from cv_model import detect_faces
from image_stitcher import stitch_images
import os
import cv2
import numpy as np
from datetime import datetime

app = Flask(__name__)
CORS(app)

@app.route('/detect', methods=['POST'])
def detect():
    # Variable to store uploaded image (if any)
    newImage = None
    
    # Check if an image was uploaded
    if 'image' in request.files:
        file = request.files['image']
        if file.filename != '':
            # Read the image file
            file_bytes = file.read()
            
            # Convert to numpy array for OpenCV processing
            nparr = np.frombuffer(file_bytes, np.uint8)
            newImage = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            # For demonstration, print the image dimensions
            if newImage is not None:
                print(f"Received image with dimensions: {newImage.shape}")
                # get current timestamp string
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                # save new image to images folder
                cv2.imwrite("images/newImage" + timestamp + ".jpg", newImage)
    
    # Create panorama from images in the images folder
    panorama_path = stitch_images("images")
    
    # Detect objects in the panorama and save the detection image to the detections folder
    results = detect_faces(panorama_path, save_image=True)
    
    # Add the detection image URL to the response for frontend access
    if "image_path" in results and results["image_path"]:
        # Convert to relative URL path that can be accessed via the API
        results["image_url"] = f"/images/{os.path.basename(results['image_path'])}"
    
    return jsonify(results)

@app.route('/reset', methods=['GET'])
def reset():
    # delete all images in the images folder
    for file in os.listdir("images"):
        os.remove(os.path.join("images", file))
    # delete all images in the detections folder
    for file in os.listdir("detections"):
        os.remove(os.path.join("detections", file))
    # delete all images in the panoramas folder
    for file in os.listdir("panoramas"):
        os.remove(os.path.join("panoramas", file))
    return jsonify({"message": "Images reset"})

if __name__ == '__main__':
    app.run(debug=True)
