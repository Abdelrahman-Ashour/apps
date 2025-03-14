import streamlit as st
import pandas as pd
import numpy as np
import random
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier

# واجهة المستخدم في Streamlit
st.set_page_config(page_title="Startup Idea Finder", layout="wide")

st.title("🚀 Startup Idea Finder")
st.write("Find the best startup idea based on your skills, budget, and market competition.")

# رفع الملف عبر Streamlit
uploaded_file = st.file_uploader("📂 Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    # قراءة البيانات من الملف المرفوع
    df = pd.read_csv(uploaded_file)

    # التحقق من البيانات
    st.write("✅ File uploaded successfully! Here is a preview:")
    st.write(df.head())  # عرض أول 5 صفوف

    # تحويل القيم النصية إلى أرقام باستخدام LabelEncoder
    le_field = LabelEncoder()
    le_competition = LabelEncoder()
    le_skills = LabelEncoder()

    df["Field_Encoded"] = le_field.fit_transform(df["المجال"])
    df["Competition_Encoded"] = le_competition.fit_transform(df["درجة التنافسية"])
    df["Skills_Encoded"] = le_skills.fit_transform(df["المهارات المطلوبة"])

    # تدريب نموذج التصنيف
    X = df[["Field_Encoded", "الميزانية المطلوبة", "Competition_Encoded", "Skills_Encoded"]]
    y = df["نجاح المشروع"]
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)

    # إدخال البيانات من المستخدم
    st.sidebar.header("🔍 Input Your Preferences")
    field = st.sidebar.selectbox("Select Industry", df["المجال"].unique())
    budget = st.sidebar.slider("Select Your Budget (in 1000s)", min_value=10, max_value=500, step=10, value=100)
    competition = st.sidebar.selectbox("Market Competition", df["درجة التنافسية"].unique())
    skills = st.sidebar.selectbox("Your Key Skill", df["المهارات المطلوبة"].unique())

    # ترميز المدخلات
    input_data = np.array([[le_field.transform([field])[0], budget,
                            le_competition.transform([competition])[0],
                            le_skills.transform([skills])[0]]])

    # التنبؤ بنجاح المشروع
    prediction = model.predict(input_data)[0]
    success_probability = random.randint(50, 95)  # احتمالية نجاح عشوائية

    # عرض النتائج
    st.subheader("📊 Suggested Startup Idea")
    st.metric(label="Industry", value=field)
    st.metric(label="Estimated Success Rate", value=f"{success_probability}%")
    st.write(f"💡 Recommended Industry: **{field}**")
    st.write(f"💰 Recommended Budget: **{budget}K**")
    st.write(f"🏆 Market Competition: **{competition}**")
    st.write(f"🛠 Key Skill Required: **{skills}**")

    if prediction == 1:
        st.success("✅ This project has a high potential for success!")
    else:
        st.warning("⚠️ This project may face challenges. Consider refining your idea.")

    # شريط التقدم
    st.progress(success_probability / 100)

    # رسالة ختامية
    st.write("🔹 Adjust your inputs in the sidebar to explore different startup ideas!")

else:
    st.warning("⚠️ Please upload a CSV file to proceed.")
