import streamlit as st
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder

st.set_page_config(page_title="AI Learning", page_icon="🎓", layout="centered")

# ---------------- SESSION STATE ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ---------------- LOGIN PAGE ----------------
if not st.session_state.logged_in:

    st.markdown("<h1 style='text-align:center;'>🎓 AI Learning Assistant</h1>", unsafe_allow_html=True)

    name = st.text_input("Enter your name")

    if st.button("Start Learning"):
        if name:
            st.session_state.logged_in = True
            st.session_state.user = name
            st.rerun()
        else:
            st.warning("Please enter your name")

# ---------------- MAIN APP ----------------
else:

    st.success(f"Welcome {st.session_state.user} 👋")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    st.divider()

    # ---------- TRAIN MODEL ----------
    data = {
        "math_score": [90, 40, 65, 30, 85, 55, 20, 75],
        "time_spent": [120, 30, 60, 20, 110, 50, 15, 95],
        "level": ["Advanced","Beginner","Intermediate","Beginner",
                  "Advanced","Intermediate","Beginner","Advanced"]
    }

    df = pd.DataFrame(data)

    encoder = LabelEncoder()
    df["level_encoded"] = encoder.fit_transform(df["level"])

    X = df[["math_score","time_spent"]]
    y = df["level_encoded"]

    model = DecisionTreeClassifier()
    model.fit(X,y)

    # ---------- INPUT ----------
    st.subheader("📊 Enter Study Details")

    score = st.slider("Score", 0, 100, 50)
    time = st.slider("Study Time (minutes)", 0, 180, 60)

    # ---------- RECOMMEND FUNCTION ----------
    def recommend(level):
        if level == "Beginner":
            return ["Revise basics", "Watch concept videos", "Practice easy problems"], "🔰 Beginner"
        elif level == "Intermediate":
            return ["Solve exercises", "Read notes", "Take quizzes"], "📘 Intermediate"
        else:
            return ["Mock tests", "Hard problems", "Timed practice"], "🏆 Advanced"

    # ---------- PREDICT ----------
    if st.button("Get AI Recommendation 🤖"):

        # FIXED INPUT FORMAT (removes sklearn warning)
        input_data = pd.DataFrame([[score, time]],
                                  columns=["math_score","time_spent"])

        prediction = model.predict(input_data)
        level = encoder.inverse_transform(prediction)[0]

        recs, badge = recommend(level)

        st.subheader(f"Level: {badge}")

        # progress bar
        st.progress(score/100)

        st.write("### 📚 Recommended Study Plan")
        for r in recs:
            st.write("✔", r)

        # tips
        if level == "Beginner":
            st.info("Tip: Focus on understanding concepts slowly.")
        elif level == "Intermediate":
            st.info("Tip: Practice regularly to improve.")
        else:
            st.info("Tip: Challenge yourself with advanced problems.")

   
