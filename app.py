import streamlit as st
import whisper

st.title("🎙️ বাংলা MCQ জেনারেটর")
st.write("সহজেই মুখে বলে এমসিকিউ তৈরি করুন।")

# একটু ভালো মানের মডেল লোড করা, যা বাংলা ভালো বোঝে
@st.cache_resource
def load_model():
    # 'tiny' বদলে 'base' বা 'small' ব্যবহার করছি ভালো বাংলা অ্যাকুরেসির জন্য
    return whisper.load_model("base")

model = load_model()

audio_file = st.audio_input("🎤 এখানে ক্লিক করে রেকর্ড করুন অথবা অডিও ফাইল আপলোড করুন")

if audio_file is not None:
    with st.spinner("আপনার কণ্ঠস্বর প্রসেস করা হচ্ছে (প্রথমবার একটু সময় লাগতে পারে)..."):
        with open("temp_audio.wav", "wb") as f:
            f.write(audio_file.getbuffer())
        
        # ট্রান্সক্রিপ্ট করার সময় মডেলকে জোর দিয়ে বলা হচ্ছে ভাষা 'bangla'
        result = model.transcribe("temp_audio.wav", language="bn")
        full_text = result['text'].strip()
        
        st.info(f"**আপনার কণ্ঠস্বর থেকে প্রাপ্ত টেক্সট:** {full_text}")
        
        # বাংলা 'অপশন' বা ইংরেজি 'option' দুইটাই চেক করবে সেফটির জন্য
        trigger_word = None
        if "অপশন" in full_text:
            trigger_word = "অপশন"
        elif "option" in full_text.lower():
            trigger_word = "option"
            
        if trigger_word:
            if trigger_word == "option":
                parts = full_text.lower().split("option")
            else:
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
            st.warning("⚠️ টেক্সটের মধ্যে 'অপশন' বা 'Option' শব্দটি খুঁজে পাওয়া যায়নি।")
            st.info("টিপস: মাইক্রোফোনের খুব কাছে গিয়ে স্পষ্ট ও একটু জোরে বলুন— 'বাংলাদেশের রাজধানী কী? অপশন ঢাকা অপশন খুলনা অপশন সিলেট'")
