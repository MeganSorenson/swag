from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from cv_model import detect_faces
from image_stitcher import stitch_images
import os

app = Flask(__name__)
CORS(app)

@app.route('/detect', methods=['GET'])
def detect():
    # Create panorama from images in the images folder
    panorama_path = stitch_images("images")
    
    # Detect objects in the panorama and save the detection image to the detections folder
    results = detect_faces(panorama_path, save_image=True)
    
    # Add the detection image URL to the response for frontend access
    if "image_path" in results and results["image_path"]:
        # Convert to relative URL path that can be accessed via the API
        results["image_url"] = f"/images/{os.path.basename(results['image_path'])}"
    
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
