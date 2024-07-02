import cv2

# Example code to read frames
cap = cv2.VideoCapture(1)  # Adjust the index (0 for default camera) or path to video file

if not cap.isOpened():
    print("Error: Could not open video source.")
    exit()

while True:
    ret, frame = cap.read()
    
    if not ret:
        print("Error: Could not read frame.")
        break
    
    # Process frame here (e.g., display, save, etc.)
    cv2.imshow('Frame', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
