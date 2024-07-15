import express from 'express';
import { detectObjects } from './detection/objectDectection.js';
import { sendNotification } from './notifications/mqtt.js';
import path from 'path';

// import Event from './dataabase/models/Event.js';
import dotenv from 'dotenv';
import { fileURLToPath } from 'url';

dotenv.config();

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const PORT = process.env.PORT || 3000;


app.get('/detect', async (req, res) => {

    res.send("Hello is running")

    // traffic video path
    const imagePath = path.join(__dirname, './images/man-and-woman.jpg');
    // const imagePath = path.join(__dirname, '../../Downloads/TUBE2GO/youtube/video/cars-moving-on-road-stock-footage-free-download_video_1080p.mp4');
    // const imagePath = path.join(__dirname, 'home/zumerhub/Downloads/TUBE2GO/youtube/cars-moving-on-road-stock-footage-free-download_video_1080p.mp4');
    try {
        const results = await detectObjects(imagePath);
        console.log('Detection results:', results);
        // const parsedResults = await detectObjects(imagePath);
    
        // for (const result of parsedResults) {
        for (const result of results) {
          const eventType = determineEventType(result);  // Function to map result to event type
          await Event.create({ eventType });
          sendNotification(eventType);
        }

        res.send(parsedResults);
      } catch (error) {
        console.error('Error during detection:', error);
        res.status(500).send('Error during detection');
      }
  
});

function determineEventType(result) {
    // logic to determine event type based on detection result
    if (result.class === 'car' && result.confidence > 0.5) {
        return 'Congestion';
    } else if (result.class === 'accident' && result.confidence > 0.5) {
        return 'Accident';
    }
// Add more conditions as needed
    return 'Unknown';
}

app.listen(PORT, () => {
    console.log(`Server listening at PORT:${PORT}`);

})
