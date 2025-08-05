import streamlit as st
from textblob import TextBlob
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Feedback Sentiment Analyzer", page_icon="🧠")

st.title("🧠 Training Feedback Sentiment Analyzer")
st.write("Paste trainee feedback below to check its sentiment.")

feedback = st.text_area("✍️ Enter trainee feedback here:")

if st.button("🔍 Analyze"):
    if feedback.strip():
        blob = TextBlob(feedback)
        polarity = blob.sentiment.polarity

        if polarity > 0:
            sentiment = "Positive 😊"
        elif polarity < 0:
            sentiment = "Negative 😠"
        else:
            sentiment = "Neutral 😐"

        st.success(f"**Sentiment:** {sentiment}")
        st.write(f"**Polarity Score:** `{polarity:.2f}`")

        data = {
            "Timestamp": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            "Feedback": [feedback],
            "Sentiment": [sentiment],
            "Polarity": [polarity]
        }

        df = pd.DataFrame(data)
        with open("feedback_log.csv", "a") as f:
            df.to_csv(f, header=f.tell()==0, index=False)
    else:
        st.warning("Please enter some feedback.")

st.markdown("---")
st.subheader("📋 Last 5 Feedback Entries")

try:
    log_df = pd.read_csv("feedback_log.csv")
    st.dataframe(log_df.tail(5))
except FileNotFoundError:
    st.info("No feedback has been submitted yet.")
