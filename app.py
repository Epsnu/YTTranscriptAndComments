from get_youtube_transcript import get_transcript
from get_youtube_comments import get_comments
from get_youtube_transcript_summary import get_transcript_summary
from get_youtube_comments_summary import get_comments_summary
from pytube import extract
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

def reset():
    video_url = st.text_input("What YouTube video do you want to learn about?", placeholder="YouTube Video URL")
    video_id = extract.video_id(video_url)
    transcript = "--N/A--"
    comments = "--N/A--"
    transcript_summary = "--N/A--"
    comments_summary = "--N/A--"
    return video_id, transcript, comments, transcript_summary, comments_summary

def main():
    video_id, transcript, comments, transcript_summary, comments_summary = reset()

    with st.expander("Summary"):
        transcript, transcript_summary = get_transcript_summary(transcript, transcript_summary, video_id)
        st.write(transcript_summary)
    with st.expander("Transcript"):
        transcript, transcript_summary = get_transcript_summary(transcript, transcript_summary, video_id)
        st.write(transcript)
    with st.expander("Comments Summary"):
        comments, comments_summary = get_comments_summary(comments, comments_summary, video_id)
        st.write(comments_summary)
    with st.expander("Comments"):
        comments = get_comments(comments, video_id)
        st.write(comments)

if __name__ == "__main__":
    main()