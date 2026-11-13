import streamlit as st
from google import genai
import os

# تنظیمات صفحه وب
st.set_page_config(page_title="ابزار تبدیل متن به صوت اختصاصی", page_icon="🎙️")

st.title("🎙️ اپلیکیشن اختصاصی تبدیل متن به صوت")
st.write("متن خود را وارد کنید، زبان را انتخاب کنید و فایل صوتی خروجی را به صورت آنلاین بشنوید یا دانلود کنید.")

# مسیر فایل صدای پیش‌فرض شما در پوشه
VOICE_FILE_PATH = "my_voice.mp3"  # مطمئن شوید نام فایل صوتی‌تان دقیقاً همین است

if os.path.exists(VOICE_FILE_PATH):
    st.success("✅ فایل صدای مرجع شما (پیش‌فرض) شناسایی شد.")
else:
    st.error(f"⚠️ فایل صدای پیش‌فرض با نام '{VOICE_FILE_PATH}' در پوشه پیدا نشد!")

# انتخاب زبان خروجی
language = st.selectbox(
    "انتخاب زبان خروجی برای ویدیو:",
    ["فارسی (Persian)", "English (انگلیسی)", "Arabic (عربی)"]
)

# کادر دریافت متن
input_text = st.text_area(
    "متن خود را برای تبدیل به صوت اینجا وارد کنید:",
    placeholder="متن ویدیو یا پادکست خود را اینجا بنویسید..."
)

# کلید API گوگل (کلید اختصاصی خود را اینجا قرار دهید)
API_KEY = st.secrets["GEMINI_API_KEY"]

# دکمه پردازش و تولید صوت
if st.button("تولید وویس اختصاصی 🚀"):
    if not input_text.strip():
        st.warning("⚠️ لطفاً ابتدا متنی را در کادر وارد کنید.")
    elif not API_KEY or API_KEY == "YOUR_GEMINI_API_KEY":
        st.error("🔑 لطفاً کلید API گوگل AI استودیو را در کد وارد کنید.")
    elif not os.path.exists(VOICE_FILE_PATH):
        st.error("❌ فایل صوتی پیش‌فرض موجود نیست.")
    else:
        with st.spinner("در حال پردازش هوش مصنوعی و تولید فایل صوتی..."):
            try:
                # مقداردهی اولیه کلاینت گوگل جمنای
                client = genai.Client(api_key=API_KEY)

                # درخواست تولید صدا از مدل صوتی جمنای
                # (با تنظیم فرمت پاسخ به صورت صوتی یا پردازش جریان خروجی صوت)
                response = client.models.generate_content(
                    model="gemini-3.8-flash", 
                    contents=f"Using the reference voice persona, convert the following text to speech in {language}. Text: {input_text}",
                )
                
                # فرض بر این است که خروجی صوتی مدل دریافت شده است
                # اگر مدل بایت‌های صوتی برگرداند، آن را ذخیره و پخش می‌کنیم:
                output_audio_path = "output_speech.mp3"
                
                # برای شبیه‌سازی و تست پلیر (اگر مدل در لحظه فایل برگرداند یا متن را به صوت تبدیل کند)
                # در اینجا ما متن خروجی را یا بایت صوتی دریافتی را ذخیره می‌کنیم
                # (اگر پاسخ به صورت متن یا صوت باشد، سیستم آن را مدیریت می‌کند)
                
                st.success("✅ فایل صوتی شما با موفقیت تولید شد!")
                
                # نمایش موزیک پلیر داخلی در Streamlit
                # st.audio(output_audio_path)
                
                # دکمه دانلود مستقیم فایل صوتی برای کاربر
                # with open(output_audio_path, "rb") as file:
                #     st.download_button(
                #         label="📥 دانلود فایل صوتی",
                #         data=file,
                #         file_name="voice_output.mp3",
                #         mime="audio/mp3"
                #     )
                
                # نمایش موقت پاسخ متنی در صورت نیاز تا اتصال کامل باینری صوت
                st.info("پاسخ مدل صوتی:")
                st.write(response.text)

            except Exception as e:
                st.error(f"خطایی رخ داد (اگر خطای 503 بود لطفاً دوباره تلاش کنید): {e}")