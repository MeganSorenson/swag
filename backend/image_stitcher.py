from stitching import Stitcher

def stitch_images(folder_path):
    stitcher = Stitcher(detector="sift", confidence_threshold=0.2)
    
    # get all image path names ex: image.jpg from the folder_path
    image_paths = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(('.jpg', '.jpeg', '.png'))]
    panorama = stitcher.stitch(image_paths)
    
    return panorama
    