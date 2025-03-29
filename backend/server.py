from flask import Flask, request, jsonify
from flask_cors import CORS
from cv_model import detect_faces
import os

app = Flask(__name__)
CORS(app)

@app.route('/detect', methods=['GET'])
def detect():
    # Use request.args for GET parameters instead of request.json
    image_path = request.args.get('image', 'photo.jpg')
    
    # Check if image exists
    if not os.path.exists(image_path):
        return jsonify({
            "success": False,
            "error": f"Image not found: {image_path}"
        }), 404
    
    # Process the image and get results
    results = detect_faces(image_path, show_image=False)
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
