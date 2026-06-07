from youtube_transcript_api import YouTubeTranscriptApi
from youtube_comment_downloader import YoutubeCommentDownloader

# Ensures transcript has been gotten
# If not, tries to get transcript
def ensure_transcript(transcript, video_id):
    if transcript == "--N/A--":
        try:
            ytt_api = YouTubeTranscriptApi()
            response = ytt_api.fetch(video_id)

            transcript_str = ""

            for line in response:
                transcript_str += line.text + " "
            
            return transcript_str.strip()

        except Exception as e:
            print("Error fetching transcript:", str(e))
    else:
        return transcript

def ensure_comments(comments, video_id):
    if comments == "--N/A--":
        try:
            ytt_api = YoutubeCommentDownloader()
            comments = ytt_api.get_comments(video_id)

            comments_str = "\n\n".join([comment['text'].strip() for comment in comments])
            
            return comments_str

        except Exception as e:
            print("Error fetching comments:", str(e))
    else:
        return comments