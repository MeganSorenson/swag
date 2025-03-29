import cv2
import numpy as np
from datetime import datetime

def add_and_crop_image(files):
    newImage = None
    
    # Check if an image was uploaded
    if 'image' in files:
        file = files['image']
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
    