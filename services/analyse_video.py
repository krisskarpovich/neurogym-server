import mediapipe as mp
import cv2
import math

# def calculate_angle(a, b, c):
#     """Вычисляет угол между тремя точками"""
#     a = [a.x, a.y]
#     b = [b.x, b.y]
#     c = [c.x, c.y]

#     angle = math.degrees(
#         math.atan2(c[1] - b[1], c[0] - b[0]) -
#         math.atan2(a[1] - b[1], a[0] - b[0])
#     )
#     return abs(angle)

# def analyze_video(file_path: str, workout_id: int) -> list[str]:
#     mp_pose = mp.solutions.pose
#     cap = cv2.VideoCapture(file_path)

#     angles = []

#     with mp_pose.Pose(static_image_mode=False) as pose:
#         while cap.isOpened():

# def calculate_angle(a, b, c):
#         a = [a.x, a.y]
#         b = [b.x, b.y]
#         c = [c.x, c.y]
#         angle = math.degrees(
#             math.atan2(c[1] - b[1], c[0] - b[0]) -
#             math.atan2(a[1] - b[1], a[0] - b[0])
#         )
#         return abs(angle)


from mediapipe.python.solutions.pose import PoseLandmark as mp_pose
import cv2
import mediapipe as mp
import numpy as np
from utils.metrics import calculate_angle, get_body_lean_angle

def analyze_video_metrics(file_path: str) -> dict:
    cap = cv2.VideoCapture(file_path)
    mp_pose_lib = mp.solutions.pose
    pose = mp_pose_lib.Pose(static_image_mode=False, min_detection_confidence=0.5)
    
    elbow_angles = []
    elbow_shifts = []
    knee_angles = []
    body_lean_angles = []

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(image)

        if results.pose_landmarks:
            lm = results.pose_landmarks.landmark

            try:
                # -------- Elbow angle (бицепс) --------
                right_elbow = calculate_angle(
                    lm[mp_pose.RIGHT_SHOULDER.value],
                    lm[mp_pose.RIGHT_ELBOW.value],
                    lm[mp_pose.RIGHT_WRIST.value]
                )
                elbow_angles.append(right_elbow)

                # -------- Elbow shift (локти вперёд) --------
                shoulder_x = lm[mp_pose.RIGHT_SHOULDER.value].x
                elbow_x = lm[mp_pose.RIGHT_ELBOW.value].x
                elbow_shift = abs(elbow_x - shoulder_x)
                elbow_shifts.append(elbow_shift)

                # -------- Knee angle (присед) --------
                right_knee = calculate_angle(
                    lm[mp_pose.RIGHT_HIP.value],
                    lm[mp_pose.RIGHT_KNEE.value],
                    lm[mp_pose.RIGHT_ANKLE.value]
                )
                knee_angles.append(right_knee)

                # -------- Body lean (наклон) --------
                lean_angle = get_body_lean_angle(
                    lm[mp_pose.LEFT_SHOULDER.value],
                    lm[mp_pose.LEFT_HIP.value]
                )
                body_lean_angles.append(lean_angle)
                
                crunch_angles = []

                # Внутри цикла, при наличии landmarks:
                lean_angle = get_body_lean_angle(
                    lm[mp_pose.LEFT_SHOULDER.value],
                    lm[mp_pose.LEFT_HIP.value]
                )
                body_lean_angles.append(lean_angle)

                crunch_angle = get_crunch_angle(
                    lm[mp_pose.RIGHT_SHOULDER.value],
                    lm[mp_pose.RIGHT_HIP.value]
                )
                crunch_angles.append(crunch_angle)


            except:
                continue

    cap.release()
    pose.close()

    # Усреднение по всем кадрам
    def safe_mean(arr):
        return round(float(np.mean(arr)), 2) if arr else 0.0

    metrics = {
      "avg_elbow_angle": safe_mean(elbow_angles),
      "avg_elbow_shift": safe_mean(elbow_shifts),
      "avg_knee_angle": safe_mean(knee_angles),
      "max_body_lean_angle": round(max(body_lean_angles), 2) if body_lean_angles else 0.0,
      "avg_crunch_angle": safe_mean(crunch_angles),
    }


    return metrics



# import numpy as np

# def calculate_angle(a, b, c):
#     """Расчет угла между тремя точками (в градусах)."""
#     a = np.array(a)
#     b = np.array(b)
#     c = np.array(c)
    
#     ab = a - b
#     cb = c - b
    
#     cosine_angle = np.dot(ab, cb) / (np.linalg.norm(ab) * np.linalg.norm(cb))
#     angle = np.arccos(np.clip(cosine_angle, -1.0, 1.0))
    
#     return np.degrees(angle)

# def get_elbow_angle(landmarks, side='left'):
#     """Угол в локте: side = 'left' или 'right'"""
#     if side == 'left':
#         shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
#         elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value]
#         wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value]
#     else:
#         shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
#         elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value]
#         wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value]
    
#     return calculate_angle(
#         [shoulder.x, shoulder.y],
#         [elbow.x, elbow.y],
#         [wrist.x, wrist.y]
#     )


def get_crunch_angle(shoulder: object, hip: object) -> float:
    """Угол между линией плеч-стопа и вертикалью"""
    # Пример для правой стороны
    vertical = [0, 1]
    body_vector = [shoulder.x - hip.x, shoulder.y - hip.y]
    
    angle = math.degrees(
        math.atan2(vertical[1], vertical[0]) -
        math.atan2(body_vector[1], body_vector[0])
    )
    return abs(angle)
