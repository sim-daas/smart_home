import cv2
import mediapipe as mp
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import json

# Initialize MediaPipe classes
BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

# Path to the Gesture Recognizer model
model_path = "gesture_recognizer.task"

# Function to display results on the frame
def display_results_on_image(image, gesture_recognition_result):
    if not gesture_recognition_result.gestures:
        return image

    # Get the gesture name and confidence score for the first detected hand
    gesture = gesture_recognition_result.gestures[0][0]
    gesture_name = gesture.category_name
    confidence = gesture.score

    # Add text to the frame
    cv2.putText(image, f"Gesture: {gesture_name} ({confidence:.2f})", (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    return image


# ROS2 Node for Gesture Recognition
class GesturePublisher(Node):
    def __init__(self):
        super().__init__('gesture_publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        self.get_logger().info('Gesture Publisher Node has been started.')

        # Initialize the Gesture Recognizer
        self.options = GestureRecognizerOptions(
            base_options=BaseOptions(model_asset_path=model_path),
            running_mode=VisionRunningMode.IMAGE,
        )
        self.recognizer = GestureRecognizer.create_from_options(self.options)

        # Open the webcam
        self.cap = cv2.VideoCapture(0)

    def run(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                self.get_logger().error("Failed to capture frame. Exiting...")
                break

            # Convert the frame to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Create MediaPipe Image object
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)

            try:
                # Perform gesture recognition
                gesture_recognition_result = self.recognizer.recognize(mp_image)

                # Display results on the frame
                frame = display_results_on_image(frame, gesture_recognition_result)

                # Publish detected gesture
                if gesture_recognition_result.gestures:
                    gesture = gesture_recognition_result.gestures[0][0]
                    gesture_data = gesture.category_name
                    self.publisher_.publish(String(data=gesture_data))
                    self.get_logger().info(f"Published: {gesture_data}")

            except Exception as e:
                self.get_logger().error(f"Error during gesture recognition: {e}")

            # Display the frame
            cv2.imshow("Gesture Recognition", frame)

            # Exit on pressing 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release resources
        self.cap.release()
        cv2.destroyAllWindows()
        self.recognizer.close()


def main(args=None):
    rclpy.init(args=args)
    node = GesturePublisher()

    try:
        node.run()
    except KeyboardInterrupt:
        node.get_logger().info("Node stopped by user.")

    rclpy.shutdown()


if __name__ == '__main__':
    main()
