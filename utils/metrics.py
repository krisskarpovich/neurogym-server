import numpy as np

def calculate_angle(a, b, c):
    a = np.array([a.x, a.y])
    b = np.array([b.x, b.y])
    c = np.array([c.x, c.y])

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    if angle > 180.0:
        angle = 360.0 - angle
    return angle

def get_body_lean_angle(shoulder, hip):
    dx = shoulder.x - hip.x
    dy = shoulder.y - hip.y
    radians = np.arctan2(dy, dx)
    angle = np.abs(radians * 180.0 / np.pi)
    return angle
