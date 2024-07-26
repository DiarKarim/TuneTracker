import numpy as np
import pyaudio
from scipy.fftpack import fft
import matplotlib.pyplot as plt
import csv

# Load note coordinates from CSV file
csv_file = 'note_coordinates.csv'
note_coordinates = []

with open(csv_file, mode='r') as file:
    reader = csv.reader(file)
    next(reader)  # Skip the header row
    for row in reader:
        x, y, width, height = map(int, row)
        note_coordinates.append((x, y, width, height))
        
# Predefined list of expected notes (frequency in Hz) and corresponding lyrics
score = [
    # "Twinkle Twinkle Little Star"
    ("E5", 659.26, "Twinkle"), ("E5", 659.26, "Twinkle"), ("B5", 987.77, "little"), ("B5", 987.77, "star"),
    ("C#6", 1108.73, "How"), ("C#6", 1108.73, "I"), ("B5", 987.77, "wonder"),

    ("A5", 880.00, "what"), ("A5", 880.00, "you"), ("G#5", 830.61, "are"),
    ("G#5", 830.61, "Up"), ("F#5", 739.99, "above"), ("F#5", 739.99, "the"), ("E5", 659.26, "world"),

    # "Like a Diamond in the Sky"
    ("B5", 987.77, "so"), ("B5", 987.77, "high"), ("A5", 880.00, "Like"), ("A5", 880.00, "a"),
    ("G#5", 830.61, "diamond"), ("G#5", 830.61, "in"), ("F#5", 739.99, "the"),
    ("B5", 987.77, "sky"), ("B5", 987.77, "Twinkle"), ("A5", 880.00, "Twinkle"), ("A5", 880.00, "little"),

    # "Twinkle Twinkle Little Star"
    ("E5", 659.26, "star"), ("E5", 659.26, "How"), ("B5", 987.77, "I"), ("B5", 987.77, "wonder"),
    ("C#6", 1108.73, "what"), ("C#6", 1108.73, "you"), ("B5", 987.77, "are"),

    ("A5", 880.00, "Twinkle"), ("A5", 880.00, "Twinkle"), ("G#5", 830.61, "little"), ("G#5", 830.61, "star"),
    ("F#5", 739.99, "How"), ("F#5", 739.99, "I"), ("E5", 659.26, "wonder"),
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
    current_lyric = ""

    while current_note_index < len(score):
        # Read audio data from stream
        data = stream.read(CHUNK)
        # Detect pitch
        pitch = detect_pitch(data)
        # print(f"Detected pitch: {pitch:.2f} Hz")

        # Find the closest note
        closest_note = min(score, key=lambda note: abs(note[1] - pitch))
        # print(f"Closest note: {closest_note[0]}, Frequency: {closest_note[1]} Hz")

        # Check if the detected note matches the expected note
        if abs(closest_note[1] - pitch) < 5:  # Allow some tolerance
            # print(f"Matched note: {closest_note[0]}")
            current_lyric = closest_note[2]
            print(f"Current Lyric: {current_lyric}")
            current_note_index += 1
            if current_note_index >= len(score):
                print("Finished playing the score!")
                break
            else:
                next_lyric = score[current_note_index][2]
                print(f"Next expected lyric: {next_lyric}")
        else:
            print("No match. Keep playing...")

# Start score following
follow_score()

# Close stream
stream.stop_stream()
stream.close()
p.terminate()
