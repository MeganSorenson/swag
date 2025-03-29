from flask import Flask, request, jsonify
from flask_cors import CORS
from cv_model import detect_faces
from image_stitcher import stitch_images
import os

app = Flask(__name__)
CORS(app)

@app.route('/detect', methods=['GET'])
def detect():
    panorama_path = stitch_images("images")
    results = detect_faces(panorama_path)
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
