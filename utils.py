from youtube_transcript_api import YouTubeTranscriptApi
from youtube_comment_downloader import YoutubeCommentDownloader
from google import genai
import os

def comments_string(comments):
    comments_str = "\n------\n".join([
        comment.get("text", "").strip() if isinstance(comment, dict) else str(comment).strip()
        for comment in comments
    ])
    return comments_str

# Ensures transcript has been gotten
# If not, tries to get transcript
def ensure_transcript(transcript, video_id):
    if transcript is None:
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
    if comments is None:
        try:
            ytt_api = YoutubeCommentDownloader()
            comments = list(ytt_api.get_comments(video_id))
        except Exception as e:
            comments = [f"Error fetching comments: {str(e)}"]
    return comments

def ensure_comments_summary(comments, comments_summary):
    if comments_summary is None:
        try:
            # get summary using gemini latest flash-lite model
            content = '''
                Summarize people's reactions and discussions in this YouTube video's comments section in one or two sentences. Add another line listing common jokes, sayings, or themes used throughout. Do not include emojis. Output should be formatted as Markdown. Use Markdown to present your output nicely. Comments delimited by "\n------\n":\n
                ''' + comments_string(comments)
            client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
            response = client.models.generate_content(
                model="gemini-flash-lite-latest",
                contents=content
            )
            comments_summary = response.text
        except Exception as e:
            comments_summary = f"Error fetching comments: {str(e)}"
    return comments_summary

def ensure_transcript_summary(transcript, transcript_summary):
    if transcript_summary is None:
        try:
            # get summary using gemini latest flash-lite model
            content = '''
                Summarize the YouTube video given its transcript. Do not include emojis. Aim to make a summary under 10 percent of the transcript length, unless transcript is reasonably short. Output should be formatted as Markdown. Use Markdown to present your output nicely. Transcript:\n
                ''' + transcript
            client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
            response = client.models.generate_content(
                model="gemini-flash-lite-latest",
                contents=content
            )
            transcript_summary = response.text
        except Exception as e:
            transcript_summary = f"Error fetching comments: {str(e)}"
    return transcript_summary
