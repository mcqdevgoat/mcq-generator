import streamlit as st
import whisper
from googletrans import Translator

st.title("🎙️ বাংলা MCQ জেনারেটর")
st.write("সহজেই মুখে বলে এমসিকিউ তৈরি করুন।")

# মডেল লোড করা
@st.cache_resource
def load_model():
    return whisper.load_model("base")

model = load_model()
translator = Translator()

audio_file = st.audio_input("🎤 এখানে ক্লিক করে রেকর্ড করুন অথবা অডিও ফাইল আপলোড করুন")

if audio_file is not None:
    with st.spinner("আপনার কণ্ঠস্বর প্রসেস করা হচ্ছে এবং খাঁটি বাংলায় রূপান্তর করা হচ্ছে..."):
        with open("temp_audio.wav", "wb") as f:
            f.write(audio_file.getbuffer())
        
        # Whisper দিয়ে প্রথমে টেক্সট নেওয়া
        result = model.transcribe("temp_audio.wav", language="bn")
        raw_text = result['text'].strip()
        
        # যদি বাংলিশ বা ইংরেজি অক্ষরে আসে, সেটাকে খাঁটি বাংলা অক্ষরে কনভার্ট করার ট্রিক
        try:
            # গুগল ট্রান্সলেটরের সাহায্যে বাংলিশকে প্রপার বাংলা টেক্সটে রূপান্তর
            converted = translator.translate(raw_text, src='en', dest='bn')
            full_text = converted.text
        except:
            full_text = raw_text

        # সেফটি চেক: যদি কোনো কারণে 'Option' শব্দটা ইংরেজিতেই থেকে যায়
        full_text = full_text.replace("Option", "অপশন").replace("option", "অপশন")
        
        st.info(f"**আপনার কণ্ঠস্বর থেকে প্রাপ্ত টেক্সট:** {full_text}")
        
        if "অপশন" in full_text:
            parts = full_text.split("অপশন")
            question = parts[0].strip()
            options = parts[1:]
            
            st.subheader("📋 আপনার তৈরি হওয়া MCQ:")
            st.markdown(f"**প্রশ্ন:** {question}")
            
            prefixes = ["ক) ", "খ) ", "গ) ", "ঘ) ", "ঙ) "]
            for i, opt in enumerate(options):
                pfx = prefixes[i] if i < len(prefixes) else f"{i+1}) "
                st.write(f"{pfx} {opt.strip()}")
        else:
            st.warning("⚠️ টেক্সটের মধ্যে 'অপশন' শব্দটি খুঁজে পাওয়া যায়নি।")
            st.info("টিপস: কথা বলার সময় প্রতিটি অপশনের আগে স্পষ্ট করে 'অপশন' শব্দটি বলুন।")
