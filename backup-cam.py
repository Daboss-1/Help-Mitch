import math
import cv2
import numpy as np

cam_res_horiz = 1280
cam_res_vert = 720
distance_from_ground = 5 # distance from ground in feet
width_of_lane = 4 # width of the lane on the ground
side_sight_angle = 90 # angle that the camera can see side to side
verticle_sight_angle = (180 - 2 * math.degrees(math.atan((20.5 / 12) / (9/12.0)))) # angle the camera can see vertically
starting_angle = 90 # angle the camera starts at, DOES NOT WORK YET
parse_res_horiz = 640
parse_res_vert = 480

px_to_degree_ratio_horiz = parse_res_horiz / side_sight_angle
px_to_degree_ratio_vert = parse_res_vert / verticle_sight_angle
print(f"{px_to_degree_ratio_horiz} pixels per degree sideways; {px_to_degree_ratio_vert} pixels per degree vertically")

def get_cam_visual_length(distance_from_cam):
    cam_to_spot = distance_from_cam**2 + distance_from_ground**2
    return 2 * math.tan(math.radians(side_sight_angle / 2)) * cam_to_spot

def distance_from_angle(ang):
    return math.tan(math.radians(ang)) * distance_from_ground

def angle_from_distance(dis):
    return float(math.degrees(math.atan((dis / distance_from_ground))))

def draw_lines(img): # TODO
    height, width = img.shape[:2]
    angle = angle_from_distance(0 - distance_from_base) - (starting_angle - 90) # TODO
    dis_to_side = math.sqrt(math.sqrt(width_of_lane**2 + (0 + distance_from_base)**2) + distance_from_ground**2)
    angle_to_lane = math.degrees(math.acos((-width_of_lane**2 + dis_to_side**2 + dis_to_side**2)/(2 * dis_to_side * dis_to_side)))
    new_img = img.copy()
    orig_point_left = (int(width / 2 - angle_to_lane / 2.0 * px_to_degree_ratio_horiz), int(height - int((angle - (90 - verticle_sight_angle / 2.0)) * px_to_degree_ratio_vert)))
    orig_point_right = (width - int(width / 2 - angle_to_lane / 2.0 * px_to_degree_ratio_horiz), int(height - int((angle - (90 - verticle_sight_angle / 2.0)) * px_to_degree_ratio_vert)))
    for i in range(20):
        angle = angle_from_distance(i - distance_from_base)
        dis_to_side = math.sqrt(math.sqrt(width_of_lane**2 + (i + distance_from_base)**2) + distance_from_ground**2)
        angle_to_lane = math.degrees(math.acos((-width_of_lane**2 + dis_to_side**2 + dis_to_side**2)/(2 * dis_to_side * dis_to_side)))
        new_img = cv2.line(new_img,(0, height - int((angle - (90 - verticle_sight_angle / 2.0)) * px_to_degree_ratio_vert)) ,(width, height - int((angle - (90 - verticle_sight_angle / 2.0)) * px_to_degree_ratio_vert)), (0, 255, 0), 1, 1, 0)
        new_img = cv2.line(new_img, (int(width / 2 - angle_to_lane / 2.0 * px_to_degree_ratio_horiz), int(height - int((angle - (90 - verticle_sight_angle / 2.0)) * px_to_degree_ratio_vert))), orig_point_left, (255, 0, 0), 2, 1, 0)
        new_img = cv2.line(new_img, (width - int((width - angle_to_lane * px_to_degree_ratio_horiz)/2.0), int(height - int((angle - (90 - verticle_sight_angle / 2.0)) * px_to_degree_ratio_vert))), orig_point_right, (255, 0, 0), 2, 1, 0)
        orig_point_left = (int(width / 2 - angle_to_lane / 2.0 * px_to_degree_ratio_horiz), int(height - int((angle - (90 - verticle_sight_angle / 2.0)) * px_to_degree_ratio_vert)))
        orig_point_right = (width - int(width / 2 - angle_to_lane / 2.0 * px_to_degree_ratio_horiz), int(height - int((angle - (90 - verticle_sight_angle / 2.0)) * px_to_degree_ratio_vert)))

        # new_img = cv2.putText(new_img, 
        #                       f"{(i - distance_from_base)}", 
        #                       (int(width / 2.0), height - int((angle - (90 - verticle_sight_angle / 2.0)) * px_to_degree_ratio_vert)), 
        #                       1, 
        #                       1, 
        #                       (255,0,0), 
        #                       1, 
        #                       1, 
        #                       False)
    
    return new_img

distance_from_base = distance_from_angle(starting_angle - verticle_sight_angle / 2) # distance to where the camera starts recording from the base
print(f"Distance from base: {distance_from_base}")

print("Initializing camera...")
cap = cv2.VideoCapture(0)
print("Camera initialized!")

while True:
    ret, frame = cap.read()
    height, width = frame.shape[:2]
    # print(f"{height} px in height, {width} px in width")
    frame = draw_lines(frame)
    cv2.imshow('Backup Cam', frame)
    code = cv2.waitKey(10)
    if code == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
