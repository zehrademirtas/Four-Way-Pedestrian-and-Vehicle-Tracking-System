# Four-Way-Pedestrian-and-Vehicle-Tracking-System
This project implements an image processing algorithm to track pedestrians and vehicles at four-way intersections. The primary goal is to detect whether pedestrians and vehicles follow predefined paths correctly and identify violations.
# **Four-Way Pedestrian and Vehicle Tracking System**  

## **Project Description**  
This project is designed to track pedestrians and vehicles at four-way intersections using image processing techniques. The main objective is to monitor traffic behavior, ensure compliance with predefined paths, and detect violations in real-time.  

By leveraging video analysis and object detection, the system can determine whether pedestrians and vehicles follow the designated paths and take necessary actions when a violation occurs. Users can manually set paths for both pedestrians and vehicles to customize the system’s behavior.  

This project is particularly useful for **traffic monitoring, urban planning, and intelligent transportation systems**.  

---

## **Technologies Used**  
The system is built using:  
- **Python** – Core programming language.  
- **OpenCV (cv2)** – Used for image processing, object detection, and motion tracking.  
- **NumPy** – For numerical operations and handling image data.  

Future enhancements may incorporate **machine learning models** for more advanced object classification.  

---

## **Features**  

### ✅ **Video Processing & Motion Detection**  
- Loads and analyzes video files frame by frame.  
- Detects movement by processing only the changing parts of the scene.  

### ✅ **Object Detection & Classification**  
- Identifies objects in the video and classifies them as **pedestrians** or **vehicles**.  
- Uses size, shape, and movement patterns for classification.  
- Calculates speed for each detected object.  

### ✅ **Violation Detection**  
- Allows users to **manually define paths** for pedestrians and vehicles.  
- Compares detected objects with the predefined paths.  
- Flags an object as a **violation** if it moves outside its designated area.  

### ✅ **Real-Time Tracking**  
- Assigns a **unique ID** to each detected object.  
- Tracks objects across frames, preventing duplicate detections.  
- Detects **lost objects** and analyzes their past movements.  

### ✅ **User Interaction**  
- Users can **define paths manually** while the video is playing.  
- **Press '1'** to draw a **pedestrian path**.  
- **Press '2'** to draw a **vehicle path**.  
- **Press 'r'** to replay the video.  

### ✅ **Results & Outputs**  
- Displays detected **pedestrians and vehicles** on the screen.  
- Visualizes **violations** by marking them on the video.  
- Can be integrated with **traffic control systems** for automated responses.  

---

## **Installation & Setup**  

### **Requirements**  
Ensure you have **Python** installed, along with the necessary dependencies. Install them using:  

```bash
pip install opencv-python numpy
```

## **Conclusion**
his project showcases a real-time tracking system for pedestrians and vehicles, offering a practical approach for traffic monitoring and violation detection. By leveraging image processing and object tracking, it provides an effective tool for studying traffic patterns and enhancing road safety.
