import cv2
import csv

# Path to the sheet music image
sheet_music_path = 'F:/Projects/TuneTracker/twinkle1.png'

# Load the sheet music image
sheet_music_img = cv2.imread(sheet_music_path)
sheet_music_img_copy = sheet_music_img.copy()

# List to store note coordinates
note_coordinates = []

# Mouse callback function to capture coordinates
def mouse_callback(event, x, y, flags, param):
    global note_coordinates, sheet_music_img_copy
    
    if event == cv2.EVENT_LBUTTONDOWN:
        # Define the size of the bounding box (adjust as needed)
        width, height = 20, 20

        # Draw a rectangle around the clicked point
        cv2.rectangle(sheet_music_img_copy, (x, y), (x + width, y + height), (0, 255, 0), 2)
        cv2.imshow("Sheet Music", sheet_music_img_copy)
        
        # Append the coordinates to the list
        note_coordinates.append((x, y, width, height))

# Create a window and set the mouse callback function
cv2.namedWindow("Sheet Music")
cv2.setMouseCallback("Sheet Music", mouse_callback)

# Display the sheet music image
while True:
    cv2.imshow("Sheet Music", sheet_music_img_copy)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):  # Press 'q' to quit
        break

# Save the coordinates to a CSV file
csv_file = 'note_coordinates.csv'
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["x", "y", "width", "height"])
    for coord in note_coordinates:
        writer.writerow(coord)

print(f"Note coordinates saved to {csv_file}")

# Close all OpenCV windows
cv2.destroyAllWindows()
