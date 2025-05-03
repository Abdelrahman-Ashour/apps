import streamlit as st
import openai
import os
import json

# تحميل مفتاح API من secrets
service_account_info = st.secrets["gcp_service_account"]
openai.api_key = st.secrets["OPENAI_API_KEY"]

# إعداد واجهة التطبيق
st.set_page_config(page_title="💡 فكرة مشروعك", page_icon="🚀", layout="centered")

st.title("🚀 فكرة مشروعك")
st.caption("باستخدام الذكاء الاصطناعي")

# إنشاء التبويبات
tab1, tab2 = st.tabs(["💡 اقتراح مشروع", "🛎️ خدمة العملاء"])

# ✅ تبويب 1: اقتراح مشروع
with tab1:
    st.header("💡 أدخل بياناتك وسنقترح لك مشروعًا مناسبًا")

    skills = st.text_input("🧠 مهاراتك (مفصولة بفواصل)", placeholder="مثال: برمجة، تصميم، تسويق")
    budget = st.slider("💰 الميزانية المتاحة (بالدولار)", 100, 100000, step=500)
    competition = st.selectbox("📊 درجة المنافسة في السوق", ["منخفضة", "متوسطة", "مرتفعة"])

    if st.button("⚡ احصل على فكرة مشروع"):
        if not skills.strip():
            st.warning("يرجى إدخال مهاراتك أولاً.")
        else:
            with st.spinner("يتم توليد فكرة مشروع مخصصة لك..."):
                try:
                    prompt = f"""
اقترح فكرة مشروع ريادي مناسبة بناءً على المعطيات التالية:
- المهارات: {skills}
- الميزانية: {budget} دولار
- درجة المنافسة: {competition}

قدم الفكرة باحترافية، تتضمن:
1. اسم المشروع
2. وصف مختصر للفكرة
3. متطلبات التنفيذ
4. طرق التسويق
5. احتمالات النجاح
                """

                    response = openai.ChatCompletion.create(
                        model="gpt-4",
                        messages=[
                            {"role": "system", "content": "أنت خبير في ريادة الأعمال."},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.7,
                        max_tokens=600
                    )

                    idea = response.choices[0].message["content"].strip()
                    st.success("🎯 فكرة المشروع المقترحة:")
                    st.markdown(idea)

                except Exception as e:
                    st.error(f"حدث خطأ أثناء الاتصال بـ OpenAI: {e}")

# ✅ تبويب 2: خدمة العملاء الذكية
with tab2:
    st.header("🛎️ خدمة العملاء الذكية")
    st.write("📬 اكتب سؤالك وسنقوم بالرد عليك فورًا:")

    user_question = st.text_area("✉️ سؤالك:")

    if st.button("📩 إرسال السؤال"):
        if user_question.strip() == "":
            st.warning("يرجى كتابة سؤال أولًا.")
        else:
            with st.spinner("يتم تجهيز الرد..."):
                try:
                    response = openai.ChatCompletion.create(
                        model="gpt-4",
                        messages=[
                            {"role": "system", "content": "أنت موظف خدمة عملاء محترف، أجب باحترافية وبلغة عربية واضحة ومبسطة."},
                            {"role": "user", "content": user_question}
                        ],
                        temperature=0.7,
                        max_tokens=300
                    )
                    answer = response.choices[0].message["content"].strip()
                    st.success("🗨️ الرد:")
                    st.markdown(answer)
                except Exception as e:
                    st.error(f"حدث خطأ في الاتصال بـ OpenAI: {e}")
