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
    *   **ROS2:** Install ROS2 Humble on both the laptop and the Raspberry Pi. Follow the ROS2 installation guide: [https://docs.ros.org/en/humble/Installation.html](https://docs.ros.org/en/humble/Installation.html). You can use the "ROS 2 base install" for simplicity.
    *   **Docker:** Install Docker on the Raspberry Pi. Follow the Docker installation guide for your system.
    *   **MediaPipe:** Install the necessary Python packages on the laptop as mentioned in the `requirements.txt` file (see installation instructions below).

##### **2.2. Installation Instructions**

1.  **Laptop (Gesture Recognition Node):**
    *   **Install ROS2 Humble (Base Install):** Follow the official ROS2 Humble installation guide for your operating system (Ubuntu is recommended for ease of use with ROS2): [https://docs.ros.org/en/humble/Installation.html](https://docs.ros.org/en/humble/Installation.html). Make sure to do the *base install*.
    *   **Install Python Dependencies:**
        ```bash
        git clone https://github.com/sim-daas/smart_home
        cd smart_home
        pip3 install -r requirements.txt
        ```

2.  **Raspberry Pi (Subscriber Node):**
    *   **Install Docker:** Follow the official Docker installation guide for your system: [https://docs.docker.com/engine/install/](https://docs.docker.com/engine/install/)
    *   **Install ROS2 Packages (If not already installed):** This step should not be required since we are using Docker on Raspberry Pi.

##### **2.3. Networking Setup**

*   Ensure that both the laptop and Raspberry Pi are connected to the **same network**. This can be a local Wi-Fi network.

#### **3. Running the System**

##### **3.1. ROS2 Docker Container (Raspberry Pi)**

1.  **Create a Dockerfile: (inside the clones repository)**
    ```dockerfile
    FROM ros:humble-ros-base

    RUN apt-get update && apt-get install -y python3-pip

    RUN pip3 install rpi_gpio

    WORKDIR /app
    COPY rasp_final.py /app

    CMD ["/bin/bash", "-c", "source /opt/ros/humble/setup.bash && python3 rasp_final.py"]
    ```
2. **Build the image**
   ```bash
    git clone https://github.com/sim-daas/smart_home
    cd smart_home
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
    source /opt/ros/humble/setup.bash
    ```
2.  **Run the Gesture Publisher on your Laptop**
    ```bash
    source /opt/ros/humble/setup.bash
    cd smart_home
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
*   It is recommended to use the "ROS 2 base install" when setting up ROS on your system to avoid potential conflicts with the full desktop install

#### **7. Future Plans**

*  Add logic within `rasp_final.py` to control the LED strip based on clapping data
