import streamlit as st
import sys
import os
import pandas as pd
import plotly.express as px
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from engine.inference import calculate_priority
from utils.scheduler import allocate_study_time

st.set_page_config(page_title="Exam Prep Assistant", layout="wide")

st.markdown("""
    <style>
    .big-title { font-size:40px !important; color: #4CAF50; font-weight: bold; }
    .subtitle { font-size:20px !important; color: #666; }
    </style>
    <div class='big-title'>📘 Intelligent Exam Preparation Assistant</div>
    <div class='subtitle'>An AI Expert System for building smart, personalized study plans</div>
""", unsafe_allow_html=True)

with st.form("exam_form"):
    st.markdown("### 🧑‍🎓 Student Info")
    exam_date = st.date_input("📅 Exam Date", value=datetime(2025, 6, 10))
    current_date = st.date_input("🕒 Today's Date", value=datetime.today())
    daily_hours = st.slider("⏱️ Daily Study Hours", 1, 10, 4)
    learner_type = st.selectbox("🧠 Your Learning Style", ["fast", "average", "needs support"])
    topic_count = st.number_input("📚 Number of Topics", min_value=1, max_value=20, value=5)

    st.markdown("### 📘 Enter Topic Details")
    topics = []
    for i in range(topic_count):
        with st.expander(f"Topic {i + 1}"):
            name = st.text_input("Topic Name", key=f"name_{i}")
            score = st.slider("Your Score (0–100)", 0, 100, 50, key=f"score_{i}")
            difficulty = st.selectbox("Difficulty", ["easy", "medium", "hard"], key=f"diff_{i}")
            importance = st.selectbox("Importance", ["optional", "important", "core"], key=f"imp_{i}")
            if name:
                topics.append({
                    "name": name,
                    "score": score,
                    "difficulty": difficulty,
                    "importance": importance
                })

    submitted = st.form_submit_button("🧠 Generate Study Plan")

if submitted:
    if not topics:
        st.error("Please enter at least one topic.")
    elif any(not t["name"] for t in topics):
        st.error("All topics must have names.")
    else:
        student_profile = {
            "current_date": current_date,
            "exam_date": exam_date,
            "daily_study_hours": daily_hours,
            "learner_type": learner_type,
            "topics": topics
        }

        for topic in student_profile["topics"]:
            topic["priority"] = calculate_priority(topic, learner_type)

        plan = allocate_study_time(student_profile)

        st.success("🎯 Study Plan generated successfully!")
        st.markdown("### 🗂️ Your Personalized Study Plan")

        df = pd.DataFrame(plan)
        df = df.rename(columns={
            "name": "Topic",
            "priority": "Priority",
            "allocated_hours": "Allocated Hours"
        })
        st.dataframe(df, use_container_width=True)

        st.markdown("### 📊 Study Time Distribution")
        fig = px.pie(df, names="Topic", values="Allocated Hours", title="Time Allocation per Topic")
        st.plotly_chart(fig)

        st.markdown("### 📊 Topic Priorities")
        fig2 = px.bar(df, x="Topic", y="Priority", color="Priority", text="Priority", title="Calculated Priority per Topic")
        st.plotly_chart(fig2)

        st.markdown("### 📥 Export")
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Download CSV", data=csv, file_name="study_plan.csv", mime="text/csv")

        # Smart Suggestions
        st.markdown("### 🔍 Smart Recommendations")
        low_score_core = [t for t in plan if t["score"] < 50 and t["importance"] == "core"]
        if low_score_core:
            st.info("Focus more on these high-priority core topics with low performance:")
            for t in low_score_core:
                st.write(f"• **{t['name']}** – Score: {t['score']}, Difficulty: {t['difficulty']}")
        else:
            st.success("Great! No urgent topics need extra attention.")

with st.expander("📘 About the Expert System"):
    st.markdown("""
    This system is built using classic AI Expert System architecture:

    - **Knowledge Base**: Rule weights for difficulty and importance
    - **Inference Engine**: Applies those rules to input data
    - **Working Memory**: Your entered profile and topic data

    It calculates a priority score and allocates study time accordingly.
    """)