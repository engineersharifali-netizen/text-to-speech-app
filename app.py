import streamlit as st
from google import genai
from google.genai import types
import os

# تنظیمات صفحه وب
st.set_page_config(page_title="ابزار تبدیل متن به صوت اختصاصی", page_icon="🎙️")

st.title("🎙️ تبدیل دقیق متن به فایل صوتی اختصاصی")
st.write("متن خود را وارد کنید تا دقیقاً همان متن به صوت تبدیل شود.")

# مسیر فایل صدای پیش‌فرض
VOICE_FILE_PATH = "my_voice.mp3"

if not os.path.exists(VOICE_FILE_PATH):
    st.error(f"⚠️ فایل صدای پیش‌فرض '{VOICE_FILE_PATH}' پیدا نشد! لطفاً آن را در پوشه پروژه قرار دهید.")

# انتخاب زبان خروجی
language = st.selectbox(
    "انتخاب زبان خروجی:",
    ["فارسی (Persian)", "English (انگلیسی)", "Arabic (عربی)"]
)

# کادر دریافت متن
input_text = st.text_area(
    "متن خود را برای تبدیل دقیق به صوت اینجا وارد کنید:",
    placeholder="متن خود را اینجا بنویسید..."
)

# دکمه پردازش
if st.button("تولید فایل صوتی 🚀"):
    if not input_text.strip():
        st.warning("⚠️ لطفاً ابتدا متنی را در کادر وارد کنید.")
    elif not os.path.exists(VOICE_FILE_PATH):
        st.error("❌ فایل صوتی پیش‌فرض موجود نیست.")
    else:
        with st.spinner("در حال پردازش و تبدیل دقیق متن به صوت..."):
            try:
                # خواندن امن کلید API از تنظیمات Secrets استریم‌لیت
                API_KEY = st.secrets["GEMINI_API_KEY"]
                client = genai.Client(api_key=API_KEY)

                # آپلود فایل صوتی مرجع به عنوان پرامپت کمکی
                voice_ref_file = client.files.upload(file=VOICE_FILE_PATH)

                # تنظیم درخواست برای تولید دقیق فایل صوتی با صدای مرجع
                prompt = (
                    f"Read the following text aloud word-for-word in {language}, using the exact voice persona "
                    f"and tone provided in the reference audio file. Do not add any introductory or concluding text, "
                    f"just output the spoken audio for the text: {input_text}"
                )

                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=[voice_ref_file, prompt],
                    config=types.GenerateContentConfig(
                        response_mime_type="audio/mp3"
                    )
                )
                
                st.success("✅ فایل صوتی شما با موفقیت تولید شد!")
                
                # ذخیره و نمایش فایل صوتی خروجی
                output_filename = "output_audio.mp3"
                
                # ذخیره بایت‌های صوتی دریافتی از مدل
                with open(output_filename, "wb") as f:
                    f.write(response.candidates[0].content.parts[0].inline_data.data)

                # نمایش موزیک پلیر در صفحه
                st.audio(output_filename, format="audio/mp3")
                
                # دکمه دانلود مستقیم
                with open(output_filename, "rb") as file:
                    st.download_button(
                        label="📥 دانلود فایل صوتی نهایی",
                        data=file,
                        file_name="final_voice.mp3",
                        mime="audio/mp3"
                    )

            except Exception as e:
                st.error(f"خطایی رخ داد (اگر خطای 503 بود لطفاً چند لحظه دیگر دوباره تلاش کنید): {e}")
