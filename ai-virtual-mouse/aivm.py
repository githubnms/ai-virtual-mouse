import streamlit as st
import cv2
import mediapipe as mp
import pyautogui
from PIL import Image
import os
import base64

# Function to encode image to Base64
def get_base64_encoded_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

# Set background image
def set_background_image(image_path=None, encoded_image=None):
    if encoded_image:
        bg_url = f"data:image/jpeg;base64,{encoded_image}"
    elif image_path:
        bg_url = image_path
    else:
        bg_url = "lightgray"  # Default fallback color

    st.markdown(
        f"""
        <style>
        [data-testid="stAppViewContainer"] {{
            background-image: url("{bg_url}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Virtual Mouse Logic
def start_virtual_mouse():
    global mouse_sensitivity
    cap = cv2.VideoCapture(0)
    screen_width, screen_height = pyautogui.size()

    if not cap.isOpened():
        st.error("Failed to access the camera.")
        return

    # Variables for scroll stability
    scroll_up_count = 0
    scroll_down_count = 0
    SCROLL_STABILITY_THRESHOLD = 5  # Number of consecutive frames to confirm a scroll

    frame_placeholder = st.empty()
    action_placeholder = st.empty()  # Placeholder to display actions in the app

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Extract landmarks
                index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                index_finger_dip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP]
                thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                thumb_ip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP]
                middle_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]

                # Cursor movement (scaled to screen resolution)
                cursor_x = int(index_finger_tip.x * screen_width)
                cursor_y = int(index_finger_tip.y * screen_height)
                pyautogui.moveTo(cursor_x, cursor_y, duration=0.1 / mouse_sensitivity)

                # Gesture recognition logic
                # Index Finger Up: Left Click
                if index_finger_tip.y < index_finger_dip.y:
                    if gesture_actions["Index Finger Up"] == "left_click":
                        print("Action: Left Click")  # Log in terminal
                        action_placeholder.text("Action: Left Click")  # Display in app
                        pyautogui.click()

                # Thumb Up: Right Click
                if thumb_tip.y < thumb_ip.y and abs(thumb_tip.x - index_finger_tip.x) > 0.1:
                    if gesture_actions["Thumb Up"] == "right_click":
                        print("Action: Right Click")  # Log in terminal
                        action_placeholder.text("Action: Right Click")  # Display in app
                        pyautogui.rightClick()

                # Pinch: Double Click
                if abs(index_finger_tip.x - thumb_tip.x) < 0.05 and abs(index_finger_tip.y - thumb_tip.y) < 0.05:
                    if gesture_actions["Pinch"] == "double_click":
                        print("Action: Double Click")  # Log in terminal
                        action_placeholder.text("Action: Double Click")  # Display in app
                        pyautogui.doubleClick()

                # Two-Finger Swipe Up: Scroll Up
                if middle_finger_tip.y < index_finger_tip.y - 0.1:
                    scroll_up_count += 1
                    scroll_down_count = 0  # Reset down counter
                    if scroll_up_count >= SCROLL_STABILITY_THRESHOLD:
                        if gesture_actions["Two-Finger Swipe Up"] == "scroll_up":
                            print("Action: Scroll Up")  # Log in terminal
                            action_placeholder.text("Action: Scroll Up")  # Display in app
                            pyautogui.scroll(100)
                            scroll_up_count = 0  # Reset after scrolling
                else:
                    scroll_up_count = 0  # Reset up counter if condition fails

                # Two-Finger Swipe Down: Scroll Down
                if middle_finger_tip.y > index_finger_tip.y + 0.1:
                    scroll_down_count += 1
                    scroll_up_count = 0  # Reset up counter
                    if scroll_down_count >= SCROLL_STABILITY_THRESHOLD:
                        if gesture_actions["Two-Finger Swipe Down"] == "scroll_down":
                            print("Action: Scroll Down")  # Log in terminal
                            action_placeholder.text("Action: Scroll Down")  # Display in app
                            pyautogui.scroll(-100)
                            scroll_down_count = 0  # Reset after scrolling
                else:
                    scroll_down_count = 0  # Reset down counter if condition fails

        # Display the frame in Streamlit
        frame_placeholder.image(frame, channels="BGR", use_column_width=True)

        # Stop the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Initialize Mediapipe Hands
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Global variables
gesture_actions = {
    "Index Finger Up": "left_click",
    "Thumb Up": "right_click",
    "Pinch": "double_click",
    "Two-Finger Swipe Up": "scroll_up",
    "Two-Finger Swipe Down": "scroll_down"
}
mouse_sensitivity = 5

# Gesture Mapping Update
def update_gesture_mapping():
    global gesture_actions
    try:
        for key in gesture_var:
            gesture_actions[key] = gesture_var[key]
        st.session_state["status"] = "Gestures saved successfully!"
    except Exception as e:
        st.error(f"Failed to update gestures: {e}")

# Rest of the code remains unchanged...

# Streamlit App Layout
st.title("AI Virtual Mouse")

# Set background image
image_path = r"D:\menn\bg.jpg"  # Replace with your actual file path
encoded_image = get_base64_encoded_image(image_path)
set_background_image(encoded_image=encoded_image)

# Sidebar for settings
st.sidebar.header("Settings")
mouse_sensitivity = st.sidebar.slider("Mouse Sensitivity", 1, 10, 5)

# Gesture Customization
st.sidebar.subheader("Gesture Mapping")
gesture_var = {}
for gesture in gesture_actions.keys():
    gesture_var[gesture] = st.sidebar.selectbox(
        gesture,
        ["left_click", "right_click", "double_click", "scroll_up", "scroll_down"],
        index=["left_click", "right_click", "double_click", "scroll_up", "scroll_down"].index(gesture_actions[gesture])
    )

if st.sidebar.button("Save Gestures"):
    update_gesture_mapping()

# Status Bar
if "status" not in st.session_state:
    st.session_state["status"] = "Ready"
st.sidebar.info(st.session_state["status"])

# Start/Stop Virtual Mouse
if st.button("Start Virtual Mouse"):
    start_virtual_mouse()

if st.button("Exit"):
    st.stop()

