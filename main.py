import cv2
import dlib
from imutils import face_utils
from scipy.spatial import distance as dist
from playsound import playsound
from twilio.rest import Client
import threading
import queue
import time

TWILIO_ACCOUNT_SID = 'YOUR TWILIO_ACCOUNT_SID'
TWILIO_AUTH_TOKEN = 'YOUR TWILIO_AUTH_TOKEN '
TWILIO_PHONE_NUMBER = 'YOUR TWILIO_PHONE_NUMBER'
TO_PHONE_NUMBER = 'YOUR TO_PHONE_NUMBER'

twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def send_sms_alert(message):
    try:
        twilio_client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to=TO_PHONE_NUMBER
        )
        print("SMS Alert Sent!")
    except Exception as e:
        print(f"Error sending SMS: {e}")

def play_sound_alert(sound):
    playsound(sound)

def display_message(message, frame):
    cv2.putText(frame, message, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

def alert_thread(message_queue):
    global frame, eyes_closed, is_sleeping, not_paying_attention, last_message_time

    while True:
        message, timestamp = message_queue.get()
        if message:
            display_message(message, frame)
            last_message_time = timestamp
            time.sleep(3)  # Sleep for 3 seconds to keep the message on the screen

def eye_aspect_ratio(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

def main():
    global frame, eyes_closed, is_sleeping, not_paying_attention, last_message_time

    # Load face detector and predictor from dlib
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

    # Define constants for eye aspect ratio (EAR) and drowsiness threshold
    EAR_THRESHOLD = 0.25
    CLOSED_EYE_FRAME_THRESHOLD = 10
    closed_eye_frames = 1
    eyes_closed = False

    # Define constants for not paying attention threshold
    NOT_PAYING_ATTENTION_THRESHOLD = 10
    not_paying_attention_frames = 0
    not_paying_attention = False

    # Define constants for sleeping detection
    SLEEPING_THRESHOLD = 20
    sleeping_frames = 0
    is_sleeping = False

    # Open the default camera (usually the webcam)
    cap = cv2.VideoCapture(0)

    # Check if the camera opened successfully
    if not cap.isOpened():
        print("Error: Could not open camera")
        exit()

    # Create a thread-safe queue for messages
    message_queue = queue.Queue()

    # Start the alert thread
    alert_thread_instance = threading.Thread(target=alert_thread, args=(message_queue,))
    alert_thread_instance.daemon = True
    alert_thread_instance.start()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = detector(gray, 0)

        if len(faces) == 0:
            not_paying_attention_frames += 1
            if not_paying_attention_frames >= NOT_PAYING_ATTENTION_THRESHOLD:
                if not not_paying_attention:
                    print("Not Paying Attention!")
                    play_sound_alert('sleeping.mp3')
                    not_paying_attention = True
                    message_queue.put(("Not Paying Attention!", time.time()))
        else:
            not_paying_attention_frames = 0
            not_paying_attention = False

        for face in faces:
            shape = predictor(gray, face)
            shape = face_utils.shape_to_np(shape)

            left_eye = shape[36:42]
            right_eye = shape[42:48]

            left_ear = eye_aspect_ratio(left_eye)
            right_ear = eye_aspect_ratio(right_eye)

            ear = (left_ear + right_ear) / 2.0

            if ear < EAR_THRESHOLD:
                closed_eye_frames += 1
                if closed_eye_frames >= CLOSED_EYE_FRAME_THRESHOLD:
                    if not eyes_closed:
                        print("Eyes Closed - Drowsiness Alert!")
                        play_sound_alert('bleep-censorship-sound-wav-74691-[AudioTrimmer.com]-[AudioTrimmer.com].mp3')
                        eyes_closed = True
                        message_queue.put(("Drowsiness Alert!", time.time()))

                sleeping_frames += 1
                if sleeping_frames >= SLEEPING_THRESHOLD:
                    if not is_sleeping:
                        print("Sleeping Detected!")
                        play_sound_alert('race-start-beeps-125125.mp3')
                        is_sleeping = True
                        message_queue.put(("Sleeping Detected!", time.time()))
                        send_sms_alert("Emergency! Sleeping Detected")
            else:
                closed_eye_frames = 0
                eyes_closed = False
                sleeping_frames = 0
                is_sleeping = False

            cv2.putText(frame, f"EAR: {ear:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        if time.time() - last_message_time > 3:
            cv2.putText(frame, "", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)  # Clear the message after 3 seconds

        cv2.imshow('Alerts', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    last_message_time = time.time()  # Initialize last message time
    main()
