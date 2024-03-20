import os
import cv2

# specify directory where images are stored
image_dir = 'Example Screenshots'
output_dir = 'Example Cropped Output'

# Create the output directory if it does not exist
os.makedirs(output_dir, exist_ok=True)

# Get a list of all image files in the directory
image_files = [f for f in os.listdir(image_dir) if f.endswith('.jpg')]

# Initialize list to hold images that are not cropped
not_cropped = []

# Define a function to check if a rectangle is contained within any rectangle from a list
def is_contained(rect, rect_list):
    for R in rect_list:
        if R[0] < rect[0] < rect[0] + rect[2] < R[0] + R[2] and R[1] < rect[1] < rect[1] + rect[3] < R[1] + R[3]:
            return True
    return False

# Function to save the cropped images
def save_cropped_image(image, rect, output_dir, image_file, index):
    x, y, w, h = rect
    cropped_img = image[y:y+h, x:x+w]
    cv2.imwrite(os.path.join(output_dir, '{}_{}.jpg'.format(os.path.splitext(image_file)[0], index)), cropped_img)

# Loop through each image file
for idx, image_file in enumerate(image_files):
    # construct full image path
    image_path = os.path.join(image_dir, image_file)

    # Load image
    im = cv2.imread(image_path)

    # Convert to grayscale and threshold
    imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgray, 1, 255, 0)

    # Find contours in the threshold image
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Initialize counter for cropped images
    i = 0

    # Initialize list for rectangles
    rect_list = []

    # Initialize flag for whether a rectangle was found
    rect_found = False

    # Loop through the found contours
    for cnt in contours:
        # Get the bounding rectangle for each contour
        x, y, w, h = cv2.boundingRect(cnt)

        # Only consider contours where the bounding rectangle is greater than 50x50 and not on the edge
        if x > 0 and y > 0 and w > 50 and h > 50:
            rect = (x, y, w, h)

            # Check if the current rectangle is contained within any of the previous rectangles
            if not is_contained(rect, rect_list):

                # Draw a green rectangle around the contour on the original image
                cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # Save the cropped image to the output directory with a sequential name
                save_cropped_image(im, rect, output_dir, image_file, i)

                # Increment the counter
                i += 1

                # Add the rectangle to the list
                rect_list.append(rect)

                # Set flag to indicate that a rectangle was found
                rect_found = True

    # If no suitable rectangle was found for this image, add it to the list of images that were not cropped
    if not rect_found:
        not_cropped.append(image_file)

# Write the list of images that were not cropped to a text file
with open('not_cropped.txt', 'w') as f:
    for image_file in not_cropped:
        f.write("%s\n" % image_file)
