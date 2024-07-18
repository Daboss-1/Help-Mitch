import cv2
import numpy as np

eye_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_eye.xml')
face_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')

one_eye = cv2.imread('testing/one-eye-open.jpg', 0)
two_eyes = cv2.imread('testing/2-eyes.jpeg', 0)
no_eyes = cv2.imread('testing/closed-eyes.jpeg', 0)

def detect_eyes(img):
    face_img = img.copy()
    eyes = eye_cascade.detectMultiScale(face_img, scaleFactor=1.2, minNeighbors=7)
    return eyes

def detect_face(img):
    face_img = img.copy()
    faces = face_cascade.detectMultiScale(face_img, scaleFactor=1.2, minNeighbors=5)
    return faces

def draw_rect(img, cascade, color):
    result = img.copy()
    for (x, y, w, h) in cascade:
        cv2.rectangle(result, (x, y), (x + w, y + h), color, 5)
    return result

def get_face_foreground(cascade):
    if len(cascade) == 1 or len(cascade) == 0:
        return cascade
    else:
        max_area = 0
        final_face = None
        for (x, y, w, h) in cascade:
            area = w * h
            if area > max_area:
                max_area = area
                final_face = (x, y, w, h)
        return [final_face]

def get_background_faces(faces):
    foreground_face = get_face_foreground(faces)
    background_faces = [face for face in faces if not any(np.array_equal(face, ff) for ff in foreground_face)]
    return background_faces

one_eye_result = len(detect_eyes(one_eye))
two_eye_result = len(detect_eyes(two_eyes))
no_eye_result = len(detect_eyes(no_eyes))

cv2.imwrite('testing/no-eye-results.jpeg', draw_rect(no_eyes, detect_eyes(no_eyes), (0,255,0)))
cv2.imwrite('testing/one-eye-results.jpeg', draw_rect(one_eye, detect_eyes(one_eye), (0,255,0)))
cv2.imwrite('testing/two-eye-results.jpeg', draw_rect(two_eyes, detect_eyes(two_eyes), (0,255,0)))

print(f"{no_eye_result} eye(s) were/was detected for a picture with zero eyes (closed eyes).")
print(f"{one_eye_result} eye(s) were/was detected for a picture with one eye.")
print(f"{two_eye_result} eye(s) were/was detected for a picture with two eyes.")
print("Initializing camera...")
cap = cv2.VideoCapture(0)
print("Camera initialized!")
while True:
    ret, frame = cap.read()
    background_faces = get_background_faces(detect_face(frame))
    face_from_frame = get_face_foreground(detect_face(frame))
    eyes_from_frame = detect_eyes(frame)
    frame = draw_rect(draw_rect(draw_rect(frame, background_faces, (255, 0, 0)), face_from_frame, (255, 255, 255)), eyes_from_frame, (0, 255, 0))

    cv2.imshow('Eye Detection', frame)
    code = cv2.waitKey(10)
    if code == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
