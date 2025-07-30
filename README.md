# AI Virtual Mouse Using Hand Gestures

An AI-powered virtual mouse system that uses real-time hand gesture recognition to perform mouse actions — like move cursor, left/right/double-click, and scroll — without any physical device.
Built with MediaPipe, OpenCV, PyAutoGUI, and Streamlit for a smooth, privacy-conscious, and user-friendly experience.

---

## Table of Contents

- [📌 Features](#-features)
- [🧑‍💻 Technologies Used](#-technologies-used)
- [🖥️ System Architecture](#️-system-architecture)
- [🚀 How to Run Locally](#-how-to-run-locally)
- [🧠 Gesture Recognition Logic](#-gesture-recognition-logic)
- [📊 Performance Metrics](#-performance-metrics)
- [📸 Screenshots](#-screenshots)
- [🎓 Project Team](#-project-team)
- [📁 Paper & Presentation](#-paper--presentation)
- [🔐 Privacy & Ethics](#-privacy--ethics)
- [🌱 Future Enhancements](#-future-enhancements)

---

## Features

- Real-Time Hand Tracking (21 landmarks using MediaPipe)
- Smooth Cursor Movement (via Kalman Filter logic)
- Rule-Based Gesture Recognition
  -  Index Finger Up → Left Click
  -  Thumb Up → Right Click
  -  Pinch (Thumb + Index) → Double Click
  -  Two-Finger Gestures → Scroll Up/Down
-  Dynamic Gesture Mapping UI (via Streamlit)
-  Adjustable Sensitivity Slider
-  Multi-Hand Gesture Support (Left + Right hands)
-  No physical device or special hardware needed
-  Privacy-safe: No cloud processing, runs locally

---

## 🧑‍💻 Technologies Used

| Tool/Library     | Purpose                                |
|------------------|----------------------------------------|
| MediaPipe        | Hand landmark detection (21 points)    |
| OpenCV           | Webcam feed and image preprocessing    |
| PyAutoGUI        | Virtual mouse control on screen        |
| Streamlit        | Interactive GUI for demo + mapping     |
| PIL              | Background image display               |
| Base64           | Background image encoding for UI       |

---

## System Architecture

```plaintext
             +----------------+
             |   Webcam Feed  |
             +----------------+
                     ↓
            [OpenCV Frame Capture]
                     ↓
       [MediaPipe → Hand Landmark Extraction]
                     ↓
      [Rule-Based Logic + Euclidean Distances]
                     ↓
     ┌────────────┬────────────┬────────────┐
     │ Move Cursor│ Left/Right │  Scroll    │
     │ (Index tip)│ Clicks     │  Actions   │
     └────────────┴────────────┴────────────┘
                     ↓
          [PyAutoGUI → System Control]
                     ↓
          [Streamlit GUI → Visualization]


## How to Run Locally (Windows/Linux)

⚠️ Important: This project is designed for local execution only (due to webcam + GUI control).
Hosting on cloud is not supported.
This app must be run locally due to webcam and OS-level control.

## Gesture Recognition Logic

| Gesture               | Condition                                              | Action       |
| --------------------- | ------------------------------------------------------ | ------------ |
| Index Finger Up       | y\_tip(8) < y\_dip(7)                                  | Left Click   |
| Thumb Up              | y\_tip(4) < y\_ip(3) +                                 | x4 - x8      |
| Pinch                 | Distance(Thumb Tip ↔ Index Tip) < 0.05                 | Double Click |
| Two-Finger Swipe Up   | Middle tip.y < Index tip.y – 0.1 (Stable for N frames) | Scroll Up    |
| Two-Finger Swipe Down | Middle tip.y > Index tip.y + 0.1 (Stable for N frames) | Scroll Down  |


## Performance Metrics

| Metric                    | Our System | Leap Motion | Logitech Gesture |
| ------------------------- | ---------- | ----------- | ---------------- |
| Gesture Accuracy          | 95.2%      | 97.5%       | 95.1%            |
| Low Light Accuracy        | 91.5%      | 84.3%       | 82.0%            |
| Latency                   | 110 ms     | 180 ms      | 150 ms           |
| Max Tracking Distance     | 1.8 meters | 0.6 meters  | 1.2 meters       |


## Screenshots



## Paper & Presentation

## Paper & Presentation

| Type                     | File                                                      |                                                                                         
| ------------------------ | ----------------------------------------------------------|
| IEEE Format Paper        | [`/docs/AI_Virtual_Mouse_Paper.docx`](dhttps://drive.google.com/drive/folders/1wWFmO2rd7bHRMJisd8dz3h0C-BxTPjGj?usp=sharing)|
| Final Presentation       | [`/docs/AI_Virtual_Mouse_Presentation.pdf`](https://drive.google.com/drive/folders/1wWFmO2rd7bHRMJisd8dz3h0C-BxTPjGj?usp=sharing) |
| Demo Video               | [Watch on YouTube](#) *(Add link)*                        |


## Privacy & Ethics

- All processing is done locally.
- No gesture images or webcam data are sent to any external server.
- Ideal for use in privacy-sensitive environments like healthcare or education.

## Future Enhancements

- Voice + Gesture Hybrid Input
- Deep Learning Model (CNN + LSTM / ResNet50)
- Sign Language Recognition Module
