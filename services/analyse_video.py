import mediapipe as mp
import cv2
import math

from mediapipe.python.solutions.pose import PoseLandmark as mp_pose
import cv2
import mediapipe as mp
import numpy as np
from utils.metrics import calculate_angle, get_body_lean_angle, get_crunch_angle


def analyze_video_metrics(file_path: str) -> dict:
    cap = cv2.VideoCapture(file_path)
    mp_pose_lib = mp.solutions.pose
    pose = mp_pose_lib.Pose(static_image_mode=False, min_detection_confidence=0.5)

    elbow_angles = []
    elbow_shifts = []
    knee_angles = []
    body_lean_angles = []
    crunch_angles = []

    person_detected = False 

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(image)

        if results.pose_landmarks:
            person_detected = True  
            lm = results.pose_landmarks.landmark

            try:
                right_elbow = calculate_angle(
                    lm[mp_pose.RIGHT_SHOULDER.value],
                    lm[mp_pose.RIGHT_ELBOW.value],
                    lm[mp_pose.RIGHT_WRIST.value],
                )
                elbow_angles.append(right_elbow)

                shoulder_x = lm[mp_pose.RIGHT_SHOULDER.value].x
                elbow_x = lm[mp_pose.RIGHT_ELBOW.value].x
                elbow_shift = abs(elbow_x - shoulder_x)
                elbow_shifts.append(elbow_shift)

                right_knee = calculate_angle(
                    lm[mp_pose.RIGHT_HIP.value],
                    lm[mp_pose.RIGHT_KNEE.value],
                    lm[mp_pose.RIGHT_ANKLE.value],
                )
                knee_angles.append(right_knee)

                lean_angle = get_body_lean_angle(
                    lm[mp_pose.LEFT_SHOULDER.value], lm[mp_pose.LEFT_HIP.value]
                )
                body_lean_angles.append(lean_angle)

                crunch_angle = get_crunch_angle(
                    lm[mp_pose.RIGHT_SHOULDER.value], lm[mp_pose.RIGHT_HIP.value]
                )
                crunch_angles.append(crunch_angle)

            except:
                continue

    cap.release()
    pose.close()

    if not person_detected:
        return []

    def safe_mean(arr):
        return round(float(np.mean(arr)), 2) if arr else 0.0

    metrics = {
        "avg_elbow_angle": safe_mean(elbow_angles),
        "avg_elbow_shift": safe_mean(elbow_shifts),
        "avg_knee_angle": safe_mean(knee_angles),
        "max_body_lean_angle": (
            round(max(body_lean_angles), 2) if body_lean_angles else 0.0
        ),
        "avg_crunch_angle": safe_mean(crunch_angles),
    }
    

    return metrics



