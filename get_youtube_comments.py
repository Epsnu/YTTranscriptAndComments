from youtube_comment_downloader import YoutubeCommentDownloader

def get_comments(video_id):
    try:
        ytt_api = YoutubeCommentDownloader()
        comments = ytt_api.get_comments(video_id)

        comments_str = "\n--------------------------\n".join([comment['text'] for comment in comments])
        outFile = "comments.txt"

        print_comments(comments_str)

        save_comments(comments_str, outFile)

    except Exception as e:
        print("Error fetching comments:", str(e))

def print_comments(comments):
    print("Would you like to see the comments now? (y/n)")
    choice = input().lower()
    if choice == "y":
        print(comments, "\n\n")

def save_comments(comments, outFile):
    print("Would you like to save the comments to your downloads folder? (y/n)")
    choice = input().lower()
    if choice == "y":
        with open(outFile, "w", encoding="utf-8") as f:
            f.write(comments)
        print(f"Comments saved to {outFile}")