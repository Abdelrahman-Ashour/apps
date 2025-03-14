import streamlit as st
import numpy as np
import random
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier

# إعداد الصفحة بتصميم مناسب
st.set_page_config(page_title="Startup Idea Finder", layout="wide")

st.markdown(
    """
    <style>
    .main {
        background-color: #f4f4f4;
        padding: 20px;
        border-radius: 10px;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-size: 16px;
        border-radius: 8px;
        width: 100%;
    }
    .stMetric {
        font-size: 20px;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🚀 Startup Idea Finder")
st.write("حدد تفاصيل مشروعك الناشئ لتحصل على تحليل لنسبة نجاحه!")

# إدخال البيانات يدويًا
st.sidebar.header("🔍 أدخل بيانات المشروع")

industries = ["التكنولوجيا", "التجارة الإلكترونية", "الصحة", "التعليم", "الطاقة المتجددة"]
competition_levels = ["منخفض", "متوسط", "مرتفع"]
skills_required = ["برمجة", "تسويق", "إدارة", "تحليل بيانات", "تمويل"]

field = st.sidebar.selectbox("اختر المجال", industries)
budget = st.sidebar.slider("حدد الميزانية المطلوبة (بالألف)", min_value=10, max_value=500, step=10, value=100)
competition = st.sidebar.selectbox("مستوى التنافسية", competition_levels)
skills = st.sidebar.selectbox("المهارة الأساسية المطلوبة", skills_required)

# تحويل البيانات إلى أرقام
le_field = LabelEncoder()
le_competition = LabelEncoder()
le_skills = LabelEncoder()

field_encoded = le_field.fit_transform([field])[0]
competition_encoded = le_competition.fit_transform([competition])[0]
skills_encoded = le_skills.fit_transform([skills])[0]

# إنشاء بيانات تدريب بسيطة
data = {
    "المجال": industries * 10,
    "الميزانية المطلوبة": np.random.randint(10, 500, size=50),
    "درجة التنافسية": competition_levels * 10,
    "المهارات المطلوبة": skills_required * 10,
    "نجاح المشروع": np.random.choice([0, 1], size=50, p=[0.4, 0.6])
}
df = pd.DataFrame(data)

df["Field_Encoded"] = le_field.fit_transform(df["المجال"])
df["Competition_Encoded"] = le_competition.fit_transform(df["درجة التنافسية"])
df["Skills_Encoded"] = le_skills.fit_transform(df["المهارات المطلوبة"])

# تدريب النموذج
X = df[["Field_Encoded", "الميزانية المطلوبة", "Competition_Encoded", "Skills_Encoded"]]
y = df["نجاح المشروع"]
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# توقع نسبة النجاح
input_data = np.array([[field_encoded, budget, competition_encoded, skills_encoded]])
prediction = model.predict(input_data)[0]
success_probability = random.randint(50, 95)

# عرض النتائج
st.subheader("📊 تحليل المشروع")
col1, col2, col3 = st.columns(3)
col1.metric(label="المجال", value=field)
col2.metric(label="نسبة النجاح", value=f"{success_probability}%")
col3.metric(label="التنافسية", value=competition)

st.write(f"💡 **مجالك المختار:** {field}")
st.write(f"💰 **الميزانية المقترحة:** {budget} ألف")
st.write(f"🏆 **مستوى التنافسية:** {competition}")
st.write(f"🛠 **المهارة الأساسية:** {skills}")

# رسم بياني دائري لنسبة النجاح
fig, ax = plt.subplots()
ax.pie([success_probability, 100 - success_probability], labels=["نجاح", "فشل"], autopct='%1.1f%%', colors=["#4CAF50", "#FF5733"])
st.pyplot(fig)

if prediction == 1:
    st.success("✅ هذا المشروع لديه فرصة جيدة للنجاح!")
else:
    st.warning("⚠️ قد يواجه المشروع تحديات، حاول تحسين الفكرة.")

st.progress(success_probability / 100)
st.write("🔹 قم بتغيير الإعدادات في القائمة الجانبية لاستكشاف أفكار جديدة!")
