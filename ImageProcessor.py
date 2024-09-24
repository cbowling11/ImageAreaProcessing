
import cv2
import numpy as np

# Initialize a list to store points
points = []
reference_points = []

# Callback function to capture the mouse click points
def get_mouse_points(event, x, y, flags, param):
    global points, reference_points
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(points) < 4:  # Collect the first 4 points for the driveway corners
            points.append((x, y))
            print(f"Point selected for corners: ({x}, {y})")
            cv2.circle(image, (x, y), 5, (0, 255, 0), -1)  # Draw a small circle on selected points
            cv2.imshow("Select 4 Corners", image)
        
        elif len(reference_points) < 2:  # Collect the next 2 points for the reference object
            reference_points.append((x, y))
            print(f"Reference point selected: ({x}, {y})")
            cv2.circle(image, (x, y), 5, (255, 0, 0), -1)  # Draw a blue circle on reference points
            cv2.imshow("Select 4 Corners", image)
        
        # Automatically close the window after selecting 4 corners and 2 reference points
        if len(points) == 4 and len(reference_points) == 2:
            print("4 points and 2 reference points selected. Proceeding...")
            cv2.destroyAllWindows()

# Function to calculate the area in pixels after perspective correction
def calculate_area(corners, reference_points, known_length_feet):
    # Define destination points to form a rectangle (adjust as needed)
    width = 500  # Set desired output width (adjust as needed)
    height = 700  # Set desired output height (adjust as needed)
    
    # Destination points, in the order: top-left, top-right, bottom-left, bottom-right
    pts_dst = np.float32([[0, 0], [width, 0], [0, height], [width, height]])

    # Compute the perspective transform matrix
    matrix = cv2.getPerspectiveTransform(corners, pts_dst)

    # Apply the perspective warp transformation
    warped_image = cv2.warpPerspective(original_image, matrix, (width, height))

    # Convert the image to grayscale and use threshold to create a binary image
    gray_warped = cv2.cvtColor(warped_image, cv2.COLOR_BGR2GRAY)
    _, thresh_warped = cv2.threshold(gray_warped, 50, 355, cv2.THRESH_BINARY)

    # Find contours on the warped image
    contours, _ = cv2.findContours(thresh_warped, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Find the largest contour (should correspond to the desired area to be calculated.)
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        area_pixels = cv2.contourArea(largest_contour)
        print(f"Calculated Area in Pixels: {area_pixels}")
        
        # Calculate the distance between the reference points in pixels
        ref_point_1 = np.array(reference_points[0])
        ref_point_2 = np.array(reference_points[1])
        distance_pixels = np.linalg.norm(ref_point_1 - ref_point_2)
        print(f"Distance between reference points in pixels: {distance_pixels}")


        # Calculate scale factor (feet per pixel)
        scale_factor = known_length_feet / distance_pixels
        print(f"Scale factor (feet per pixel): {scale_factor}")
        distance_feet = distance_pixels * (scale_factor)
        print(f"Distance between reference points in feet: {distance_feet}")

        # Convert the area from pixels to square feet
        area_square_feet = area_pixels * (scale_factor ** 2)
        print(f"Calculated Area in Square Feet: {area_square_feet}")
        
        # Draw the contour on the warped image to visualize the selected area
        cv2.drawContours(warped_image, [largest_contour], -1, (0, 255, 0), 3)
        cv2.imshow("Warped Image with area to be calculated selected.", warped_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

# ********************************************************
# CHANGE IMAGE HERE 

original_image = cv2.imread('testImage6.png')
image = original_image.copy()

# Show the image and capture points
cv2.imshow("Select 4 Corners", image)
cv2.setMouseCallback("Select 4 Corners", get_mouse_points)

# Wait until 4 corner points and 2 reference points are selected
cv2.waitKey(0)

# Proceed if 4 corners and 2 reference points are selected
if len(points) == 4 and len(reference_points) == 2:
    # Convert the points list to a NumPy array
    pts_src = np.float32(points)
    
    # Define the known length of the reference object in feet 
    known_length_feet = 4.0

    # Calculate the area within the selected points, converted to square feet
    calculate_area(pts_src, reference_points, known_length_feet)
else:
    print("Please select exactly 4 corners and 2 reference points.")
