import streamlit as st
from few_shot import FewShotPosts
from post_generator import generate_post

# Options for controls
length_options = ["Short", "Medium", "Long"]
language_options = ["English", "Hinglish"]
tone_options = [
    "Professional 👔",
    "Casual 😌",
    "Witty 👻",
    "Storytelling 📖",
    "Motivational 🚀",
    "Educational 📚"
]

# Page config
st.set_page_config(
    page_title="LinkedIn Post Generator",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    /* Global Polish */
    .stApp {
        background-color: #0e1117;
    }
    
    /* Post container */
    .stTextArea > div > div > textarea {
        background-color: #1c1c1c;
        border: 1px solid #333;
        border-radius: 12px;
        color: #f0f0f0;
        font-size: 16px;
        line-height: 1.6;
    }
    
    /* Button Styling */
    div.stButton > button {
        background: linear-gradient(90deg, #4b6cb7 0%, #182848 100%);
        border: none;
        color: white;
        height: 50px;
        border-radius: 25px;
        font-weight: 700;
        font-size: 16px;
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    }
    
    /* Sidebar polish */
    section[data-testid="stSidebar"] {
        background-color: #151515;
    }
    
    .sidebar-header {
        font-size: 20px;
        font-weight: bold;
        margin-bottom: 20px;
        color: #ddd;
    }
</style>
""", unsafe_allow_html=True)


def main():
    
    # --- Sidebar Controls ---
    with st.sidebar:
        st.markdown('<div class="sidebar-header">⚙️ Configuration</div>', unsafe_allow_html=True)
        
        # Load Tag Data
        fs = FewShotPosts()
        tags = fs.get_tags()
        
        # Topic Selection
        topic_mode = st.radio("Topic Source:", ["Select from List", "Custom Topic"], horizontal=True)
        
        selected_tag = None
        custom_topic = None
        
        if topic_mode == "Select from List":
            selected_tag = st.selectbox("Choose a Topic", options=tags)
        else:
            custom_topic = st.text_input("Enter your Topic", placeholder="e.g. AI Agents, Space Travel...")
        
        st.markdown("---")
        
        # Other Controls
        selected_length = st.selectbox("Length", options=length_options)
        selected_language = st.selectbox("Language", options=language_options)
        selected_tone = st.selectbox("Tone / Style", options=tone_options)
        
        st.markdown("---")
        generate_clicked = st.button("✨ Generate Post", use_container_width=True)

    # --- Main Content Area ---
    st.markdown("## 📝 LinkedIn Post Generator")
    st.caption("Create engaging content in seconds using advanced AI few-shot prompting.")

    # Initialize session state for the post content
    if "generated_post" not in st.session_state:
        st.session_state.generated_post = ""

    # Generate Handler
    if generate_clicked:
        # Validation
        if topic_mode == "Custom Topic" and not custom_topic:
            st.error("Please enter a custom topic.")
        else:
            with st.spinner("Writing your masterful post..."):
                # Clean up tone string (remove emoji)
                clean_tone = selected_tone.split(" ")[0]
                
                post = generate_post(
                    selected_length, 
                    selected_language, 
                    selected_tag,
                    clean_tone,
                    custom_topic
                )
                st.session_state.generated_post = post

    # Display & Edit Area
    if st.session_state.generated_post:
        st.markdown("### ✍️ Your Post (Editable)")
        
        # Editable Text Area
        final_post = st.text_area(
            label="Edit your post before publishing:",
            value=st.session_state.generated_post,
            height=350,
            label_visibility="collapsed"
        )
        
        st.write("")
        
        # Action Buttons
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
             st.download_button(
                "⬇️ Download Text",
                data=final_post,
                file_name="linkedin_post.txt",
                mime="text/plain",
                use_container_width=True
            )
            
        with col2:
            if st.button("📋 Copy to Clipboard", use_container_width=True):
                st.toast("Copied to clipboard! (Simulated)", icon="✅")
                # Note: Real clipboard access in basic Streamlit is limited without components, 
                # so we stick to simulated feedback or specialized components.

        with col3:
            st.info(f"**Mode:** {selected_length} | {selected_language} | {selected_tone}")


if __name__ == "__main__":
    main()
