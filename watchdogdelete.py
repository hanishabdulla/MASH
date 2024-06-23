import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from google.cloud import vision

# Set the environment variable for Google Cloud credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'Google Cloud API Keys.json'

# Keywords list (shortened for brevity)
keywords = ["-KBL-", "-KDH-", "-OAI-", "-HME-"]

def detect_text(image_path):
    """Detects text in the file and returns it."""
    client = vision.ImageAnnotatorClient()

    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations

    if response.error.message:
        raise Exception(f'{response.error.message}')
    
    return texts[0].description if texts else ""

def check_keywords(text, keywords):
    """Checks if any of the keywords are present in the text."""
    for keyword in keywords:
        if keyword in text:
            print(f"Keyword found: {keyword}")
            return True
    else:
        print("No keywords found.")
        return False

class ImageHandler(FileSystemEventHandler):
    """Event handler for processing new images."""
    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.lower().endswith(('.jpeg', '.jpg', '.png')):
            print(f"New image detected: {event.src_path}")
            try:
                extracted_text = detect_text(event.src_path)
                print(f"Extracted Text for {event.src_path}:")
                print(extracted_text)
                keyword_found = check_keywords(extracted_text, keywords)
                
                # Delete the image file after processing
                os.remove(event.src_path)
                print(f"Deleted image: {event.src_path}")

            except Exception as e:
                print(f"Error processing image {event.src_path}: {e}")

if __name__ == "__main__":
    path = "/path/to/your/folder"  # Update with the path to your folder
    event_handler = ImageHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    print(f"Monitoring folder: {path}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
