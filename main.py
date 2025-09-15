import cv2
import os
import time
import serial
import pygame
from picamera2 import Picamera2
from inference_sdk import InferenceHTTPClient
from detection import check_image
from twilio.rest import Client


alert_sound = None


def create_folder(folder_name):
    """Create a folder if it doesn't exist."""
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)


def initialize_audio():
    """Initialize audio system and load alert sound."""
    global alert_sound
    try:
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)
        if os.path.exists(ALERT_SOUND_FILE):
            alert_sound = pygame.mixer.Sound(ALERT_SOUND_FILE)
            print("Audio system initialized successfully")
        else:
            print(f"Warning: Alert sound file not found at {ALERT_SOUND_FILE}")
    except Exception as e:
        print(f"Error initializing audio: {e}")
        pygame.mixer.quit()


try:
    CLIENT = InferenceHTTPClient(
        api_url="https://detect.roboflow.com", api_key=ROBOFLOW_API_KEY
    )
except Exception as e:
    print(f"Error initializing clients: {e}")
    exit(1)

try:
    gps_serial = serial.Serial("/dev/ttyS0", 9600, timeout=1)
except serial.SerialException as e:
    print(f"Error initializing GPS: {e}")
    gps_serial = None


def get_gps_location():
    """Get GPS coordinates from NEO-6M module."""
    if gps_serial is None:
        return None, None

    while True:
        line = gps_serial.readline().decode("utf-8")
        if line.startswith("$GPGGA"):
            try:
                parts = line.split(",")
                if parts[2] and parts[4]:
                    lat = float(parts[2][:2]) + float(parts[2][2:]) / 60
                    lon = float(parts[4][:3]) + float(parts[4][3:]) / 60
                    if parts[3] == "S":
                        lat = -lat
                    if parts[5] == "W":
                        lon = -lon
                    return lat, lon
            except ValueError:
                pass


def play_alert_sound():
    """Play alert sound through 3.5mm audio jack with error handling."""
    if alert_sound:
        try:
            print("Attempting to play alert sound...")
            pygame.mixer.stop()  
            alert_sound.play()
            time.sleep(2)  
            print("Alert sound played successfully")
        except Exception as e:
            print(f"Error playing alert sound: {e}")
    else:
        print("No alert sound available - check if alert.wav exists in audio folder")


def send_alert(detection_result):
    """Send SMS alert with location and play sound if elephant detected."""
    print(f"Processing detection result: {detection_result}")

    if not detection_result:
        print("No elephant detected, skipping alert")
        return

    print("Elephant detected! Triggering alerts...")

    if alert_sound:
        try:
            pygame.mixer.stop()
            alert_sound.play()
            time.sleep(2)
            print("Alert sound played successfully")
        except Exception as e:
            print(f"Error playing alert sound: {e}")

    try:
        twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        location_text = "Location: 9.7268Â° N, 76.7261Â° E\nGoogle Maps: https://maps.google.com/?q=9.7268,76.7261"
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        message = f"ðŸ˜ Elephant detected!\nTime: {current_time}\n{location_text}"

        message_info = twilio_client.messages.create(
            body=message, from_=TWILIO_PHONE_NUMBER, to=TARGET_PHONE_NUMBER
        )
        print(f"SMS sent successfully. SID: {message_info.sid}")
    except Exception as e:
        print(f"Failed to send SMS: {e}")


def show_live_feed_with_timed_motion_capture():
    images_folder = "images"
    create_folder(images_folder)

    picam2 = Picamera2()
    preview_config = picam2.create_preview_configuration(
        main={"size": (1920, 1080), "format": "RGB888"},
        controls={
            "FrameDurationLimits": (33333, 33333),
            "ExposureTime": 20000,
            "AnalogueGain": 1.0,
        },
    )
    picam2.configure(preview_config)
    picam2.start()
    time.sleep(2)

    print("Running motion detection... (Press Ctrl+C to stop)")

    prev_frame = picam2.capture_array()
    if prev_frame is None:
        print("Error: Unable to capture initial frame")
        picam2.stop()
        return

    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_RGB2GRAY)
    prev_gray = cv2.GaussianBlur(prev_gray, (21, 21), 0)

    object_start_time = None
    capture_delay = 2
    motion_threshold = 3000

    try:
        while True:
            frame = picam2.capture_array()
            if frame is None:
                print("Warning: Skipped frame")
                continue

            frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)

            delta_frame = cv2.absdiff(prev_gray, gray)
            thresh = cv2.threshold(delta_frame, 25, 255, cv2.THRESH_BINARY)[1]
            thresh = cv2.dilate(thresh, None, iterations=2)

            contours = cv2.findContours(
                thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
            )[0]

            motion_detected = False
            for contour in contours:
                if cv2.contourArea(contour) < motion_threshold:
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
                    cv2.imwrite(photo_path, frame_bgr)
                    print(f"Motion detected! Photo saved at: {photo_path}")

                    try:
                        result = check_image(photo_path)
                        print(f"API Result: {result}")
                        send_alert(result)
                    except Exception as e:
                        print(f"Error during processing: {e}")

                    object_start_time = None
            else:
                object_start_time = None

            prev_gray = gray.copy()

    except KeyboardInterrupt:
        print("\nStopping motion detection...")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        picam2.stop()
        pygame.mixer.quit()
        if gps_serial:
            gps_serial.close()


if __name__ == "__main__":
    try:
        initialize_audio()  
        show_live_feed_with_timed_motion_capture()
    except Exception as e:
        print(f"Main program error: {e}")
    finally:
        pygame.mixer.quit()
        if gps_serial:
            gps_serial.close()
