import { spawn } from 'child_process';
import path from 'path';

export function detectObjects(imagePath) {
    return new Promise((resolve, reject) => {
        const scriptPath = path.join(__dirname, 'yolov5', 'detect.py');
        const pythonProcess = spawn('python3', [scriptPath, imagePath]);

        pythonProcess.stdout.on('data', (data) => {
            try {
                resolve(JSON.parse(data.toString()));
            } catch (error) {
                reject(new Error(`Failed to parse JSON: ${error.message}`));
            }
        });

        pythonProcess.stderr.on('data', (data) => {
            reject(new Error(data.toString()));
        });

        pythonProcess.on('close', (code) => {
            if (code !== 0) {
                reject(new Error(`Python script exited with code ${code}`));
            }
        });
    });
}

export default {
    detectObjects
};


