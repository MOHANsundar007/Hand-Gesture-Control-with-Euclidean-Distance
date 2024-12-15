# Gesture Recognition Using Hand Landmarks

This project recognizes hand gestures using the MediaPipe library to detect hand landmarks and performs corresponding actions (such as keyboard input) based on the gesture detected.

### **Mathematical Concepts Used**

**Euclidean Distance**.

---

## 1. **Euclidean Distance**

The Euclidean distance is used to measure the distance between the thumb tip and other finger tips. This is important for detecting whether the hand is in an open or closed state.
The formula to calculate the Euclidean distance between two points \( P_1(x_1, y_1) \) and \( P_2(x_2, y_2) \) is:
$$
\text{Distance}(P_1, P_2) = \sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2}
$$

- If the distance between the thumb and other finger tips is large (greater than 60 pixels), the hand is classified as **Open Hand**.
- If the distance is small (less than 60 pixels), the hand is classified as **Closed Fist**.

---

## **Gesture Classifications**

Based on the calculations of distances, the following gestures are recognized:

1. **Open Hand Gesture**: If the distance between the thumb and each of the other fingers is large (more than 60 pixels), the hand is considered open.
2. **Closed Fist Gesture**: If the distance between the thumb and other fingers is small (less than 60 pixels), the hand is considered closed into a fist.

These gestures are detected in real-time using the MediaPipe Hand model, and corresponding actions are performed, such as pressing keyboard keys (e.g., left, right).

---
Output:
![gestureproof](https://github.com/user-attachments/assets/b03e19fe-42b0-4c06-bb7f-dfea4f1e21e3)


## **Libraries Used**

- **OpenCV**: For capturing and displaying video frames.
- **MediaPipe**: For detecting and drawing hand landmarks.
- **Pynput**: For simulating keyboard inputs based on hand gestures.

---

## **How to Run the Code**

1. Install the required libraries:

    ```bash
    pip install opencv-python mediapipe pynput
    ```

2. Run the script. It will use your webcam to detect hand gestures.

3. The following gestures are mapped to specific keyboard keys:
    - **Open Hand**: Right arrow
    - **Closed Fist**: Left arrow

4. Press the **"q"** key to exit the video feed.

