import streamlit as st
import whisper

st.title("🎙️ বাংলা MCQ জেনারেটর")
st.write("सहजেই মুখে বলে এমসিকিউ তৈরি করুন।")

# হালকা মডেল লোড করা
@st.cache_resource
def load_model():
    return whisper.load_model("tiny")

model = load_model()

# অডিও ইনপুট নেওয়ার অপশন
audio_file = st.audio_input("🎤 এখানে ক্লিক করে রেকর্ড করুন অথবা অডিও ফাইল আপলোড করুন")

if audio_file is not None:
    with st.spinner("আপনার কণ্ঠস্বর প্রসেস করা হচ্ছে..."):
        # অডিও ফাইলটি সাময়িকভাবে সেভ করা
        with open("temp_audio.wav", "wb") as f:
            f.write(audio_file.getbuffer())
        
        # Whisper দিয়ে বাংলায় রূপান্তর
        result = model.transcribe("temp_audio.wav", language="bn")
        full_text = result['text'].strip()
        
        # ক, খ, গ, ঘ অপশনে ভাগ করার লজিক
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
            st.warning("⚠️ আপনি অপশনগুলো আলাদা করতে 'অপশন' শব্দটি বলেননি।")
            st.write(f"**আপনার সম্পূর্ণ কথা:** {full_text}")
            st.info("টিপস: কথা বলার সময় এভাবে বলুন— 'বাংলাদেশের রাজধানী কী? অপশন ঢাকা অপশন খুলনা অপশন সিলেট'")
