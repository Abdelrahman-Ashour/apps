import streamlit as st
import numpy as np
import random
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier

# إعداد الصفحة
st.set_page_config(page_title="🤖 IDEA.AI", layout="wide")

st.title("🤖 IDEA.AI")
st.write("إبحث عن أفضل فكرة لمشروع ناشئ بناءً على مهاراتك وميزانيتك ومستوى المنافسة.")

# إدخال البيانات يدويًا لتجنب الأخطاء
industries = ["تكنولوجيا", "زراعة", "تعليم", "صحة", "تصنيع"]
competition_levels = ["منخفضة", "متوسطة", "عالية"]
skills_required = ["برمجة", "إدارة أعمال", "تسويق", "هندسة"]

# عدد السجلات المطلوبة
num_records = 50

# إنشاء البيانات مع التأكد من تساوي الطول
industries_list = np.random.choice(industries, size=num_records).tolist()
budgets_list = np.random.randint(10, 500, size=num_records).tolist()
competition_list = np.random.choice(competition_levels, size=num_records).tolist()
skills_list = np.random.choice(skills_required, size=num_records).tolist()
success_list = np.random.choice([0, 1], size=num_records, p=[0.4, 0.6]).tolist()

# إنشاء DataFrame
data = {
    "المجال": industries_list,
    "الميزانية المطلوبة": budgets_list,
    "درجة التنافسية": competition_list,
    "المهارات المطلوبة": skills_list,
    "نجاح المشروع": success_list
}
df = pd.DataFrame(data)

# ترميز البيانات
le_field = LabelEncoder()
le_competition = LabelEncoder()
le_skills = LabelEncoder()

df["Field_Encoded"] = le_field.fit_transform(df["المجال"])
df["Competition_Encoded"] = le_competition.fit_transform(df["درجة التنافسية"])
df["Skills_Encoded"] = le_skills.fit_transform(df["المهارات المطلوبة"])

# تدريب النموذج
X = df[["Field_Encoded", "الميزانية المطلوبة", "Competition_Encoded", "Skills_Encoded"]]
y = df["نجاح المشروع"]
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# واجهة المستخدم
st.sidebar.header("🔍 أدخل تفضيلاتك")
field = st.sidebar.selectbox("حدد المجال", industries)
budget = st.sidebar.slider("حدد الميزانية (بالآلاف)", min_value=10, max_value=500, step=10, value=100)
competition = st.sidebar.selectbox("مستوى التنافسية", competition_levels)
skills = st.sidebar.selectbox("مهارتك الرئيسية", skills_required)

# ترميز المدخلات
input_data = np.array([[
    le_field.transform([field])[0],
    budget,
    le_competition.transform([competition])[0],
    le_skills.transform([skills])[0]
]])

# التنبؤ بنجاح المشروع
prediction = model.predict(input_data)[0]
success_probability = random.randint(50, 95)  # نسبة نجاح عشوائية

# عرض النتائج
st.subheader("📊 تفاصيل الفكرة المقترحة")
st.metric(label="المجال", value=field)
st.metric(label="نسبة النجاح المتوقعة", value=f"{success_probability}%")
st.write(f"💡 المجال: **{field}**")
st.write(f"💰 الميزانية المقترحة: **{budget}K**")
st.write(f"🏆 مستوى التنافسية: **{competition}**")
st.write(f"🛠 المهارة المطلوبة: **{skills}**")

if prediction == 1:
    st.success("✅ هذا المشروع لديه فرصة كبيرة للنجاح!")
else:
    st.warning("⚠️ قد يواجه هذا المشروع تحديات، يُفضل إعادة النظر في الفكرة.")

# شريط التقدم
st.progress(success_probability / 100)

st.write("🔹 جرب تعديل المدخلات في الشريط الجانبي لاكتشاف أفكار مختلفة!")

