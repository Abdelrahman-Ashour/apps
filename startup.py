import streamlit as st
import numpy as np
import pandas as pd
import random
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
import joblib

# -------------------- إعداد الصفحة --------------------
st.set_page_config(page_title="🤖 IDEA.AI", layout="wide")
st.title("🤖 IDEA.AI")
st.write("ابحث عن أفضل فكرة لمشروع ناشئ بناءً على مهاراتك، ميزانيتك، وتفاصيل السوق.")

# -------------------- البيانات المحدثة --------------------
main_industries = {
    "تكنولوجيا": ["برمجيات", "ذكاء صناعي", "أمن سيبراني"],
    "زراعة": ["زراعة عضوية", "تكنولوجيا زراعية"],
    "تعليم": ["منصات تعليمية", "دروس خصوصية"],
    "صحة": ["تطبيقات طبية", "مكملات غذائية"],
    "تصنيع": ["تصنيع غذائي", "طباعة ثلاثية الأبعاد"]
}

competition_levels = ["منخفضة", "متوسطة", "عالية"]
skills_required = ["برمجة", "إدارة أعمال", "تسويق", "هندسة", "تحليل بيانات", "تصميم جرافيك", "ذكاء صناعي"]

# -------------------- إنشاء بيانات أكبر --------------------
num_records = 1500
industries_list = []
detail_list = []

for _ in range(num_records):
    field = random.choice(list(main_industries.keys()))
    detail = random.choice(main_industries[field])
    industries_list.append(field)
    detail_list.append(detail)

budgets_list = np.random.randint(100, 5000, size=num_records).tolist()
competition_list = np.random.choice(competition_levels, size=num_records).tolist()
skills_list = np.random.choice(skills_required, size=num_records).tolist()
success_list = np.random.choice([0, 1], size=num_records, p=[0.4, 0.6]).tolist()

data = pd.DataFrame({
    "المجال": industries_list,
    "التفصيل": detail_list,
    "الميزانية المطلوبة": budgets_list,
    "درجة التنافسية": competition_list,
    "المهارات المطلوبة": skills_list,
    "نجاح المشروع": success_list
})

# -------------------- الترميز والتدريب --------------------
le_field = LabelEncoder()
le_detail = LabelEncoder()
le_competition = LabelEncoder()
le_skills = LabelEncoder()

data["Field_Encoded"] = le_field.fit_transform(data["المجال"])
data["Detail_Encoded"] = le_detail.fit_transform(data["التفصيل"])
data["Competition_Encoded"] = le_competition.fit_transform(data["درجة التنافسية"])
data["Skills_Encoded"] = le_skills.fit_transform(data["المهارات المطلوبة"])

X = data[["Field_Encoded", "Detail_Encoded", "الميزانية المطلوبة", "Competition_Encoded", "Skills_Encoded"]]
y = data["نجاح المشروع"]
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# -------------------- واجهة المستخدم --------------------
st.sidebar.header("🔍 أدخل تفضيلاتك")
field = st.sidebar.selectbox("اختر المجال الرئيسي", list(main_industries.keys()))
detail = st.sidebar.selectbox("اختر التفصيل الفرعي", main_industries[field])
budget = st.sidebar.slider("حدد الميزانية (بالآلاف)", min_value=10, max_value=500, step=10, value=100)
competition = st.sidebar.selectbox("مستوى التنافسية", competition_levels)
skills = st.sidebar.selectbox("مهارتك الأساسية", skills_required)

# -------------------- التنبؤ --------------------
input_data = np.array([[
    le_field.transform([field])[0],
    le_detail.transform([detail])[0],
    budget,
    le_competition.transform([competition])[0],
    le_skills.transform([skills])[0]
]])

prediction = model.predict(input_data)[0]
success_probability = round(model.predict_proba(input_data)[0][1] * 100)

# -------------------- عرض النتائج --------------------
st.subheader("📊 تفاصيل الفكرة المقترحة")
st.metric(label="المجال", value=field)
st.metric(label="الفرع", value=detail)
st.metric(label="نسبة النجاح المتوقعة", value=f"{success_probability}%")
st.write(f"💡 المجال: **{field}** → **{detail}**")
st.write(f"💰 الميزانية المقترحة: **{budget}K**")
st.write(f"🏆 مستوى التنافسية: **{competition}**")
st.write(f"🛠 المهارة المطلوبة: **{skills}**")

if prediction == 1:
    st.success("✅ هذا المشروع لديه فرصة كبيرة للنجاح!")
else:
    st.warning("⚠️ قد يواجه هذا المشروع تحديات، يُفضل إعادة النظر في الفكرة.")

st.progress(success_probability / 100)

if st.button("🎲 فكرة عشوائية"):
    rand_row = data.sample(1).iloc[0]
    st.info(f"جرب مشروع في مجال **{rand_row['المجال']}** → **{rand_row['التفصيل']}** بميزانية **{rand_row['الميزانية المطلوبة']}K**، تنافسية **{rand_row['درجة التنافسية']}**، باستخدام مهارة **{rand_row['المهارات المطلوبة']}**")

st.write("🔹 جرب تعديل المدخلات في الشريط الجانبي لاكتشاف أفكار مختلفة!")
