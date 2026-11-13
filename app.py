import streamlit as st
from google import genai
import os

st.set_page_config(page_title="ابزار تبدیل متن به صوت اختصاصی", page_icon="🎙️")

st.title("🎙️ تبدیل دقیق متن به فایل صوتی اختصاصی")
st.write("متن خود را وارد کنید تا مستقیماً فایل صوتی تحویل بگیرید.")

VOICE_FILE_PATH = "my_voice.mp3"

if not os.path.exists(VOICE_FILE_PATH):
    st.error(f"⚠️ فایل صدای پیش‌فرض '{VOICE_FILE_PATH}' پیدا نشد!")

language = st.selectbox(
    "انتخاب زبان خروجی:",
    ["فارسی (Persian)", "English (انگلیسی)", "Arabic (عربی)"]
)

input_text = st.text_area(
    "متن خود را برای تبدیل به صوت اینجا وارد کنید:",
    placeholder="متن خود را اینجا بنویسید..."
)

if st.button("تولید فایل صوتی 🚀"):
    if not input_text.strip():
        st.warning("⚠️ لطفاً ابتدا متنی را در کادر وارد کنید.")
    elif not os.path.exists(VOICE_FILE_PATH):
        st.error("❌ فایل صوتی پیش‌فرض موجود نیست.")
    else:
        with st.spinner("در حال پردازش و تولید فایل صوتی..."):
            try:
                API_KEY = st.secrets["GEMINI_API_KEY"]
                client = genai.Client(api_key=API_KEY)

                # بارگذاری فایل صوتی مرجع
                voice_ref = client.files.upload(file=VOICE_FILE_PATH)

                # درخواست تولید صوت با مدل
                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=[
                        voice_ref,
                        f"Convert this text to speech in {language}, using the voice persona from the reference file. Read only this text: {input_text}"
                    ]
                )
                
                # استخراج خروجی صوتی باینری
                audio_bytes = None
                if response.candidates and response.candidates[0].content.parts:
                    for part in response.candidates[0].content.parts:
                        if hasattr(part, 'inline_data') and part.inline_data:
                            audio_bytes = part.inline_data.data
                            break

                if audio_bytes:
                    output_filename = "output_audio.mp3"
                    with open(output_filename, "wb") as f:
                        f.write(audio_bytes)

                    st.success("✅ فایل صوتی با موفقیت تولید شد!")
                    st.audio(output_filename, format="audio/mp3")
                    
                    with open(output_filename, "rb") as file:
                        st.download_button(
                            label="📥 دانلود فایل صوتی نهایی",
                            data=file,
                            file_name="final_voice.mp3",
                            mime="audio/mp3"
                        )
                else:
                    st.error("❌ مدل به جای فایل صوتی، پاسخ متنی بازگرداند. لطفاً دوباره تلاش کنید.")
                    if hasattr(response, 'text'):
                        st.write(response.text)

            except Exception as e:
                st.error(f"خطا: {e}")
