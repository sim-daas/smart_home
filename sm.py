import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# Initialize MediaPipe utilities
BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# Path to the hand landmarker model
model_path = 'hand_landmarker.task'

# Configure the hand landmarker
options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.IMAGE,  # Set to IMAGE mode for simplicity
    num_hands=2,
    min_hand_detection_confidence=0.5,
    min_hand_presence_confidence=0.5
)

# Create the hand landmarker instance
with HandLandmarker.create_from_options(options) as landmarker:
    # Start capturing video from the webcam
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame. Exiting.")
            break

        # Convert frame to RGB as MediaPipe expects
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)

        # Perform hand landmarks detection
        try:
            result = landmarker.detect(mp_image)

            # Draw landmarks on the frame
            if result.hand_landmarks:
                for idx, hand_landmark in enumerate(result.hand_landmarks):
                    print(f"Hand {idx + 1}:")
                    for i, landmark in enumerate(hand_landmark):
                        print(f"Landmark {i}: x={landmark.x}, y={landmark.y}, z={landmark.z}")

                    # Draw landmarks on the image
                    mp_drawing.draw_landmarks(
                        frame,
                        hand_landmark,
                        mp.solutions.hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style(),
                    )
        except Exception as e:
            print(f"Error during detection: {e}")

        # Display the frame with landmarks
        cv2.imshow("Hand Landmarks", frame)

        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()
