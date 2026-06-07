from google import genai
from utils import ensure_transcript
from datetime import date
from pathlib import Path
import os

def get_transcript_summary(transcript, transcript_summary, video_id):
    transcript = ensure_transcript(transcript, video_id)

    if transcript_summary == "--N/A--":
        # get summary using gemini latest flash-lite model
        content = '''
            Summarize the YouTube video given its transcript. Do not include emojis. Aim to make a summary under 10 percent of the transcript length, unless transcript is reasonably short. Keep it paragraph form, using little special characters. Transcript:\n
            ''' + transcript
        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        response = client.models.generate_content(
            model="gemini-flash-lite-latest",
            contents=content
        )
        summary_str = response.text
    else:
        summary_str = transcript_summary

    # print_summary(summary_str)

    # save_summary(summary_str)

    return transcript, summary_str

def print_summary(transcript):
    print("Summary of YouTube Transcript:\n")
    print(transcript, "\n\n")

def save_summary(summary):
    print("Would you like to save the summary to your downloads folder? (y/n)")
    try:
        today = date.today()
        outFile = Path.home() / f"Downloads/transcript_summary_{today}.txt"
        choice = input().lower()
        if choice == "y":
            with open(outFile, "w", encoding="utf-8") as f:
                f.write("\n\n-----------BEGIN SUMMARY-----------\n\n")
                f.write(summary)
                f.write("\n\n-----------END SUMMARY-----------\n\n")
            print(f"Summary saved to {outFile}")
    except Exception as e:
        print("Error saving summary:", str(e))