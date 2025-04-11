import streamlit as st
import pandas as pd
import datetime
import random

st.set_page_config(page_title="📘 StudyPal – Smart Study Planner", layout="centered")

st.title("📘 StudyPal – Smart Study Planner & Tracker")
st.markdown("Plan your study week, track your progress, and stay productive!")

st.divider()

# ---- USER INPUT SECTION ----
st.header("🧠 Step 1: Add Your Subjects & Topics")
subjects_input = st.text_area(
    "Enter subjects and topics (format: Subject: topic1, topic2, ...)",
    "Math: Algebra, Geometry\nScience: Motion, Atoms\nEnglish: Grammar, Essay Writing"
)

st.header("⏳ Step 2: Set Daily Study Hours")
daily_hours = st.slider("How many hours can you study per day?", 1, 10, 4)

# ---- PARSE INPUT AND GENERATE PLAN ----
def parse_subjects(input_str):
    plan = []
    lines = input_str.strip().split("\n")
    for line in lines:
        if ":" in line:
            subject, topics = line.split(":")
            topics_list = [t.strip() for t in topics.split(",")]
            for topic in topics_list:
                plan.append({
                    "Subject": subject.strip(),
                    "Topic": topic,
                    "Completed": False
                })
    return pd.DataFrame(plan)

# ---- GENERATE PLAN BUTTON ----
if st.button("📅 Generate Study Plan"):
    df = parse_subjects(subjects_input)
    if df.empty:
        st.error("Please enter valid subjects and topics.")
    else:
        st.session_state.study_plan = df
        st.success("Your study plan has been created!")

# ---- DISPLAY PLAN ----
if "study_plan" in st.session_state:
    st.header("📋 Your Study Plan")

    df = st.session_state.study_plan
    edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)
    st.session_state.study_plan = edited_df

    # ---- Progress Calculation ----
    total = len(edited_df)
    completed = edited_df["Completed"].sum()
    progress = int((completed / total) * 100) if total > 0 else 0

    st.subheader("📊 Progress Overview")
    st.progress(progress)
    st.success(f"✅ {completed} out of {total} topics completed ({progress}%)")

    # ---- Optional Tips ----
    with st.expander("💡 Need a Productivity Tip?"):
        tips = [
            "📌 Use Pomodoro technique: 25 min study + 5 min break.",
            "📚 Teach someone to reinforce your understanding.",
            "🧘 Take regular breaks to avoid burnout.",
            "📝 Review your notes after every study session.",
            "🎯 Set small goals to stay motivated."
        ]
        if st.button("Show Tip"):
            st.info(random.choice(tips))

# ---- FOOTER ----
st.divider()
st.caption("Made with ❤️ in Python & Streamlit | StudyPal © 2025")
