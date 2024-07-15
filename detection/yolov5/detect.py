import torch
from PIL import Image
import cv2
import psycopg2
from datetime import datetime
import json

# Load YOLO model
def load_yolo_model():
    return torch.hub.load('ultralytics/yolov5', 'yolov5s')

# Object detection function
def detect_objects(model, image_path):
    img = Image.open(image_path)
    results = model(img)
    return results.pandas().xyxy[0].to_json(orient="records")

# Draw bounding boxes and save image
def draw_bounding_boxes(image_path, results):
    # Load image using OpenCV
    img = cv2.imread(image_path)
    
    # Convert BGR image to RGB
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Parse results
    detections = json.loads(results)
    
    for detection in detections:
        if detection['name'] == 'person':  # Only add bounding boxes for detected persons
            xmin, ymin, xmax, ymax = int(detection['xmin']), int(detection['ymin']), int(detection['xmax']), int(detection['ymax'])
            cv2.rectangle(img_rgb, (xmin, ymin), (xmax, ymax), (255, 0, 0), 2)  # Draw rectangle in RGB
        
    # Save the image with bounding boxes
    output_path = './images/detected_faces.jpg'
    cv2.imwrite(output_path, cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR))  # Convert back to BGR for saving
    return output_path

# Save results to PostgreSQL
def save_to_db(results):
    conn = psycopg2.connect(
        dbname="trafficdatabase",
        user="samuel",
        password="new_password",
        host="localhost"
    )
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id SERIAL PRIMARY KEY,
            event_type VARCHAR(50),
            description TEXT,
            timestamp TIMESTAMP
        )
    """)
    cur.execute("""
        INSERT INTO events (event_type, description, timestamp)
        VALUES (%s, %s, %s)
    """, ("congestion", results, datetime.now()))
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    # image_path = sys.argv[1]
    image_path = './images/man-and-woman.jpg'
    model = load_yolo_model()
    results = detect_objects(model, image_path)
    save_to_db(results)
    output_path = draw_bounding_boxes(image_path, results)
    print(f"Results: {results}")
    print(f"Output image saved at: {output_path}")
