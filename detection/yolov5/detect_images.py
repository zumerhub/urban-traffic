import torch
import cv2
import json
from datetime import datetime
import psycopg2
import paho.mqtt.client as mqtt

# MQTT configuration
MQTT_BROKER = "127.0.0.1"
MQTT_PORT = 1883
MQTT_TOPIC = "traffic/alerts"

print("paho-mqtt installed successfully!")

# Load YOLO model
def load_yolo_model():
    return torch.hub.load('ultralytics/yolov5', 'yolov5s')

# Object detection function for a single frame
def detect_objects(model, frame):
    results = model(frame)
    return results.pandas().xyxy[0].to_dict(orient="records")

# Function to save results to PostgreSQL
def save_to_db(vehicle_count, avg_speed, density, results):
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
            timestamp TIMESTAMP,
            vehicle_count INTEGER,
            avg_speed FLOAT,
            density FLOAT
        )
    """)
    for result in results:
        cur.execute("""
            INSERT INTO events (event_type, description, timestamp, vehicle_count, avg_speed, density)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (result['name'], json.dumps(result), datetime.now(), vehicle_count, avg_speed, density))
    conn.commit()
    cur.close()
    conn.close()

# Function to send MQTT notification
def send_notification(density):
    client = mqtt.Client()
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.publish(MQTT_TOPIC, json.dumps({"density": density, "timestamp": datetime.now().isoformat()}))
    client.disconnect()

# Function to draw bounding boxes, labels, vehicle count, and density on the frame
def draw_boxes(results, frame, vehicle_count, avg_speed, density):
    for result in results:
        xmin, ymin, xmax, ymax = int(result['xmin']), int(result['ymin']), int(result['xmax']), int(result['ymax'])
        label = result['name']
        confidence = result['confidence']

        # Draw bounding box
        cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (255, 0, 0), 2)
        # Put label and confidence
        cv2.putText(frame, f"{label} {confidence:.2f}", (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    # Draw horizontal line
    height, width, _ = frame.shape
    line_y = height // 2
    cv2.line(frame, (0, line_y), (width, line_y), (0, 255, 0), 2)
    # Put vehicle count, average speed, and density
    cv2.putText(frame, f"Vehicle Count: {vehicle_count}", (10, line_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
    cv2.putText(frame, f"Avg Speed: {avg_speed:.2f} km/h", (10, line_y + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
    cv2.putText(frame, f"Density: {density:.2f} vehicles/m", (10, line_y + 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

    return frame

# Function to calculate average speed (placeholder logic)
def calculate_avg_speed(results, time_elapsed):
    speeds = []
    for result in results:
        if result['name'] == 'car':  # Assuming 'car' is the class name for vehicles
            speeds.append(result['confidence'] * 60)  # Placeholder: confidence * 60 as speed
    if speeds:
        avg_speed = sum(speeds) / len(speeds)
    else:
        avg_speed = 0
    return avg_speed

# Function to calculate traffic density
def calculate_density(vehicle_count, frame_width):
    # Assuming a unit length of 1 meter for simplicity
    unit_length = 1
    density = vehicle_count / (frame_width / unit_length)
    return density

def main(video_path):
    model = load_yolo_model()
    cap = cv2.VideoCapture(video_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Define the codec and create VideoWriter object
    out = cv2.VideoWriter('output_video.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

    frame_count = 0
    detected_count = 0
    total_vehicle_count = 0
    avg_speed = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        if frame_count % 10 != 0:
            continue  # Process every 10th frame to speed up

        print(f"Processing frame {frame_count}")

        # Convert the frame from BGR to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Perform detection on the frame
        results = detect_objects(model, frame_rgb)

        if results:
            detected_count += 1
            vehicle_count = sum(1 for result in results if result['name'] == 'car')  # Count vehicles
            total_vehicle_count += vehicle_count
            avg_speed = calculate_avg_speed(results, 1 / fps)  # Placeholder time_elapsed = 1/fps
            density = calculate_density(vehicle_count, width)

            print(f"Detections in frame {frame_count}: {results}")
            save_to_db(vehicle_count, avg_speed, density, results)

            if density > 10:  # Threshold for high traffic density
                send_notification(density)
            # Draw bounding boxes, labels, vehicle count, average speed, and density on the frame
            frame = draw_boxes(results, frame, vehicle_count, avg_speed, density)

        # Write the frame into the file 'output_video.mp4'
        out.write(frame)

        # Optional: Display the frame
        cv2.imshow('Frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print(f"Processed {frame_count} frames, detected objects in {detected_count} frames")

if __name__ == "__main__":
    video_path = '/home/zumerhub/Downloads/TUBE2GO/youtube/video/cars-moving-on-road-stock-footage-free-download_video_1080p.mp4'
    main(video_path)
