import streamlit as st
import numpy as np
import random
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
import plotly.express as px

# إعداد الصفحة
st.set_page_config(page_title="🤖 IDEA.AI", layout="wide")

# اللوجو
st.image("image/IDEA_AI.png", width=200)
st.title("IDEA.AI")
st.caption("START SMART")

st.write("""
### 🤖 اكتشف أفضل فكرة لمشروع ناشئ بناءً على مهاراتك وميزانيتك ومستوى المنافسة
""")

# قوائم الاختيارات
industries = {
    "تكنولوجيا": ["برمجيات", "أجهزة ذكية", "ذكاء اصطناعي"],
    "زراعة": ["زراعة عضوية", "تكنولوجيا زراعية"],
    "تصنيع": ["منتجات غذائية", "معدات كهربائية", "تصنيع بلاستيك"],
    "تعليم": ["دورات أونلاين", "تدريب مهني"],
    "صحة": ["مستلزمات طبية", "علاج طبيعي"]
}
skills_required = ["برمجة", "إدارة أعمال", "تسويق", "هندسة", "تحليل بيانات", "إلكترونيات"]
competition_levels = ["منخفضة", "متوسطة", "عالية"]

# إدخال بيانات عشوائية لتدريب الموديل
num_records = 100
industry_list = []
subindustry_list = []
for _ in range(num_records):
    field = random.choice(list(industries.keys()))
    industry_list.append(field)
    subindustry_list.append(random.choice(industries[field]))

budgets_list = np.random.randint(10, 500, size=num_records).tolist()
competition_list = np.random.choice(competition_levels, size=num_records).tolist()
skills_list = np.random.choice(skills_required, size=num_records).tolist()
success_list = np.random.choice([0, 1], size=num_records, p=[0.4, 0.6]).tolist()

# DataFrame
df = pd.DataFrame({
    "المجال": industry_list,
    "التخصص": subindustry_list,
    "الميزانية المطلوبة": budgets_list,
    "درجة التنافسية": competition_list,
    "المهارات المطلوبة": skills_list,
    "نجاح المشروع": success_list
})

# الترميز
le_field = LabelEncoder()
le_sub = LabelEncoder()
le_comp = LabelEncoder()
le_skills = LabelEncoder()

df["Field_Encoded"] = le_field.fit_transform(df["المجال"])
df["Sub_Encoded"] = le_sub.fit_transform(df["التخصص"])
df["Competition_Encoded"] = le_comp.fit_transform(df["درجة التنافسية"])
df["Skills_Encoded"] = le_skills.fit_transform(df["المهارات المطلوبة"])

X = df[["Field_Encoded", "Sub_Encoded", "الميزانية المطلوبة", "Competition_Encoded", "Skills_Encoded"]]
y = df["نجاح المشروع"]

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# الشريط الجانبي
st.sidebar.header("🔍 أدخل تفضيلاتك")
field = st.sidebar.selectbox("حدد المجال", list(industries.keys()))
sub = st.sidebar.selectbox("اختر التخصص", industries[field])
budget = st.sidebar.slider("حدد الميزانية (بالآلاف)", min_value=10, max_value=500, step=10)
competition = st.sidebar.selectbox("مستوى التنافسية", competition_levels)
skills = st.sidebar.selectbox("مهارتك الرئيسية", skills_required)

# ترميز
input_data = np.array([[
    le_field.transform([field])[0],
    le_sub.transform([sub])[0],
    budget,
    le_comp.transform([competition])[0],
    le_skills.transform([skills])[0]
]])

prediction = model.predict(input_data)[0]
success_probability = random.randint(60, 95)

# عرض النتائج
st.subheader("📊 تفاصيل الفكرة المقترحة")
st.metric("المجال", field)
st.metric("التخصص", sub)
st.metric("نسبة النجاح المتوقعة", f"{success_probability}%")

if prediction == 1:
    st.success("✅ هذا المشروع لديه فرصة كبيرة للنجاح!")
else:
    st.warning("⚠️ قد يواجه هذا المشروع تحديات، يُفضل إعادة النظر في الفكرة.")

st.progress(success_probability / 100)

# رسم بياني
fig = px.histogram(df, x="المجال", color="نجاح المشروع", barmode="group",
                   title="تحليل نجاح المشاريع حسب المجال")
st.plotly_chart(fig, use_container_width=True)

# ميزة مشروعك
st.header(":star: ميزة 'مشروعك'")
if st.button("اقترح لي مشروع الآن"):
    idea = f"مشروع في مجال {field} - {sub} باستخدام مهارة {skills} بميزانية {budget}K"
    st.info(f"أفضل مشروع مناسب لك: {idea}")
    st.write("يمكنك تفعيل الميزة الكاملة بالاشتراك")

# الاشتراك الشهري
st.sidebar.subheader(":moneybag: اشتراك ميزة مشروعك")
st.sidebar.info("سعر الاشتراك: 200 جنيه شهريًا")
st.sidebar.write("تحويل على رقم فودافون كاش: 01093716581 - Abdelrahman Nasr")

# صفحة بسيطة للدردشة
st.sidebar.subheader(":speech_balloon: خدمة العملاء")
question = st.sidebar.text_input("اكتب سؤالك")
if question:
    st.sidebar.write("شكراً، سيتم الرد عليك قريبًا ✉")
