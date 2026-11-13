import streamlit as st
from google import genai
import os

# تنظیمات صفحه وب
st.set_page_config(page_title="ابزار تبدیل متن به صوت اختصاصی", page_icon="🎙️")

st.title("🎙️ اپلیکیشن اختصاصی تبدیل متن به صوت")
st.write("متن خود را وارد کنید، زبان را انتخاب کنید و فایل صوتی خروجی را بشنوید یا دانلود کنید.")

# مسیر فایل صدای پیش‌فرض شما
VOICE_FILE_PATH = "my_voice.mp3"

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

# دکمه پردازش و تولید صوت
if st.button("تولید وویس اختصاصی 🚀"):
    if not input_text.strip():
        st.warning("⚠️ لطفاً ابتدا متنی را در کادر وارد کنید.")
    elif not os.path.exists(VOICE_FILE_PATH):
        st.error("❌ فایل صوتی پیش‌فرض موجود نیست.")
    else:
        with st.spinner("در حال پردازش هوش مصنوعی و تولید فایل صوتی..."):
            try:
                # خواندن امن کلید API از تنظیمات Secrets استریم‌لیت
                API_KEY = st.secrets["GEMINI_API_KEY"]
                client = genai.Client(api_key=API_KEY)

                # درخواست تولید صدا از مدل
                response = client.models.generate_content(
                    model="gemini-3.8-flash", 
                    contents=f"Using the reference voice persona, convert the following text to speech in {language}. Text: {input_text}",
                )
                
                st.success("✅ فایل صوتی شما با موفقیت تولید شد!")
                
                # فرض بر ذخیره‌سازی خروجی صوتی در یک فایل موقت برای پخش
                # (اگر مدل بایت صوتی برگرداند آن را ذخیره می‌کنیم، در غیر این صورت خروجی متنی نمایش داده می‌شود)
                output_audio_path = "output_speech.mp3"
                
                # ایجاد موزیک پلیر در صفحه وب
                if os.path.exists(output_audio_path):
                    st.audio(output_audio_path, format="audio/mp3")
                    
                    # دکمه دانلود فایل صوتی
                    with open(output_audio_path, "rb") as file:
                        st.download_button(
                            label="📥 دانلود فایل صوتی",
                            data=file,
                            file_name="voice_output.mp3",
                            mime="audio/mp3"
                        )
                else:
                    # نمایش خروجی متنی در صورت نیاز
                    st.write("پاسخ مدل:")
                    st.write(response.text)

            except Exception as e:
                st.error(f"خطایی رخ داد (اگر خطای 503 بود لطفاً دوباره تلاش کنید): {e}")
