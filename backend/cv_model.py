from inference.models.utils import get_roboflow_model
import cv2
import os
import time

def detect_faces(image_path, save_image=True):
    """
    Detect objects in an image using the Roboflow model.
    
    Args:
        image_path (str): Path to the image file
        save_image (bool): Whether to save the annotated image to the detections folder
        
    Returns:
        dict: Dictionary containing detection results and path to saved image
    """
    # Roboflow model
    model_name = "artai3"
    model_version = "2"

    # Get the API key from environment variable
    api_key = os.environ.get("ROBOFLOW_API_KEY")
    if not api_key:
        raise ValueError("ROBOFLOW_API_KEY environment variable not set")

    # Get Roboflow face model (this will fetch the model from Roboflow)
    model = get_roboflow_model(
        model_id="{}/{}".format(model_name, model_version),
        api_key=api_key
    )

    # Load image with opencv
    frame = cv2.imread(image_path)
    if frame is None:
        return {"error": f"Could not load image from {image_path}"}

    # Inference image to find objects
    results = model.infer(image=frame,
                          confidence=0.4,
                          iou_threshold=0.5)
    
    # Prepare response data
    detections = []
    
    # Plot all predictions on the image
    if results[0].predictions:
        print(f"Found {len(results[0].predictions)} predictions")
        
        # Define a list of colors for different predictions
        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), 
                (255, 0, 255), (0, 255, 255), (128, 0, 0), (0, 128, 0)]
        
        for i, prediction in enumerate(results[0].predictions):
            print(f"Prediction {i+1}:", prediction)
            
            # Get color for this prediction (cycle through colors if needed)
            color = colors[i % len(colors)]
            
            x_center = int(prediction.x)
            y_center = int(prediction.y)
            width = int(prediction.width)
            height = int(prediction.height)

            # Calculate top-left and bottom-right corners from center, width, and height
            x0 = x_center - width // 2
            y0 = y_center - height // 2
            x1 = x_center + width // 2
            y1 = y_center + height // 2
            
            # Add to detections response
            detection = {
                "id": i,
                "bbox": {
                    "x0": x0,
                    "y0": y0,
                    "x1": x1,
                    "y1": y1,
                    "width": width,
                    "height": height
                },
                "confidence": float(prediction.confidence) if hasattr(prediction, 'confidence') else None,
                "class": prediction.class_name if hasattr(prediction, 'class_name') else f"Object {i+1}"
            }
            detections.append(detection)
            
            # Draw rectangle and label on the image
            cv2.rectangle(frame, (x0, y0), (x1, y1), color, 3)
            
            # Add confidence score to label if available
            label = f"Object {i+1}"
            if hasattr(prediction, 'class_name') and prediction.class_name:
                label = prediction.class_name
            if hasattr(prediction, 'confidence'):
                label += f" ({prediction.confidence:.2f})"
                
            cv2.putText(frame, label, (x0, y0 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
    else:
        print("No predictions found")

    # Save the image with detections to the detections folder
    if save_image:
        cv2.imwrite("detections/detection.jpg", frame)
    
    # Return detection results with path to the saved image
    return {
        "success": True,
        "count": len(detections),
        "detections": detections,
        "image_path": "detections/detection.jpg" if save_image else None
    }