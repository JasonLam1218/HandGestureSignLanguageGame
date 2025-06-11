import cv2

def list_cameras():
    i = 0
    while True:
        cap = cv2.VideoCapture(i)
        if not cap.read()[0]:
            break
        else:
            print(f"Camera found at index: {i}")
        cap.release()
        i += 1

if __name__ == '__main__':
    print("Listing all available camera devices:")
    list_cameras()
    print("\nDone listing cameras.") 