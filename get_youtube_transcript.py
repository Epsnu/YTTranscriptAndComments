from youtube_transcript_api import YouTubeTranscriptApi
from datetime import date

def get_transcript(video_id):
    try:
        ytt_api = YouTubeTranscriptApi()
        transcript = ytt_api.fetch(video_id)

        transcript_str = ""

        for line in transcript:
            transcript_str += line.text + " "

        print_transcript(transcript_str)

        save_transcript(transcript_str)

    except Exception as e:
        print("Error fetching transcript:", str(e))

def print_transcript(transcript):
    print("Would you like to see the transcript now? (y/n)")
    choice = input().lower()
    if choice == "y":
        print(transcript, "\n\n")

def save_transcript(transcript):
    print("Would you like to save the transcript to your downloads folder? (y/n)")
    today = date.today()
    outFile = f"C:/Users/tobia/Downloads/transcript_{today}.txt"
    choice = input().lower()
    if choice == "y":
        with open(outFile, "w", encoding="utf-8") as f:
            f.write(transcript)
            f.write("\n\n-----------END OF TRANSCRIPT-----------\n\n")
        print(f"Transcript saved to {outFile}")