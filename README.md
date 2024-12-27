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


### **Smart Home Appliance Controller with ROS2**

This project implements a smart home appliance control system using hand gestures and a Raspberry Pi, leveraging ROS2 for communication. The system uses a webcam for gesture recognition and a Raspberry Pi for controlling a fan and LED lights.

#### **1. Overview**

The system is divided into the following components:

*   **Gesture Recognition (Laptop)**: Uses MediaPipe to recognize hand gestures via webcam, publishing recognized gestures to a ROS2 topic.
*   **Raspberry Pi Controller**: Subscribes to the gesture topic, translating recognized gestures into actions to control connected appliances.
*   **Appliance Control**: Manages a fan and LED light based on commands received from the gesture recognition system.

#### **2. System Setup**

##### **2.1. Prerequisites**

1.  **Hardware:**
    *   Laptop (for running the gesture recognition node)
    *   Raspberry Pi (for running the subscriber node and controlling peripherals)
    *   Webcam (for gesture recognition)
    *   Relay module
    *   Wires and jumper wires
    *   Mains supply for fan and LED lights
    *   Fan with speed control module (e.g., using a relay)
    *   LED strip or bulb
2.  **Software:**
    *   **Python:** Ensure Python 3.8+ is installed on both the laptop and Raspberry Pi.
    *   **ROS2:** Install ROS2 Foxy on both the laptop and the Raspberry Pi. Follow the ROS2 installation guide: [https://docs.ros.org/en/foxy/Installation.html](https://docs.ros.org/en/foxy/Installation.html)
    *   **Docker:** Install Docker on the Raspberry Pi. Follow the Docker installation guide for your system.
    *   **MediaPipe:** Install the necessary Python packages on the laptop as mentioned in the `requirements.txt` file (see installation instructions below).

##### **2.2. Installation Instructions**

1.  **Laptop (Gesture Recognition Node):**
    *   **Create a Virtual Environment (Optional but Recommended):**
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```
    *   **Install Python Dependencies:**
        ```bash
        pip install -r requirements.txt
        ```
    *   **Install ROS2 Packages (If not already installed):**
        ```bash
        sudo apt update
        sudo apt install ros-foxy-rclpy ros-foxy-std-msgs
        ```

2.  **Raspberry Pi (Subscriber Node):**
    *   **Install Docker:** Follow the official Docker installation guide for your system: [https://docs.docker.com/engine/install/](https://docs.docker.com/engine/install/)
    *   **Install ROS2 Packages (If not already installed):**
        ```bash
         sudo apt update
        sudo apt install ros-foxy-rclpy ros-foxy-std-msgs
        ```
    *   **Install Python Dependencies:**
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        pip install rpi_gpio
        ```

##### **2.3. Networking Setup**

*   Ensure that both the laptop and Raspberry Pi are connected to the **same network**. This can be a local Wi-Fi network.

#### **3. Running the System**

##### **3.1. ROS2 Docker Container (Raspberry Pi)**

1.  **Create a Dockerfile (optional):** For ease of future use, you can create a Dockerfile with the ROS and Python environment. Here's a sample:
    ```dockerfile
    FROM ros:foxy

    RUN apt-get update && apt-get install -y python3-pip
    RUN pip3 install rpi_gpio

    WORKDIR /app
    COPY rasp_final.py /app

    CMD ["/bin/bash", "-c", "source /opt/ros/foxy/setup.bash && python3 rasp_final.py"]
    ```
2. **Build the image**
   ```bash
    docker build -t ros_app .
    ```
3.  **Run the Docker Container:**
    ```bash
    docker run --privileged --net=host ros_app
    ```
    *   `--privileged`: Allows access to hardware, like GPIO pins.
    *   `--net=host`: Uses the host's network, required for ROS2 communication.

##### **3.2. Run ROS2 Nodes**

1.  **Start ROS2 Master on your Laptop**
    ```bash
    source /opt/ros/foxy/setup.bash
    ros2 run turtlesim turtlesim_node
    ```
2.  **Run the Gesture Publisher on your Laptop**
    ```bash
        source /opt/ros/foxy/setup.bash
        cd <path to your python scripts>
        python3 gesture-pub.py
    ```

3.  **Run the Subscriber Node on Raspberry Pi (Inside Docker container)**
    The subscriber node will start automatically when the Docker container is run in 3.1.

#### **4. Code Description**

*   `gesture-pub.py`: This script captures video from the webcam, recognizes hand gestures using MediaPipe, and publishes the recognized gesture to the `topic` ROS2 topic.
*   `rasp_final.py`: This script runs on the Raspberry Pi. It subscribes to the `topic` ROS2 topic and processes the incoming data to control GPIO pins which are connected to relays.
*   `gesture-det.py` This script runs the mediapipe gesture detection from the video frame.
*    `hand-landmarkdet.py` This script runs the mediapipe hand landmark detection from the video frame.

#### **5. Appliance Control Logic**

*   **Fan Speed Control (Implemented in `rasp_final.py`):**
    *   When a "Thumb_Up" gesture is received, the GPIO pin connected to a relay is set HIGH, enabling power to the fan.
    *   When a "Closed_Fist" gesture is received, the GPIO pin is set LOW, stopping the fan
*   **LED Light Control (To be Implemented in `rasp_final.py`):**
    *   You'll need to add logic within `rasp_final.py` to control the LED strip based on clap data you'll receive from another topic when you integrate that part.

#### **6. Important Notes**

*   Ensure all necessary dependencies are installed.
*   Verify network connectivity between the laptop and Raspberry Pi.
*   Adjust the GPIO pin in `rasp_final.py` to match your wiring setup.

This setup provides a foundation for building more complex smart home controls. By integrating clap detection, you can extend the system further
