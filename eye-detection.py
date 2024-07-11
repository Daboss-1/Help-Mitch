import cv2

eye_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_eye.xml')
face_cascade = cv2.CascadeClassifier('haarcascades\haarcascade_frontalface_default.xml')

one_eye = cv2.imread('testing/one-eye-open.jpg',0)
two_eyes = cv2.imread('testing/2-eyes.jpeg',0)
no_eyes = cv2.imread('testing/closed-eyes.jpeg',0)

def detect_eyes(img):
    face_img = img.copy()
    eyes = eye_cascade.detectMultiScale(face_img,scaleFactor=1.35,minNeighbors=5) 
    
    return len(eyes)

def detect_eyes_image(img):
    face_img = img.copy()
    eyes = eye_cascade.detectMultiScale(face_img,scaleFactor=1.35,minNeighbors=5) 
    
    for (x,y,w,h) in eyes: 
        cv2.rectangle(face_img, (x,y), (x+w,y+h), (255,255,255), 10) 
    return face_img

def detect_face(img):
    face_img = img.copy()
    faces = face_cascade.detectMultiScale(face_img,scaleFactor=1.5,minNeighbors=5) 
    
    for (x,y,w,h) in faces: 
        cv2.rectangle(face_img, (x,y), (x+w,y+h), (255,255,255), 5) 
    return face_img

one_eye_result = detect_eyes(one_eye)
two_eye_result = detect_eyes(two_eyes)
no_eye_result = detect_eyes(no_eyes)

cv2.imwrite('testing/no-eye-results.jpeg', detect_eyes_image(no_eyes))
cv2.imwrite('testing/one-eye-results.jpeg', detect_eyes_image(one_eye))
cv2.imwrite('testing/two-eye-results.jpeg', detect_eyes_image(two_eyes))

print(f"{no_eye_result} eye(s) were/was detected for a picture with zero eyes (closed eyes).")
print(f"{one_eye_result} eye(s) were/was detected for a picture with one eye.")
print(f"{two_eye_result} eye(s) were/was detected for a picture with two eyes.")
print("Initializing camera...")
cap = cv2.VideoCapture(0)
print("Camera initialized!")
while True:
    ret,frame = cap.read()
    frame = (detect_eyes_image(frame))
    cv2.imshow('Eye Detection',frame)
    code = cv2.waitKey(10)
    if code == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()