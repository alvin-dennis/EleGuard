# import cv2
# import os
# import time
# import requests
# from inference_sdk import InferenceHTTPClient
# from idk import check_image

# # Initialize the Roboflow inference client
# CLIENT = InferenceHTTPClient(
#     api_url="https://detect.roboflow.com", api_key="q1Da5hSpF9063JELvJer"
# )



# def create_folder(folder_name):
#     """Create a folder if it doesn't exist."""
#     if not os.path.exists(folder_name):
#         os.makedirs(folder_name)


# # def check_image(image_path):
# #     """Check the image using the Roboflow API."""
# #     # Send the file path to the API
# #     with open(image_path, "rb") as image_file:
# #         # Read the image as bytes and send to the API
# #         image_bytes = image_file.read()
# #         result = CLIENT.infer(image_bytes, model_id="train-elephant/2")
# #     return result


# def show_live_feed_with_timed_motion_capture():
#     # Create the 'images' folder
#     images_folder = "images"
#     create_folder(images_folder)

#     # Open a connection to the default webcam (camera index 0)
#     cap = cv2.VideoCapture(0)

#     # Check if the webcam is opened successfully
#     if not cap.isOpened():
#         print("Error: Unable to access the camera.")
#         return

#     print("Press 'q' to quit the live feed.")

#     # Read the first frame to use as a reference for motion detection
#     ret, prev_frame = cap.read()
#     if not ret:
#         print("Error: Unable to read the first frame.")
#         return

#     # Convert the first frame to grayscale and blur it
#     prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
#     prev_gray = cv2.GaussianBlur(prev_gray, (21, 21), 0)

#     object_start_time = None  # Time when motion is first detected
#     capture_delay = 2  # Seconds to wait before capturing an image

#     while True:
#         # Capture the current frame
#         ret, frame = cap.read()
#         if not ret:
#             print("Error: Unable to read frame from camera.")
#             break

#         # Convert the current frame to grayscale and blur it
#         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#         gray = cv2.GaussianBlur(gray, (21, 21), 0)

#         # Compute the absolute difference between the current frame and the previous frame
#         delta_frame = cv2.absdiff(prev_gray, gray)

#         # Apply a threshold to identify significant changes (motion)
#         _, thresh = cv2.threshold(delta_frame, 25, 255, cv2.THRESH_BINARY)
#         thresh = cv2.dilate(thresh, None, iterations=2)

#         # Find contours of the thresholded image
#         contours, _ = cv2.findContours(
#             thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
#         )

#         motion_detected = False
#         for contour in contours:
#             # Ignore small movements
#             if cv2.contourArea(contour) < 1000:
#                 continue

#             # Draw a rectangle around the detected motion
#             (x, y, w, h) = cv2.boundingRect(contour)
#             cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
#             motion_detected = True

#         if motion_detected:
#             if object_start_time is None:
#                 # Record the time when motion is first detected
#                 object_start_time = time.time()
#             elif time.time() - object_start_time >= capture_delay:
#                 # Capture the image if the object stays in the frame for the specified time
#                 photo_path = os.path.join(
#                     images_folder, f"motion_{int(time.time())}.jpg"
#                 )
#                 cv2.imwrite(photo_path, frame)
#                 print(f"Motion detected! Photo saved at: {photo_path}")

#                 # Check the image using the API
#                 try:
#                     result = check_image(photo_path)
#                     print(f"API Result: {result}")
#                 except Exception as e:
#                     print(f"Error during API call: {e}")

#                 # Reset the timer after capturing the image
#                 object_start_time = None
#         else:
#             # Reset the timer if no motion is detected
#             object_start_time = None

#         # Display the live feed
#         cv2.imshow("Live Feed", frame)

#         # Update the previous framew
#         prev_gray = gray

#         # Break the loop if 'q' is pressed
#         if cv2.waitKey(1) & 0xFF == ord("q"):
#             break

#     # Release the webcam and close the window
#     cap.release()
#     cv2.destroyAllWindows()


# if __name__ == "__main__":
#     show_live_feed_with_timed_motion_capture()

import cv2
import os
import time
from inference_sdk import InferenceHTTPClient
from detection import check_image

# Initialize the Roboflow inference client
CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com", api_key="q1Da5hSpF9063JELvJer"
)


def create_folder(folder_name):
    """Create a folder if it doesn't exist."""
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)


def show_live_feed_with_timed_motion_capture():
    # Create the 'images' folder
    images_folder = "images"
    create_folder(images_folder)

    # Open a connection to the default webcam (camera index 0)
    cap = cv2.VideoCapture(0)

    # Check if the webcam is opened successfully
    if not cap.isOpened():
        print("Error: Unable to access the camera.")
        return

    print("Running motion detection... (Press Ctrl+C to stop)")

    # Read the first frame to use as a reference for motion detection
    ret, prev_frame = cap.read()
    if not ret:
        print("Error: Unable to read the first frame.")
        return

    # Convert the first frame to grayscale and blur it
    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    prev_gray = cv2.GaussianBlur(prev_gray, (21, 21), 0)

    object_start_time = None  # Time when motion is first detected
    capture_delay = 2  # Seconds to wait before capturing an image

    try:
        while True:
            # Capture the current frame
            ret, frame = cap.read()
            if not ret:
                print("Error: Unable to read frame from camera.")
                break

            # Convert the current frame to grayscale and blur it
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)

            # Compute the absolute difference between frames
            delta_frame = cv2.absdiff(prev_gray, gray)
            _, thresh = cv2.threshold(delta_frame, 25, 255, cv2.THRESH_BINARY)
            thresh = cv2.dilate(thresh, None, iterations=2)

            # Find contours
            contours, _ = cv2.findContours(
                thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
            )

            motion_detected = False
            for contour in contours:
                if cv2.contourArea(contour) < 1000:
                    continue

                (x, y, w, h) = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                motion_detected = True

            if motion_detected:
                if object_start_time is None:
                    object_start_time = time.time()
                elif time.time() - object_start_time >= capture_delay:
                    photo_path = os.path.join(
                        images_folder, f"motion_{int(time.time())}.jpg"
                    )
                    cv2.imwrite(photo_path, frame)
                    print(f"Motion detected! Photo saved at: {photo_path}")

                    try:
                        result = check_image(photo_path)
                        print(f"API Result: {result}")
                    except Exception as e:
                        print(f"Error during API call: {e}")

                    object_start_time = None
            else:
                object_start_time = None

            # Update the previous frame
            prev_gray = gray

    except KeyboardInterrupt:
        print("\nStopping motion detection...")
    finally:
        # Release the webcam
        cap.release()


if __name__ == "__main__":
    show_live_feed_with_timed_motion_capture()