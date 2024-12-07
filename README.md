### **Smart House Appliances Controller Overview**

#### **1. Input Systems**
- **Gesture Recognition**:
  - Implemented using the Mediapipe library.
  - Captures hand gestures through a webcam and maps them to specific appliance commands.
  - Runs as a ROS2 publisher node on the laptop.

- **Clap Detection**:
  - Powered by Google Teachable Machine for sound-based classification.
  - Identifies single or double claps and maps them to appliance actions.
  - Runs as another ROS2 publisher node on the laptop.

#### **2. Data Processing**
- Both gesture recognition and clap detection nodes publish processed data (e.g., `gesture: increase_speed`, `clap: toggle_light`) to separate ROS2 topics.

#### **3. Data Communication**
- A **Raspberry Pi** subscribes to the ROS2 topics:
  - **Gesture Data Topic**: Commands related to fan control.
  - **Clap Data Topic**: Commands to toggle LED lights.

#### **4. Appliance Control**
- **Fan Speed Control**:
  - Adjusts speed based on recognized gestures (e.g., palm up increases speed, palm down decreases).

- **LED Light Control**:
  - Toggles lights on/off or changes colors based on detected clap patterns.

#### **5. Network Setup**
- The laptop and Raspberry Pi are on the same network, ensuring seamless ROS2 communication.

#### **6. Demo Setup**
- A small fan connected to the Raspberry Pi with a speed-controlling module.
- LED strip or bulb connected to the Raspberry Pi for light control.
