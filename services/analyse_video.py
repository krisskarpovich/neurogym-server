import mediapipe as mp
import cv2
import math

from mediapipe.python.solutions.pose import PoseLandmark as mp_pose
import cv2
import mediapipe as mp
import numpy as np
# from utils.metrics import calculate_angle, get_body_lean_angle, get_crunch_angle


def analyze_video_metrics_and_draw(input_path: str, output_path: str) -> dict:
    import cv2
    import mediapipe as mp
    import numpy as np
    from utils.metrics import calculate_angle, get_body_lean_angle, get_crunch_angle

    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5)
    mp_drawing = mp.solutions.drawing_utils

    cap = cv2.VideoCapture(input_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    elbow_angles = []
    elbow_shifts = []
    knee_angles = []
    body_lean_angles = []
    crunch_angles = []

    person_detected = False

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(image_rgb)

        if results.pose_landmarks:
            person_detected = True
            lm = results.pose_landmarks.landmark

            try:
                right_elbow = calculate_angle(
                    lm[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                    lm[mp_pose.PoseLandmark.RIGHT_ELBOW.value],
                    lm[mp_pose.PoseLandmark.RIGHT_WRIST.value],
                )
                elbow_angles.append(right_elbow)

                shoulder_x = lm[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x
                elbow_x = lm[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x
                elbow_shift = abs(elbow_x - shoulder_x)
                elbow_shifts.append(elbow_shift)

                right_knee = calculate_angle(
                    lm[mp_pose.PoseLandmark.RIGHT_HIP.value],
                    lm[mp_pose.PoseLandmark.RIGHT_KNEE.value],
                    lm[mp_pose.PoseLandmark.RIGHT_ANKLE.value],
                )
                knee_angles.append(right_knee)

                lean_angle = get_body_lean_angle(
                    lm[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                    lm[mp_pose.PoseLandmark.LEFT_HIP.value],
                )
                body_lean_angles.append(lean_angle)

                crunch_angle = get_crunch_angle(
                    lm[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                    lm[mp_pose.PoseLandmark.RIGHT_HIP.value],
                )
                crunch_angles.append(crunch_angle)
            except Exception:
                pass

            # ⬇️ Рисуем скелет на кадре
            mp_drawing.draw_landmarks(
                frame,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                connection_drawing_spec=mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2),
            )

        # ⬇️ Записываем кадр в выходное видео
        out.write(frame)

    cap.release()
    out.release()
    pose.close()

    if not person_detected:
        return {}

    def safe_mean(arr):
        return round(float(np.mean(arr)), 2) if arr else 0.0

    return {
        "avg_elbow_angle": safe_mean(elbow_angles),
        "avg_elbow_shift": safe_mean(elbow_shifts),
        "avg_knee_angle": safe_mean(knee_angles),
        "max_body_lean_angle": round(max(body_lean_angles), 2) if body_lean_angles else 0.0,
        "avg_crunch_angle": safe_mean(crunch_angles),
    }
