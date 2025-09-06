import cv2
import numpy as np

# Web Camera
cap = cv2.VideoCapture('video.mp4')
count_line_position = 550
# Minimum width and height for vehicle detection
min_width_react = 80
min_height_react = 80

# Size thresholds for vehicle classification (in pixels)
SMALL_MAX_WIDTH = 120
SMALL_MAX_HEIGHT = 120
MEDIUM_MAX_WIDTH = 200
MEDIUM_MAX_HEIGHT = 200
# Intialize Substructor
algo = cv2.bgsegm.createBackgroundSubtractorMOG()

def center_handle(x,y,w,h):
    x1=int(w/2)
    y1=int(h/2)
    cx=x+x1
    cy=y+y1
    return cx,cy

detect=[]
offset =6 # Allowable error between pixel

# Counters for each vehicle type
small_vehicle_count = 0
medium_vehicle_count = 0
large_vehicle_count = 0
counter = 0  # total

while True:
    ret,frame1=cap.read()
    grey = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
    blur= cv2.GaussianBlur(grey,(3,3),5)
    # applying on each frame
    img_sub = algo.apply(blur)
    dilat = cv2.dilate(img_sub,np.ones((5,5)))
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
    dilatdata = cv2.morphologyEx(dilat,cv2.MORPH_ELLIPSE,kernel)
    dilatdata = cv2.morphologyEx(dilatdata,cv2.MORPH_ELLIPSE,kernel)
    counterShape,h = cv2.findContours(dilatdata,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    cv2.line(frame1, (25,count_line_position),(1200,count_line_position),(255,127,0),3)

    for (i,c) in enumerate(counterShape):
        (x,y,w,h) = cv2.boundingRect(c)
        validate_counter = (w>=min_width_react) and (h>=min_height_react)
        if not validate_counter:
            continue
        cv2.rectangle(frame1,(x,y),(x+w,y+h),(0,255,0),2)

        # Classify vehicle size
        if w <= SMALL_MAX_WIDTH and h <= SMALL_MAX_HEIGHT:
            vehicle_type = 'Small'
            color = (255, 255, 0)
        elif w <= MEDIUM_MAX_WIDTH and h <= MEDIUM_MAX_HEIGHT:
            vehicle_type = 'Medium'
            color = (0, 255, 255)
        else:
            vehicle_type = 'Large'
            color = (255, 0, 255)

        cv2.putText(frame1, f"{vehicle_type} Vehicle", (x, y-20), cv2.FONT_HERSHEY_TRIPLEX, 1, color, 2)

        center = center_handle(x,y,w,h)
        detect.append((center, vehicle_type))
        cv2.circle(frame1,center,4,(0,0,255),-1)

    # Count vehicles by type when they cross the line
    for (center, vtype) in detect[:]:
        cx, cy = center
        if cy < (count_line_position+offset) and cy > (count_line_position-offset):
            counter += 1
            if vtype == 'Small':
                small_vehicle_count += 1
            elif vtype == 'Medium':
                medium_vehicle_count += 1
            else:
                large_vehicle_count += 1
            cv2.line(frame1,(25,count_line_position),(1200,count_line_position),(0,127,255),3)
            detect.remove((center, vtype))
            print(f"vehicle counter: {counter} | Small: {small_vehicle_count} | Medium: {medium_vehicle_count} | Large: {large_vehicle_count}")

    # Display counters for each vehicle type
    cv2.putText(frame1, f"Total: {counter}", (450, 70), cv2.FONT_HERSHEY_COMPLEX, 2, (0,0,255), 5)
    cv2.putText(frame1, f"Small: {small_vehicle_count}", (50, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,0), 2)
    cv2.putText(frame1, f"Medium: {medium_vehicle_count}", (50, 120), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,255), 2)
    cv2.putText(frame1, f"Large: {large_vehicle_count}", (50, 170), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,255), 2)


    cv2.imshow('Video',frame1)
    if cv2.waitKey(1) == 13:
        break
cv2.destroyAllWindows()
cap.release()