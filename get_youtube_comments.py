from utils import ensure_comments
from datetime import date
from pathlib import Path

def get_comments(comments, video_id):
    comments = ensure_comments(comments, video_id)

    print_comments(comments)

    save_comments(comments)

    return comments

def print_comments(comments):
    print("Would you like to see the comments now? (y/n)")
    choice = input().lower()
    if choice == "y":
        print(comments, "\n\n")

def save_comments(comments):
    print("Would you like to save the comments to your downloads folder? (y/n)")
    today = date.today()
    outFile = Path.home() / f"Downloads/comments_{today}.txt"
    choice = input().lower()
    if choice == "y":
        with open(outFile, "w", encoding="utf-8") as f:
            f.write("\n\n-----------BEGIN COMMENTS-----------\n\n")
            f.write(comments)
            f.write("\n\n-----------END COMMENTS-----------\n\n")
        print(f"Comments saved to {outFile}")