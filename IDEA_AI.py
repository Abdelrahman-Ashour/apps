import streamlit as st
import openai

# إعداد API من secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# تبويب الصفحة الرئيسي
st.set_page_config(page_title="IdeaAI", page_icon="🤖", layout="centered")

# القائمة الجانبية
st.sidebar.title("📂 قائمة الصفحات")
page = st.sidebar.radio("اذهب إلى:", ["الرئيسية", "خدمة العملاء"])

# الصفحة الرئيسية
if page == "الرئيسية":
    st.title("🎯 مرحبًا بك في IdeaAI")
    st.write("مرحبًا بك في منصة اختيار أفكار المشاريع باستخدام الذكاء الاصطناعي.")

# صفحة خدمة العملاء
elif page == "خدمة العملاء":
    st.title("📞 خدمة العملاء")
    st.write("يرجى كتابة سؤالك وسنقوم بالرد عليك فورًا:")

    user_question = st.text_area("✍️ اكتب سؤالك هنا")

    if st.button("📤 إرسال"):
        if user_question.strip() == "":
            st.warning("⚠️ يرجى كتابة سؤال قبل الإرسال.")
        else:
            with st.spinner("⏳ جاري إرسال سؤالك إلى خدمة العملاء..."):
                try:
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",  # استخدم gpt-4 لو متاح
                        messages=[
                            {"role": "system", "content": "أنت موظف خدمة عملاء محترف. أجب باحترافية وبأسلوب مبسط."},
                            {"role": "user", "content": user_question}
                        ]
                    )
                    answer = response.choices[0].message.content
                    st.success("✅ تم الرد:")
                    st.markdown(answer)
                except Exception as e:
                    st.error(f"❌ حدث خطأ أثناء الاتصال بـ OpenAI API:\n{e}")
