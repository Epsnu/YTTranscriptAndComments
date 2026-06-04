from google import genai
from utils import ensure_comments
from datetime import date
from pathlib import Path
import os

def get_comments_summary(comments, video_id):
    comments = ensure_comments(comments, video_id)

    # get summary using gemini latest flash-lite model
    content = '''
        Summarize people's reactions and discussions in this YouTube video's comments section in one or two sentences. Add another line listing common jokes, sayings, or themes used throughout. Do not include emojis. Don't use many special characters unless they are part of the "inside jokes" or "motifs" summary. Comments:\n
        ''' + comments
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    response = client.models.generate_content(
        model="gemini-flash-lite-latest",
        contents=content
    )
    summary_str = response.text

    print_summary(summary_str)

    save_summary(summary_str)

    return comments

def print_summary(transcript):
    print("Summary of YouTube Comments:\n")
    print(transcript, "\n\n")

def save_summary(summary):
    print("Would you like to save the summary to your downloads folder? (y/n)")
    try:
        today = date.today()
        outFile = Path.home() / f"Downloads/comments_summary_{today}.txt"
        choice = input().lower()
        if choice == "y":
            with open(outFile, "w", encoding="utf-8") as f:
                f.write("\n\n-----------BEGIN SUMMARY-----------\n\n")
                f.write(summary)
                f.write("\n\n-----------END SUMMARY-----------\n\n")
            print(f"Summary saved to {outFile}")
    except Exception as e:
        print("Error saving summary:", str(e))