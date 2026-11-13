import streamlit as st
from google import genai
import os

# تنظیمات صفحه وب
st.set_page_config(page_title="ابزار تبدیل متن به صوت اختصاصی", page_icon="🎙️")

st.title("🎙️ تبدیل دقیق متن به فایل صوتی اختصاصی")
st.write("متن خود را وارد کنید تا فایل صوتی با صدای مرجع شما تولید شود.")

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
    "متن خود را برای تبدیل به صوت اینجا وارد کنید:",
    placeholder="متن خود را اینجا بنویسید..."
)

# دکمه پردازش
if st.button("تولید فایل صوتی 🚀"):
    if not input_text.strip():
        st.warning("⚠️ لطفاً ابتدا متنی را در کادر وارد کنید.")
    elif not os.path.exists(VOICE_FILE_PATH):
        st.error("❌ فایل صوتی پیش‌فرض موجود نیست.")
    else:
        with st.spinner("در حال پردازش و تولید فایل صوتی..."):
            try:
                # خواندن امن کلید API از تنظیمات Secrets استریم‌لیت
                API_KEY = st.secrets["GEMINI_API_KEY"]
                client = genai.Client(api_key=API_KEY)

                # آپلود فایل صوتی مرجع
                voice_ref_file = client.files.upload(file=VOICE_FILE_PATH)

                # ارسال درخواست متنی و مرجع صوتی به مدل
                prompt = (
                    f"Convert the following text into spoken audio in {language}, strictly using the exact voice persona "
                    f"from the reference audio file. Read only the provided text and output the speech response: {input_text}"
                )

                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=[voice_ref_file, prompt]
                )
                
                st.success("✅ پاسخ هوش مصنوعی دریافت شد!")
                
                # بررسی و نمایش خروجی
                if response.candidates and response.candidates[0].content.parts:
                    # بررسی وجود داده صوتی در خروجی مدل
                    part = response.candidates[0].content.parts[0]
                    
                    if hasattr(part, 'inline_data') and part.inline_data:
                        output_filename = "output_audio.mp3"
                        with open(output_filename, "wb") as f:
                            f.write(part.inline_data.data)

                        st.audio(output_filename, format="audio/mp3")
                        
                        with open(output_filename, "rb") as file:
                            st.download_button(
                                label="📥 دانلود فایل صوتی نهایی",
                                data=file,
                                file_name="final_voice.mp3",
                                mime="audio/mp3"
                            )
                    else:
                        # اگر خروجی متنی بود، متن را نمایش می‌دهیم
                        st.write("پاسخ متنی مدل:")
                        st.write(response.text)
                else:
                    st.warning("پاسخی از مدل دریافت نشد.")

            except Exception as e:
                st.error(f"خطایی رخ داد (اگر خطای 503 بود لطفاً دوباره تلاش کنید): {e}")
