import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# Path to the hand landmark model
MODEL_PATH = 'hand_landmarker.task'

# Define a callback function for asynchronous results in live stream mode
def hand_landmark_callback(result, output_image, timestamp_ms):
    if result.hand_landmarks:
        print(f"Detected {len(result.hand_landmarks)} hands.")
        for idx, hand_landmark in enumerate(result.hand_landmarks):
            print(f"Hand {idx + 1}:")
            for i, landmark in enumerate(hand_landmark):
                print(f"Landmark {i}: x={landmark.x}, y={landmark.y}, z={landmark.z}")
    else:
        print("No hands detected.")

# Initialize the MediaPipe Hand Landmarker
BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=MODEL_PATH),
    running_mode=VisionRunningMode.LIVE_STREAM,
    num_hands=2,  # Detect up to 2 hands
    min_hand_detection_confidence=0.5,
    min_hand_presence_confidence=0.5,
    min_tracking_confidence=0.5,
    result_callback=hand_landmark_callback
)

# Open the webcam
cap = cv2.VideoCapture(0)

# Check if the webcam is opened successfully
if not cap.isOpened():
    print("Error: Could not open the webcam.")
    exit()

# Use Hand Landmarker in live stream mode
with HandLandmarker.create_from_options(options) as landmarker:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame from webcam.")
            break

        # Convert the frame to an MP Image
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)

        # Process the frame and get the timestamp
        timestamp_ms = int(cap.get(cv2.CAP_PROP_POS_MSEC))
        landmarker.detect_async(mp_image, timestamp_ms)

        # Display the frame
        cv2.imshow("Hand Landmark Detection", frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release resources
cap.release()
cv2.destroyAllWindows()
