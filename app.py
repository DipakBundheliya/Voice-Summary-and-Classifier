import streamlit as st
from dialogue_classifier import my_dialogue_classifier
from summarizer import my_summarizer
import os
from datetime import datetime

# Assume these are your two functions for classification and summarization
def classify_dialogue(audio_path):
    cls = my_dialogue_classifier(audio_path)
    dialogue = cls.classify() 
    # Replace with actual dialogue classification logic
    print("###",dialogue)
    return dialogue

def generate_summary(dialogue):
    # Replace with actual summary generation logic
    sm = my_summarizer()
    summary = sm.summarize(dialogue)
    return summary

def format_dialogue(dialogue):
    formatted_text = ""
    for entry in dialogue:
        for speaker, text in entry.items():
            if text.strip():  # Only add if the text is not empty
                formatted_text += f"**{speaker}:** {text}\n\n"
    return formatted_text



def main():

    st.set_page_config(page_title="Audio Transcriber and Summarizer", page_icon="🎙️", layout="centered")
    
    st.markdown("""
    <style>
    /* Change header color */
    header[data-testid="stHeader"] {
        background-color: #f0f2f6;
    }
    /* Remove the white line */
    .css-18e3th9 {
        padding-top: 0rem;
    }
    .css-1d391kg {
        display: none;
    }
    .css-1d391kg:before {
        content: '';
        display: block;
        height: 10px;
        background-color: #4CAF50;
    }
    /* Main content styling */
    .main {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 20px;
    }
    /* Upload box styling */
    .upload-box {
        border: 2px dashed #bbb;
        padding: 20px;
        text-align: center;
        background-color: #fff;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    /* Button styling */
    .button-container {
        display: flex;
        justify-content: center;
        margin-top: 20px;
    }
    .button-container > div {
        margin: 0 10px;
    }
    .stButton > button {
        color: white;
        background-color: #4c58af;
        border: none;
        padding: 10px 24px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 8px;
        transition-duration: 0.4s;
    }
    .stButton > button:hover {
        background-color: #4c58af;
    }
    .stButton > button:active {
        color: #ffffff; /* or any other color you want */
    }
    /* Transcription and summary boxes */
    .transcription, .summary {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("🎙️ Audio Conversation Transcriber and Summarizer")

    audio_file = st.file_uploader("Upload an audio file", type=["mp3", "wav"], help="Supported formats: mp3, wav")
    if audio_file is not None:

        st.audio(audio_file, format="audio/wav")

        save_folder = "uploaded_files"
        os.makedirs(save_folder, exist_ok=True)

        # Save the file with a unique name (using a timestamp to avoid conflicts)
        save_path = os.path.join(save_folder, f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{audio_file.name}")
        
        # Save the file
        with open(save_path, "wb") as f:
            f.write(audio_file.getbuffer())
        
        # Confirm saving
        st.success(f"File saved at: {save_path}"
                   )
        print(save_path)
        
        transcribed_text = ""
        summary_text = ""
        
        col1, col2 = st.columns([1, 4])
        
        with col1:
            if st.button("Transcribe"):
                with st.spinner("Transcribing..."):
                    transcribed_text = classify_dialogue(save_path) 
                    st.session_state['transcribed_text'] = transcribed_text 
                    
        with col2:
            if st.button("Summarize"):
                with st.spinner("Summarizing..."):
                    if 'transcribed_text' in st.session_state:
                        transcribed_text = st.session_state['transcribed_text']
                        summary_text = generate_summary(transcribed_text)
                        st.session_state['summary_text'] = summary_text
                    else:
                        st.error("Please transcribe the audio first.")
        
        if 'transcribed_text' in st.session_state: 
            # Format the dialogue
            formatted_dialogue = format_dialogue(transcribed_text)
            
            # Display the formatted dialogue
            st.markdown("### Transcribed Dialogue")
            st.markdown(formatted_dialogue)                                        
            st.session_state['transcribed_text'] = transcribed_text
    

        if 'summary_text' in st.session_state:
            st.markdown('<div class="summary"><h3>Summary of the Conversation</h3><p>{}</p></div>'.format(st.session_state['summary_text']), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
