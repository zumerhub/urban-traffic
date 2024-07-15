import dotenv from 'dotenv'; 

const config = {
    db: {
        username: process.env.DB_USER,
        password: process.env.DB_PASSWORD,
        database: process.env.DB_NAME,
        host: process.env.DB_HOST,
        dialect: 'postgres',
        port: process.env.DB_PORT,  // Added DB_PORT
    },

    mqtt: {
        broker: process.env.MQTT_BROKER,
        port: process.env.MQTT_PORT,
        topic: process.env.MQTT_TOPIC,
    }
};

export default config