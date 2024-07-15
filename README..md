# Urban-traffic

1. Run `npm install`
2. Run `npm start`
3. Add your own database credentials to `database/index.js`

To use YOLOv5 with PyTorch, you need to install several dependencies, including torch and torchvision. These libraries are required for loading and utilizing the YOLOv5 model.

Here are the steps to install these dependencies:

1. pip install torch torchvision.

## GPU Version

If you have an NVIDIA GPU and CUDA installed, you'll want to install a version of PyTorch that supports CUDA. Visit the PyTorch website to get the exact command for your CUDA version. Here are examples for different CUDA versions:

CUDA 11.8:
2. pip install torch torchvision torchaudio --index-url <https://download.pytorch.org/whl/cu118>

## Install Additional Dependencies

YOLOv5 requires additional libraries such as OpenCV for image processing:

pip install opencv-python-headless numpy pandas matplotlib

**Make sure you use PostgreSQL instead of MySQL for this code base.**
** Make sure you use postgreSQL instead of mySQL for this code base.
