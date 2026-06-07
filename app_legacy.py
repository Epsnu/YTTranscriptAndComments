from get_youtube_transcript import get_transcript
from get_youtube_comments import get_comments
from get_youtube_transcript_summary import get_transcript_summary
from get_youtube_comments_summary import get_comments_summary
from pytube import extract
from dotenv import load_dotenv

load_dotenv()

def reset():
    video_url = input("Enter the YouTube video URL: ")
    video_id = extract.video_id(video_url)
    transcript = "--N/A--"
    comments = "--N/A--"
    transcript_summary = "--N/A--"
    comments_summary = "--N/A--"
    return video_id, transcript, comments, transcript_summary, comments_summary

def main():
    video_id, transcript, comments, transcript_summary, comments_summary = reset()
    
    while True:
        print("\nChoose an option:")
        print("1. Get transcript")
        print("2. Get transcript summary")
        print("3. Get comments")
        print("4. Get comments summary")
        print("5. New Video")
        print("6. Exit")
        choice = input("Enter your choice (1-6): ")
        if choice == "1":
            transcript = get_transcript(transcript, video_id)
        elif choice == "2":
            transcript, transcript_summary = get_transcript_summary(transcript, transcript_summary, video_id)
        elif choice == "3":
            comments = get_comments(comments, video_id)
        elif choice == "4":
            comments, comments_summary = get_comments_summary(comments, comments_summary, video_id)
        elif choice == "5":
            video_id, transcript, comments, transcript_summary, comments_summary = reset()
        elif choice == "6":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter a number 1-6.")

if __name__ == "__main__":
    main()