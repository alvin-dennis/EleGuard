from roboflow import Roboflow
import cv2


def check_image(IMAGE_PATH):
    api_key = "your_api_key_here"  # Replace with your actual API key

    if not api_key:
        raise EnvironmentError("ROBOFLOW_API_KEY environment variable is not set")

    rf = Roboflow(api_key=api_key)
    project = rf.workspace().project("train-elephant")
    model = project.version(2).model

    try:
        image = cv2.imread(IMAGE_PATH)
        if image is None:
            raise FileNotFoundError(f"Could not read image at {IMAGE_PATH}")

        image = cv2.resize(image, (640, 480), interpolation=cv2.INTER_AREA)

        result = model.predict(IMAGE_PATH, confidence=0.65, overlap=30).json()

        # Simplify return value - just return True if any predictions exist
        if "predictions" in result and len(result["predictions"]) > 0:
            confidence = result["predictions"][0]["confidence"]
            print(f"Elephant detected with confidence: {confidence}")
            return True

        print("No elephants detected in the image.")
        return False

    except Exception as e:
        print(f"An error occurred during detection: {str(e)}")
        return False
