import numpy as np
import pyaudio
from scipy.fftpack import fft
import cv2
import matplotlib.pyplot as plt

# Predefined list of expected notes (frequency in Hz) and corresponding lyrics and coordinates
score = [
    # ("Note", Frequency, "Lyric", (x, y, width, height))
    ("E5", 659.26, "Twinkle", (50, 50, 20, 20)), ("E5", 659.26, "Twinkle", (70, 50, 20, 20)), 
    ("B5", 987.77, "little", (90, 50, 20, 20)), ("B5", 987.77, "star", (110, 50, 20, 20)),
    ("C#6", 1108.73, "How", (130, 50, 20, 20)), ("C#6", 1108.73, "I", (150, 50, 20, 20)), 
    ("B5", 987.77, "wonder", (170, 50, 20, 20)),
    # Continue with the rest of the notes and coordinates
]

# Parameters for audio stream
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

# Initialize PyAudio
p = pyaudio.PyAudio()

# Open audio stream
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

# Load the sheet music image
sheet_music_img = cv2.imread('twinkle1.png')

# Pitch detection function
def detect_pitch(data):
    # Convert audio data to numpy array
    audio_data = np.frombuffer(data, dtype=np.int16)
    # Compute FFT
    fft_data = fft(audio_data)
    # Get the frequency with the highest magnitude
    frequencies = np.fft.fftfreq(len(fft_data))
    magnitudes = np.abs(fft_data)
    peak_index = np.argmax(magnitudes)
    peak_freq = abs(frequencies[peak_index] * RATE)
    return peak_freq

# Score following function
def follow_score():
    current_note_index = 0

    while current_note_index < len(score):
        # Read audio data from stream
        data = stream.read(CHUNK)
        # Detect pitch
        pitch = detect_pitch(data)
        print(f"Detected pitch: {pitch:.2f} Hz")

        # Find the closest note
        closest_note = min(score, key=lambda note: abs(note[1] - pitch))
        print(f"Closest note: {closest_note[0]}, Frequency: {closest_note[1]} Hz")

        # Check if the detected note matches the expected note
        if abs(closest_note[1] - pitch) < 5:  # Allow some tolerance
            print(f"Matched note: {closest_note[0]}")
            current_note_index += 1

            # Highlight the current note on the sheet music image
            x, y, w, h = closest_note[3]
            highlighted_img = sheet_music_img.copy()
            cv2.rectangle(highlighted_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.imshow("Sheet Music", highlighted_img)
            cv2.waitKey(500)  # Display for 500 ms

            if current_note_index >= len(score):
                print("Finished playing the score!")
                break
        else:
            print("No match. Keep playing...")

# Start score following
follow_score()

# Close stream
stream.stop_stream()
stream.close()
p.terminate()

# Close the OpenCV window
cv2.destroyAllWindows()
