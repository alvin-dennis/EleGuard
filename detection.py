from roboflow import Roboflow
# import supervision as sv
import cv2
# import numpy as np


def check_image(IMAGE_PATH):
    # Initialize Roboflow
    rf = Roboflow(api_key="q1Da5hSpF9063JELvJer")
    project = rf.workspace().project("train-elephant")
    model = project.version(2).model

    # Define image path
    # IMAGE_PATH = "./images/download.jpg"  # Use the same image path consistently

    try:
        # Read image first to ensure it exists
        image = cv2.imread(IMAGE_PATH)
        if image is None:
            raise FileNotFoundError(f"Could not read image at {IMAGE_PATH}")

        # Make prediction with confidence between 0-1
        result = model.predict(IMAGE_PATH, confidence=0.8, overlap=30).json()
        # print(result)

        # Extract bounding boxes, labels, and confidences
        boxes = []
        labels = []
        confidences = []
        class_ids = []

        for prediction in result["predictions"]:
            x = prediction["x"]
            y = prediction["y"]
            w = prediction["width"]
            h = prediction["height"]

            # Convert center coordinates to corner coordinates
            x1 = x - w / 2
            y1 = y - h / 2
            x2 = x + w / 2
            y2 = y + h / 2

            boxes.append([x1, y1, x2, y2])
            labels.append(prediction.get("class", "Unknown"))
            confidences.append(prediction.get("confidence", 1.0))
            class_ids.append(prediction.get("class_id", 0))

        if boxes:  # Check if any detections were made
            #     # Convert to numpy arrays
            #     boxes = np.array(boxes)
            #     confidences = np.array(confidences)
            #     class_ids = np.array(class_ids)

            #     # Create detections object
            #     detections = sv.Detections(
            #         xyxy=boxes, confidence=confidences, class_id=class_ids
            #     )

            #     # Create annotators
            #     label_annotator = sv.LabelAnnotator(color_lookup=sv.ColorLookup.INDEX)
            #     box_annotator = sv.BoxAnnotator(color_lookup=sv.ColorLookup.INDEX)

            #     # Annotate image
            #     annotated_image = box_annotator.annotate(scene=image, detections=detections)
            #     annotated_image = label_annotator.annotate(
            #         scene=annotated_image, detections=detections, labels=labels
            #     )

            #     # Display result
            #     sv.plot_image(image=annotated_image, size=(16, 16))
            print(f"""
                  Confidence: {result["predictions"][0]["confidence"]}
                  Elephants detected in the image.
                  """)
            return True
        else:
            print("No elephants detected in the image.")
            return False

    except Exception as e:
        print(f"An error occurred: {str(e)}")
