import os

from dotenv import load_dotenv
from dotenv import set_key
from google import genai
from pytube import extract
from html import escape
import streamlit as st

from utils import (
    comments_string,
    ensure_comments,
    ensure_comments_summary,
    ensure_transcript,
    ensure_transcript_summary,
)

load_dotenv()


PAGE_TITLE = "YouTube Video Info"
ENV_FILE = ".env"
API_KEY_ENV_VAR = "GEMINI_API_KEY"


def get_saved_api_key():
    saved_api_key = os.getenv(API_KEY_ENV_VAR, "").strip()
    return saved_api_key or ""


def persist_api_key(api_key):
    api_key = api_key.strip()
    if not api_key:
        return

    set_key(ENV_FILE, API_KEY_ENV_VAR, api_key)
    os.environ[API_KEY_ENV_VAR] = api_key
    st.session_state.api_key = api_key


def verify_api_key(api_key):
    client = genai.Client(api_key=api_key)
    client.models.generate_content(
        model="gemini-flash-lite-latest",
        contents="Reply with OK.",
    )

def ensure_api_key():
    if st.session_state.get("api_key"):
        return

    with st.container():
        st.markdown(
            """
            <div style="
                padding: 1.5rem;
                background: #ffffff;
                border: 2px solid #d0d7e2;
                border-radius: 10px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.08);
                max-width: 420px;
                margin: 3rem auto;
                text-align: center;
            ">
                <h3 style="margin-bottom: 0.5rem;">Enter Your Gemini API Key</h3>
                <p style="color: #555; margin-bottom: 1rem;">
                    This key is stored locally in your project `.env` file and never sent anywhere except Gemini.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
        with st.form("api_key_form"):
            api_key = st.text_input(
                "Enter Gemini API key",
                type="password",
                placeholder="xJ.aLeq...",
                key="api_key_input",
            )
            submitted = st.form_submit_button("Save API key")

        if submitted:
            if api_key.strip():
                with st.spinner("Verifying API key..."):
                    try:
                        verify_api_key(api_key)
                    except Exception as exc:
                        st.error(f"API key verification failed: {exc}")
                    else:
                        persist_api_key(api_key)
                        st.success("API key saved locally. You should not be prompted again.")
                        st.rerun()
            else:
                st.error("Please enter a valid API key.")
    st.stop()

def configure_page():
    st.set_page_config(
        page_title=PAGE_TITLE,
        page_icon=":bar_chart:",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.markdown(
        """
        <style>
            :root {
                --app-border: #d9dee8;
                --app-muted: #667085;
                --app-panel: #ffffff;
                --app-soft: #f5f7fb;
                --app-text: #111827;
                --app-accent: #b42318;
            }

            .stApp {
                background:
                    linear-gradient(180deg, #f8fafc 0%, #eef2f7 100%);
                color: var(--app-text);
            }

            .main .block-container {
                max-width: 1180px;
                padding-top: 2rem;
                padding-bottom: 3rem;
            }

            [data-testid="stSidebar"] {
                background: #ffffff;
                border-right: 1px solid var(--app-border);
            }

            .app-header {
                border-bottom: 1px solid var(--app-border);
                margin-bottom: 1.5rem;
                padding-bottom: 1.25rem;
            }

            .app-kicker {
                color: var(--app-accent);
                font-size: 0.78rem;
                font-weight: 700;
                letter-spacing: 0.08em;
                margin-bottom: 0.35rem;
                text-transform: uppercase;
            }

            .app-header h1 {
                color: #101828;
                font-size: 2.2rem;
                font-weight: 760;
                letter-spacing: 0;
                line-height: 1.1;
                margin: 0;
            }

            .app-subtitle {
                color: var(--app-muted);
                font-size: 1rem;
                margin-top: 0.65rem;
                max-width: 780px;
            }

            .status-card {
                background: var(--app-panel);
                border: 1px solid var(--app-border);
                border-radius: 8px;
                box-shadow: 0 10px 28px rgba(16, 24, 40, 0.06);
                padding: 1rem;
            }

            .status-label {
                color: var(--app-muted);
                font-size: 0.78rem;
                font-weight: 700;
                letter-spacing: 0.04em;
                text-transform: uppercase;
            }

            .status-value {
                color: #101828;
                font-size: 1.35rem;
                font-weight: 720;
                margin-top: 0.25rem;
            }

            div[data-testid="stMetric"] {
                background: #ffffff;
                border: 1px solid var(--app-border);
                border-radius: 8px;
                padding: 0.95rem 1rem;
            }

            div[data-testid="stMetricLabel"] {
                color: var(--app-muted);
            }

            div[data-testid="stTabs"] [role="tablist"] {
                border-bottom: 1px solid var(--app-border);
                gap: 0.35rem;
            }

            div[data-testid="stTabs"] [role="tab"] {
                border-radius: 6px 6px 0 0;
                padding: 0.75rem 1rem;
            }

            .comment-row {
                background: #ffffff;
                border: 1px solid var(--app-border);
                border-radius: 8px;
                margin-bottom: 0.65rem;
                padding: 0.85rem 1rem;
            }

            .empty-panel {
                background: var(--app-soft);
                border: 1px dashed #c8cfdb;
                border-radius: 8px;
                color: var(--app-muted);
                padding: 1.25rem;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def initialize_state():
    defaults = {
        "api_key": get_saved_api_key(),
        "video_url": "",
        "video_id": None,
        "transcript_loaded_video_id": None,
        "comments_loaded_video_id": None,
        "transcript": None,
        "transcript_summary": None,
        "comments": None,
        "comments_summary": None,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_video_state(video_url, video_id):
    st.session_state.video_url = video_url
    st.session_state.video_id = video_id
    st.session_state.transcript_loaded_video_id = None
    st.session_state.comments_loaded_video_id = None
    st.session_state.transcript = None
    st.session_state.transcript_summary = None
    st.session_state.comments = None
    st.session_state.comments_summary = None


def parse_video_url(video_url):
    if not video_url.strip():
        return None

    try:
        return extract.video_id(video_url)
    except Exception:
        return None


def transcript_word_count():
    transcript = st.session_state.transcript
    if not transcript:
        return 0
    return len(transcript.split())


def comment_count():
    comments = st.session_state.comments
    if not isinstance(comments, list):
        return 0
    return len(comments)


def render_header():
    st.markdown(
        f"""
        <div class="app-header">
            <div class="app-kicker">I'm too lazy to watch</div>
            <h1>{PAGE_TITLE}</h1>
            <div class="app-subtitle">
                Pull transcripts and comments and summarize them. Export them as well!
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar():
    with st.sidebar:
        st.header("Video")
        video_url = st.text_input(
            "YouTube URL",
            value=st.session_state.video_url,
            placeholder="https://www.youtube.com/watch?v=...",
        )

        video_id = parse_video_url(video_url)
        if video_url and video_id is None:
            st.error("Enter a valid YouTube URL.")
        elif video_id:
            st.success("Video ready.")

        if video_id != st.session_state.video_id:
            reset_video_state(video_url, video_id)
        else:
            st.session_state.video_url = video_url

        st.divider()
        st.caption("Local dashboard")
        st.write("Double-click `run_app.bat` to launch this screen.")

        if st.button("Clear current video", use_container_width=True):
            reset_video_state("", None)
            st.rerun()


def fetch_transcript():
    with st.spinner("Fetching transcript..."):
        st.session_state.transcript = ensure_transcript(
            st.session_state.transcript,
            st.session_state.video_id,
        )


def fetch_transcript_summary():
    if st.session_state.transcript is None:
        fetch_transcript()

    if not st.session_state.transcript:
        return

    with st.spinner("Summarizing transcript..."):
        st.session_state.transcript_summary = ensure_transcript_summary(
            st.session_state.transcript,
            st.session_state.transcript_summary,
        )


def fetch_comments():
    with st.spinner("Fetching comments..."):
        st.session_state.comments = ensure_comments(
            st.session_state.comments,
            st.session_state.video_id,
        )


def fetch_comments_summary():
    if st.session_state.comments is None:
        fetch_comments()

    if not st.session_state.comments:
        return

    with st.spinner("Summarizing comments..."):
        st.session_state.comments_summary = ensure_comments_summary(
            st.session_state.comments,
            st.session_state.comments_summary,
        )


def fetch_transcript_data():
    if st.session_state.video_id is None:
        return False

    if st.session_state.transcript_loaded_video_id == st.session_state.video_id:
        return False

    fetch_transcript()
    fetch_transcript_summary()
    st.session_state.transcript_loaded_video_id = st.session_state.video_id
    return True


def fetch_comment_data():
    if st.session_state.video_id is None:
        return False

    if st.session_state.comments_loaded_video_id == st.session_state.video_id:
        return False

    fetch_comments()
    fetch_comments_summary()
    st.session_state.comments_loaded_video_id = st.session_state.video_id
    return True


def render_metrics():
    metric_two, metric_three = st.columns(2)
    metric_two.metric("Transcript Words", f"{transcript_word_count():,}")
    metric_three.metric("Comments Loaded", f"{comment_count():,}")


def render_overview_tab():
    left, right = st.columns([1.15, 0.85], gap="large")

    with left:
        st.subheader("Video Summary")
        if st.session_state.transcript_summary:
            st.markdown(st.session_state.transcript_summary)
        else:
            st.markdown(
                '<div class="empty-panel">Paste a YouTube URL to generate a transcript summary.</div>',
                unsafe_allow_html=True,
            )

    with right:
        st.subheader("Preview")
        if st.session_state.video_url:
            st.video(st.session_state.video_url)
        else:
            st.markdown(
                '<div class="empty-panel">Paste a YouTube URL in the sidebar to load a preview.</div>',
                unsafe_allow_html=True,
            )

        st.subheader("Comment Summary")
        if st.session_state.comments_summary:
            st.markdown(st.session_state.comments_summary)
        elif st.session_state.video_id and st.session_state.comments_loaded_video_id != st.session_state.video_id:
            st.markdown(
                '<div class="empty-panel">Loading comments summary after the transcript finishes.</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                '<div class="empty-panel">Paste a YouTube URL to summarize audience reactions.</div>',
                unsafe_allow_html=True,
            )


def render_transcript_tab():
    st.subheader("Transcript")
    if not st.session_state.transcript:
        st.markdown(
            '<div class="empty-panel">Paste a YouTube URL to view the full transcript.</div>',
            unsafe_allow_html=True,
        )
        return

    st.download_button(
        "Download Transcript",
        data=st.session_state.transcript,
        file_name=f"transcript_{st.session_state.video_id}.txt",
        use_container_width=False,
    )
    st.text_area(
        "Full transcript",
        value=st.session_state.transcript,
        height=420,
        label_visibility="collapsed",
    )


def render_comments_tab():
    st.subheader("Comments")
    comments = st.session_state.comments
    if not isinstance(comments, list) or not comments:
        if st.session_state.video_id and st.session_state.comments_loaded_video_id != st.session_state.video_id:
            st.markdown(
                '<div class="empty-panel">Comments are still loading. The transcript and video summary are ready to read now.</div>',
                unsafe_allow_html=True,
            )
            return

        st.markdown(
            '<div class="empty-panel">Paste a YouTube URL to browse and search comments.</div>',
            unsafe_allow_html=True,
        )
        return

    query = st.text_input("Search comments", placeholder="Search words, phrases, or reactions")
    normalized_query = query.strip().lower()

    filtered_comments = []
    for comment in comments:
        text = comment.get("text", "").strip() if isinstance(comment, dict) else str(comment)
        if not normalized_query or normalized_query in text.lower():
            filtered_comments.append(text)

    st.caption(f"Showing {len(filtered_comments):,} of {len(comments):,} comments")
    st.download_button(
        "Download Comments",
        data=comments_string(comments),
        file_name=f"comments_{st.session_state.video_id}.txt",
    )

    for text in filtered_comments[:250]:
        st.markdown(f'<div class="comment-row">{escape(text)}</div>', unsafe_allow_html=True)

    if len(filtered_comments) > 250:
        st.info("Showing the first 250 matching comments to keep the dashboard responsive.")


def render_downloads_tab():
    st.subheader("Exports")
    col_one, col_two = st.columns(2)

    with col_one:
        st.write("Transcript files")
        st.download_button(
            "Download Transcript",
            data=st.session_state.transcript or "",
            file_name=f"transcript_{st.session_state.video_id or 'video'}.txt",
            disabled=st.session_state.transcript is None,
            use_container_width=True,
        )
        st.download_button(
            "Download Video Summary",
            data=st.session_state.transcript_summary or "",
            file_name=f"transcript_summary_{st.session_state.video_id or 'video'}.md",
            disabled=st.session_state.transcript_summary is None,
            use_container_width=True,
        )

    with col_two:
        st.write("Comment files")
        comments_data = comments_string(st.session_state.comments) if st.session_state.comments else ""
        st.download_button(
            "Download Comments",
            data=comments_data,
            file_name=f"comments_{st.session_state.video_id or 'video'}.txt",
            disabled=st.session_state.comments is None,
            use_container_width=True,
        )
        st.download_button(
            "Download Comment Summary",
            data=st.session_state.comments_summary or "",
            file_name=f"comments_summary_{st.session_state.video_id or 'video'}.md",
            disabled=st.session_state.comments_summary is None,
            use_container_width=True,
        )


def render_dashboard():
    if st.session_state.video_id is None:
        st.info("Paste a YouTube URL in the sidebar to begin.")
    else:
        fetch_transcript_data()

    render_metrics()
    st.divider()

    overview_tab, transcript_tab, comments_tab, downloads_tab = st.tabs(
        ["Overview", "Transcript", "Comments", "Exports"]
    )
    with overview_tab:
        render_overview_tab()
    with transcript_tab:
        render_transcript_tab()
    with comments_tab:
        render_comments_tab()
    with downloads_tab:
        render_downloads_tab()

    if st.session_state.video_id is not None:
        comments_loaded = fetch_comment_data()
        if comments_loaded:
            st.rerun()


def main():
    configure_page()
    initialize_state()
    if not ("api_key" in st.session_state and st.session_state.api_key):
        ensure_api_key()
        return
    render_sidebar()
    render_header()
    render_dashboard()


if __name__ == "__main__":
    main()
