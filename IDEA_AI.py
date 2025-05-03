import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# إعداد الاتصال بـ Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

credentials = {
    "type": "service_account",
    "project_id": st.secrets["gcp_service_account"]["project_id"],
    "private_key_id": st.secrets["gcp_service_account"]["private_key_id"],
    "private_key": st.secrets["gcp_service_account"]["private_key"].replace("\\n", "\n"),
    "client_email": st.secrets["gcp_service_account"]["client_email"],
    "client_id": st.secrets["gcp_service_account"]["client_id"],
    "auth_uri": st.secrets["gcp_service_account"]["auth_uri"],
    "token_uri": st.secrets["gcp_service_account"]["token_uri"],
    "auth_provider_x509_cert_url": st.secrets["gcp_service_account"]["auth_provider_x509_cert_url"],
    "client_x509_cert_url": st.secrets["gcp_service_account"]["client_x509_cert_url"]
}

credentials_obj = ServiceAccountCredentials.from_json_keyfile_dict(credentials, scope)
client = gspread.authorize(credentials_obj)
sheet = client.open("startup-form").sheet1

# واجهة التطبيق
st.title("💡 Startup Idea Finder")

st.markdown("ساعدنا في اختيار فكرة المشروع الأنسب لك بناءً على مهاراتك وميزانيتك والمجال المستهدف:")

with st.form("idea_form"):
    name = st.text_input("👤 الاسم")
    skills = st.text_area("🛠️ المهارات (مثال: برمجة، تصميم، تسويق...)")
    budget = st.selectbox("💰 الميزانية المتاحة", ["أقل من 1000$", "1000$ - 5000$", "أكثر من 5000$"])
    field = st.text_input("🏷️ المجال المفضل (مثال: تكنولوجيا، زراعة، تعليم...)")
    competition = st.selectbox("📊 مستوى المنافسة في المجال", ["منخفضة", "متوسطة", "عالية"])

    submitted = st.form_submit_button("إرسال")

    if submitted:
        if not name.strip():
            st.warning("يرجى إدخال الاسم.")
        else:
            sheet.append_row([name, skills, budget, field, competition])
            st.success("✅ تم إرسال بياناتك بنجاح!")

            # تحليل مبدئي واقتراح فكرة
            idea = "🤔 لم نستطع تحديد فكرة مناسبة. حاول كتابة مهارات أو مجال مختلف."

            if "برمجة" in skills or "تطبيق" in field:
                if budget == "أقل من 1000$":
                    idea = "📱 تطوير تطبيق بسيط باستخدام Flutter أو Python Streamlit"
                elif budget == "1000$ - 5000$":
                    idea = "🧠 تطبيق ذكي يستخدم الذكاء الاصطناعي لحل مشكلة محلية"
                else:
                    idea = "🌐 منصة SaaS تخدم الشركات الصغيرة في مجال معين"

            elif "تصميم" in skills or "ملابس" in field:
                if competition == "منخفضة":
                    idea = "🧵 مشروع طباعة وتصميم تيشيرتات حسب الطلب على الإنترنت"
                else:
                    idea = "👕 متجر ملابس إلكتروني يستهدف جمهور متخصص (مثل: أطفال أو رياضيين)"

            elif "تسويق" in skills:
                idea = "📢 وكالة تسويق رقمي صغيرة تستهدف المشاريع المحلية"

            elif "زراعة" in field:
                idea = "🌱 زراعة عمودية أو مشروع إنتاج عضوي وتوزيعه إلكترونيًا"

            elif "تعليم" in field:
                idea = "📚 منصة تعليمية لمهارة معينة (مثال: تصميم، لغة، تطوير ذاتي)"

            st.markdown("### 🔍 اقتراح فكرة مشروع لك:")
            st.success(idea)
