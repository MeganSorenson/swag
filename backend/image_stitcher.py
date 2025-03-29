from stitching import Stitcher
import os
import cv2

def stitch_images(folder_path):
    stitcher = Stitcher(detector="sift", confidence_threshold=0.2)
    
    # get all image path names ex: image.jpg from the folder_path
    image_paths = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(('.jpg', '.jpeg', '.png'))]
    print(image_paths)
    if len(image_paths) < 2:
        # save the single image called panorama.jpg (overwrite if exists)
        panorama = cv2.imread(image_paths[0])
    else:
        panorama = stitcher.stitch(image_paths)
    
    cv2.imwrite("panoramas/panorama.jpg", panorama)
    
    return "panoramas/panorama.jpg"
    