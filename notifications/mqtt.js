import mqtt from 'mqtt';
import config from '../dataabase/config/config.js';
import dotenv from 'dotenv';
dotenv.config();


const client = mqtt.connect(`mqtt://localhost`);

client.on('connect', () => {
    console.log('MQTT client connected');
});

client.on('error', (err) => {
    console.error('MQTT client error:', err);
});

export function sendNotification(eventType) {
    if (client.connected) {
        client.publish(config.mqtt.topic, `Event detected: ${eventType}`, (err) => {
            if (err) {
                console.error('Error publishing message:', err);
            } else {
                console.log('Notification sent:', eventType);
            }
        });
    } else {
        console.error('MQTT client is not connected');
    }
}
