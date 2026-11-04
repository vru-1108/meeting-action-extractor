import json
import requests
import pandas as pd
import streamlit as st

# --------------------------------------------------
# Configuration
# --------------------------------------------------

API_URL = "http://127.0.0.1:8000/api/v1/meetings/analyze"

st.set_page_config(
    page_title="Meeting Action Extractor",
    page_icon="📝",
    layout="wide"
)

# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("📝 Meeting Intelligence & Action Extractor")
st.write(
    "Upload a meeting transcript or paste its contents "
    "to extract summaries, decisions, and action items."
)

st.divider()

# --------------------------------------------------
# Transcript Input
# --------------------------------------------------

st.subheader("1. Provide Meeting Transcript")

uploaded_file = st.file_uploader(
    "Upload a transcript (.txt)",
    type=["txt"]
)

transcript = st.text_area(
    "Or paste your meeting transcript here",
    height=250,
    placeholder=(
        "Example:\n"
        "Sarah will complete API integration by Wednesday. "
        "John will prepare testing documentation by Friday. "
        "The team decided to use PostgreSQL."
    )
)

# --------------------------------------------------
# Analyze Transcript
# --------------------------------------------------

if st.button("Analyze Meeting", type="primary"):

    if uploaded_file is not None:
        try:
            transcript = uploaded_file.getvalue().decode("utf-8")
        except UnicodeDecodeError:
            st.error("Please upload a valid UTF-8 text file.")
            st.stop()

    if not transcript or not transcript.strip():
        st.warning("Please upload or enter a meeting transcript.")
        st.stop()

    with st.spinner("Analyzing meeting transcript... This may take a moment."):

        try:
            response = requests.post(
                API_URL,
                json={"transcript": transcript},
                timeout=300
            )

            if response.status_code != 200:
                try:
                    error_detail = response.json().get(
                        "detail", "Something went wrong."
                    )
                except ValueError:
                    error_detail = response.text

                st.error(f"Analysis failed: {error_detail}")
                st.stop()

            data = response.json()
            result = data["result"]

            st.session_state["meeting_result"] = result
            st.session_state["guardrail_issues"] = data.get(
                "guardrail_issues", []
            )

        except requests.exceptions.ConnectionError:
            st.error(
                "Could not connect to FastAPI. "
                "Make sure the backend is running."
            )
            st.stop()

        except requests.exceptions.Timeout:
            st.error(
                "The analysis took too long. "
                "Please try again."
            )
            st.stop()

        except requests.exceptions.RequestException as error:
            st.error(f"Request failed: {error}")
            st.stop()

# --------------------------------------------------
# Display Results
# --------------------------------------------------

if "meeting_result" in st.session_state:

    result = st.session_state["meeting_result"]
    guardrail_issues = st.session_state.get(
        "guardrail_issues", []
    )

    st.divider()
    st.header("2. Meeting Analysis")

    # Summary
    st.subheader("Meeting Summary")
    st.write(result.get("summary", "No summary available."))

    # Key Topics
    st.subheader("Key Topics")

    topics = result.get("key_topics", [])

    if topics:
        for topic in topics:
            st.markdown(f"- {topic}")
    else:
        st.info("No key topics identified.")

    # Decisions
    st.subheader("Decisions")

    decisions = result.get("decisions", [])

    if decisions:
        for index, decision in enumerate(decisions, start=1):
            st.markdown(f"**{index}. {decision['decision']}**")
            st.caption(f"Evidence: {decision['source_text']}")
    else:
        st.info("No explicit decisions identified.")

    # Action Items
    st.subheader("Action Items")

    action_items = result.get("action_items", [])

    if action_items:
        action_df = pd.DataFrame(action_items)

        display_columns = [
            "task",
            "owner",
            "deadline",
            "priority",
            "status",
            "source_text"
        ]

        action_df = action_df.reindex(columns=display_columns)

        st.dataframe(
            action_df,
            use_container_width=True,
            hide_index=True
        )

        # CSV Download
        csv_data = action_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="Download Action Items (CSV)",
            data=csv_data,
            file_name="meeting_action_items.csv",
            mime="text/csv"
        )

    else:
        st.info("No action items identified.")

    # Open Questions
    st.subheader("Open Questions")

    open_questions = result.get("open_questions", [])

    if open_questions:
        for question in open_questions:
            st.markdown(f"- {question}")
    else:
        st.info("No open questions identified.")

    # Guardrail Issues
    if guardrail_issues:
        st.warning("Some extracted evidence needs human review.")

        for issue in guardrail_issues:
            st.write(f"- {issue}")
    else:
        st.success("Evidence checks passed.")

    # JSON Download
    st.divider()
    st.subheader("Export Results")

    json_data = json.dumps(
        result,
        indent=4,
        ensure_ascii=False
    )

    st.download_button(
        label="Download Full Analysis (JSON)",
        data=json_data,
        file_name="meeting_analysis.json",
        mime="application/json"
    )