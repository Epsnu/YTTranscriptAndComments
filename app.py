from get_youtube_transcript import get_transcript
from get_youtube_comments import get_comments
from pytube import extract

def main():
    video_url = input("Enter the YouTube video URL: ")
    video_id = extract.video_id(video_url)
    
    while True:
        print("\nChoose an option:")
        print("1. Get transcript")
        print("2. Get comments")
        print("3. Exit")
        choice = input("Enter your choice (1/2/3): ")
        if choice == "1":
            get_transcript(video_id)
        elif choice == "2":
            get_comments(video_id)
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()