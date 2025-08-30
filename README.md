# Vehicle Detection and Counting using OpenCV

This project demonstrates vehicle detection and counting in a video using OpenCV and background subtraction. It processes a video file, detects moving vehicles, and counts them as they cross a defined line.

## Features
- Detects moving vehicles in a video stream
- Counts vehicles as they cross a virtual line
- Uses background subtraction and contour detection
- Displays real-time video with bounding boxes and counters

## Requirements
- Python 3.x
- OpenCV (`opencv-python`, `opencv-contrib-python`)
- NumPy

## Installation
1. Clone this repository or download the source code.
2. Install the required Python packages:
   ```bash
   pip install opencv-python opencv-contrib-python numpy
   ```

## Usage
1. Place your input video file as `video.mp4` in the project directory (or update the filename in `vehicle.py`).
2. Run the script:
   ```bash
   python vehicle.py
   ```
3. The script will display the video with detected vehicles and a counter.

## File Structure
- `vehicle.py` - Main script for vehicle detection and counting
- `video.mp4` - Input video file (replace with your own video if needed)
- `README.md` - Project documentation

## How it Works
- The script uses background subtraction to detect moving objects (vehicles).
- Contours are found and filtered by size to identify vehicles.
- When a vehicle's center crosses a predefined line, the counter is incremented.

## Customization
- To use a different video, change the filename in `vehicle.py`:
  ```python
  cap = cv2.VideoCapture('your_video.mp4')
  ```
- Adjust `count_line_position`, `min_width_react`, and `min_height_react` for different video perspectives or vehicle sizes.

## License
This project is for educational purposes.
