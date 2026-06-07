from utils import ensure_transcript
from datetime import date
from pathlib import Path

def get_transcript(transcript, video_id):
    transcript = ensure_transcript(transcript, video_id)

    # print_transcript(transcript)

    # save_transcript(transcript)

    return transcript

def print_transcript(transcript):
    print("Would you like to see the transcript now? (y/n)")
    choice = input().lower()
    if choice == "y":
        print(transcript, "\n\n")

def save_transcript(transcript):
    print("Would you like to save the transcript to your downloads folder? (y/n)")
    try:
        today = date.today()
        outFile = Path.home() / f"Downloads/transcript_{today}.txt"
        choice = input().lower()
        if choice == "y":
            with open(outFile, "w", encoding="utf-8") as f:
                f.write("\n\n-----------BEGIN TRANSCRIPT-----------\n\n")
                f.write(transcript)
                f.write("\n\n-----------END TRANSCRIPT-----------\n\n")
            print(f"Transcript saved to {outFile}")
    except Exception as e:
        print("Error saving transcript:", str(e))