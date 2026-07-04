import datetime
import streamlit as st
from few_shot import FewShotPosts
from post_generator import generate_post

length_options = ["Short", "Medium", "Long"]
language_options = ["English", "Hinglish"]
tone_options = [
    "Professional 👔",
    "Casual 😌",
    "Witty 👻",
    "Storytelling 📖",
    "Motivational 🚀",
    "Educational 📚",
]
emoji_density_options = ["None", "Low", "Medium", "High"]
hook_options = ["None", "Question hook", "Contrarian take", "Story hook", "Stat hook"]
max_chars = 3000
ideal_range = (1300, 2000)
tone_palette = {
    "Professional": ("#5B8CFF", "blue"),
    "Casual": ("#F29E4C", "orange"),
    "Witty": ("#D56BFF", "purple"),
    "Storytelling": ("#4CC9F0", "cyan"),
    "Motivational": ("#2ECF6B", "green"),
    "Educational": ("#FF7A59", "coral"),
}

st.set_page_config(page_title="LinkedIn Post Generator", page_icon="📝", layout="wide", initial_sidebar_state="expanded")

st.markdown(
    """
    <style>
        :root { color-scheme: dark; }
        .stApp {
            background: radial-gradient(circle at top left, rgba(80, 91, 255, 0.16), transparent 24%),
                        radial-gradient(circle at bottom right, rgba(255, 109, 109, 0.12), transparent 18%),
                        #0b1220;
            color: #f2f4f8;
        }
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #101521 0%, #121926 100%);
            border-right: 1px solid rgba(255,255,255,0.08);
        }
        .sidebar-header {
            font-size: 22px; font-weight: 800; margin-bottom: 8px; color: #f6f7fa;
        }
        .sidebar-sticky {
            position: sticky; top: 0.6rem; z-index: 10; padding: 10px 0 12px 0;
            background: linear-gradient(180deg, rgba(16,21,33,0.95) 0%, rgba(16,21,33,0.85) 100%);
            backdrop-filter: blur(8px);
        }
        .stSidebar .stButton>button,
        .stButton>button {
            background: linear-gradient(90deg, #5664ff 0%, #1f335a 100%);
            border: none; color: white; min-height: 48px; border-radius: 18px; font-weight: 700;
            box-shadow: 0 14px 28px rgba(19, 41, 84, 0.18);
        }
        .stButton>button:hover { transform: translateY(-1px); box-shadow: 0 16px 30px rgba(19, 41, 84, 0.28); }
        .stTextArea>div>div>textarea,
        .stTextInput>div>div>input,
        .stSelectbox>div>div>div>div,
        .stMultiselect>div>div>div>div {
            background: #121927 !important; color: #f5f7ff !important;
            border: 1px solid rgba(255,255,255,0.08) !important; border-radius: 14px !important;
            box-shadow: inset 0 0 0 1px rgba(255,255,255,0.02);
        }
        .stSelectbox>div>div>div>div:focus-within,
        .stTextInput>div>div>input:focus,
        .stTextArea>div>div>textarea:focus {
            box-shadow: 0 0 0 3px rgba(86, 100, 255, 0.24) !important;
        }
        .stTextArea>div>div>textarea { min-height: 340px; }
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 { color: #f4f7ff; }
        .block-container { padding-top: 24px; padding-left: 28px; padding-right: 28px; padding-bottom: 24px; }
        .stInfo, .stAlert { border-radius: 18px; padding: 18px 22px; }
        .hashtag-pill {
            display: inline-block; padding: 8px 12px; margin: 4px 4px 4px 0; border-radius: 999px;
            background: rgba(86, 100, 255, 0.18); color: #c0d3ff; font-size: 0.95rem;
        }
        .tone-badge {
            display: inline-block; padding: 6px 10px; border-radius: 999px; margin: 4px 6px 4px 0; font-size: 0.86rem; font-weight: 700;
            color: white; border: 1px solid rgba(255,255,255,0.1);
        }
        .preview-card {
            background: linear-gradient(180deg, #111827 0%, #161d2c 100%);
            border: 1px solid rgba(255,255,255,0.08); border-radius: 20px; padding: 18px 18px 16px 18px;
            box-shadow: 0 10px 22px rgba(0,0,0,0.24);
        }
        .avatar-circle {
            width: 44px; height: 44px; border-radius: 50%; background: linear-gradient(135deg, #5664ff 0%, #3a5cff 100%);
            display: flex; align-items: center; justify-content: center; font-weight: 800; color: white;
        }
        .preview-meta { color: #9aa6bf; font-size: 0.95rem; margin-top: 2px; }
        .progress-track {
            width: 100%; height: 8px; border-radius: 999px; background: rgba(255,255,255,0.08); overflow: hidden; margin-top: 8px;
        }
        .progress-fill.good { background: linear-gradient(90deg, #2ecc71 0%, #1f9e59 100%); }
        .progress-fill.warn { background: linear-gradient(90deg, #f4b942 0%, #e08f10 100%); }
        .progress-fill.danger { background: linear-gradient(90deg, #ff6b6b 0%, #c0392b 100%); }
        .empty-state-card {
            border: 1px dashed rgba(255,255,255,0.16); border-radius: 20px; padding: 18px; background: rgba(255,255,255,0.03);
        }
        .hero-step-card {
            background: linear-gradient(180deg, rgba(86,100,255,0.16), rgba(17,24,39,0.8));
            border: 1px solid rgba(255,255,255,0.08); border-radius: 18px; padding: 14px 14px 14px 14px; min-height: 118px;
            box-shadow: inset 0 1px 0 rgba(255,255,255,0.03);
        }
        .hero-summary {
            background: rgba(86, 100, 255, 0.08); border: 1px solid rgba(86, 100, 255, 0.18); border-radius: 18px;
            padding: 16px 18px; margin: 18px 0 14px 0; color: #dce4ff;
        }
        .hero-summary strong { color: #ffffff; }
        .step-number {
            display: inline-flex; align-items: center; justify-content: center; width: 30px; height: 30px;
            border-radius: 999px; background: rgba(86,100,255,0.24); color: #dfe7ff; font-weight: 800; margin-bottom: 10px;
        }
        .feature-card {
            background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); border-radius: 16px; padding: 12px 14px; margin-bottom: 10px;
        }
        .feature-card strong { color: #f4f7ff; }
        .hero-badge {
            display: inline-block; padding: 8px 12px; border-radius: 999px; background: rgba(46,207,107,0.14);
            color: #bff3d2; border: 1px solid rgba(46,207,107,0.2); margin: 8px 0 14px 0; font-size: 0.95rem;
        }
        .example-card {
            background: linear-gradient(180deg, rgba(17,24,39,0.96), rgba(10,14,24,0.92));
            border: 1px solid rgba(255,255,255,0.08); border-radius: 16px; padding: 14px; min-height: 140px;
        }
        .example-card .tone-chip { display: inline-block; font-size: 0.8rem; font-weight: 700; padding: 4px 8px; border-radius: 999px; background: rgba(86,100,255,0.16); color: #cbd8ff; margin-bottom: 8px; }
        .sample-preview {
            background: linear-gradient(180deg, #111827 0%, #171f2f 100%); border: 1px solid rgba(255,255,255,0.08); border-radius: 20px; padding: 16px; min-height: 180px;
        }
        .sample-preview .sample-line { height: 9px; border-radius: 999px; background: rgba(255,255,255,0.12); margin-bottom: 8px; }
        .sample-preview .sample-line.short { width: 70%; }
        .sample-preview .sample-line.medium { width: 92%; }
        .sample-preview .sample-line.tiny { width: 56%; }
        .skeleton-line { height: 10px; border-radius: 999px; background: rgba(255,255,255,0.12); margin-bottom: 8px; }
        .skeleton-line.short { width: 72%; }
        .skeleton-line.medium { width: 92%; }
        .skeleton-line.tiny { width: 52%; }
        .sticky-header {
            position: sticky; top: 0; z-index: 100; padding: 8px 0 12px 0; background: rgba(11, 18, 32, 0.9); backdrop-filter: blur(8px);
            border-bottom: 1px solid rgba(255,255,255,0.06); margin-bottom: 12px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


def get_hashtag_suggestions(topic: str) -> list[str]:
    base_fallback = ["#LinkedIn", "#Content", "#Storytelling", "#Growth", "#Leadership"]
    if not topic:
        return base_fallback[:4]

    topic_text = topic.lower()
    suggestions = []
    if any(keyword in topic_text for keyword in ["ai", "artificial", "machine", "data", "llm", "model"]):
        suggestions.extend(["#AI", "#MachineLearning", "#FutureOfWork", "#DataScience", "#Innovation"])
    elif any(keyword in topic_text for keyword in ["career", "job", "leadership", "growth", "professional"]):
        suggestions.extend(["#CareerGrowth", "#Leadership", "#ProfessionalDevelopment", "#JobSearch", "#GrowthMindset"])
    elif any(keyword in topic_text for keyword in ["startup", "founder", "product", "business"]):
        suggestions.extend(["#StartupLife", "#ProductLedGrowth", "#Entrepreneurship", "#ScaleUp", "#MarketFit"])
    elif any(keyword in topic_text for keyword in ["wellness", "mental", "health", "balance"]):
        suggestions.extend(["#Wellbeing", "#MentalHealth", "#WorkLifeBalance", "#SelfCare", "#Mindset"])

    if not suggestions:
        core_words = [word.capitalize() for word in topic_text.replace("#", "").split() if word.isalpha()][:4]
        suggestions.extend([f"#{word}" for word in core_words])

    suggestions = list(dict.fromkeys(suggestions + base_fallback))
    if len(suggestions) < 4:
        suggestions.extend([tag for tag in base_fallback if tag not in suggestions])

    return suggestions[:8]


def get_tone_badges(selected_tone: str):
    badges = []
    for tone_name in tone_options:
        base_tone = tone_name.split(" ")[0]
        color, _ = tone_palette.get(base_tone, ("#5664ff", "blue"))
        active = selected_tone == tone_name
        badges.append(f'<span class="tone-badge" style="background:{color}; opacity:{1 if active else 0.6};">{tone_name}</span>')
    return "".join(badges)


def render_sidebar():
    fs = FewShotPosts()
    tags = sorted(fs.get_tags() or [])

    st.markdown('<div class="sidebar-header">⚙️ Configuration</div>', unsafe_allow_html=True)
    st.caption("Choose your topic, style, and generate strong LinkedIn content instantly.")

    st.markdown('<div class="sidebar-sticky">', unsafe_allow_html=True)
    generate_clicked = st.button("✨ Generate Post", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    with st.expander("📄 Content Settings", expanded=True):
        topic_mode = st.radio("Topic Source", ["Select from List", "Custom Topic"], horizontal=True)
        selected_tag = None
        custom_topic = None
        if topic_mode == "Select from List":
            selected_tag = st.selectbox("📝 Topic", options=tags, index=0)
        else:
            custom_topic = st.text_input("✍️ Custom Topic", placeholder="e.g. AI Agents, Space Travel...")
        selected_length = st.selectbox("📏 Length", options=length_options)
        selected_language = st.selectbox("🌐 Language", options=language_options)

    with st.expander("🎨 Style Settings", expanded=True):
        selected_tone = st.selectbox("💼 Tone / Style", options=tone_options)
        st.markdown(f"<div>{get_tone_badges(selected_tone)}</div>", unsafe_allow_html=True)
        selected_hook = st.selectbox("🪝 Hook / Opening style", options=hook_options)
        selected_emoji_density = st.selectbox("✨ Emoji density", options=emoji_density_options)
        selected_variant_count = st.slider("🔁 Output variants", min_value=1, max_value=3, value=2)

    st.markdown("\n---\n")
    st.markdown(
        "#### Quick tips"
        "\n- Keep your topic focused for sharper results."
        "\n- Use `Hinglish` for a more approachable voice."
        "\n- Pick a hook to strengthen the opening line."
    )

    return topic_mode, selected_tag, custom_topic, selected_length, selected_language, selected_tone, selected_hook, selected_emoji_density, selected_variant_count, generate_clicked


def render_preview_card(post_text: str):
    preview_body = post_text.replace("\n", "<br>").strip()
    st.markdown(
        f"""
        <div class="preview-card">
            <div style="display:flex; align-items:center; gap:12px; margin-bottom:12px;">
                <div class="avatar-circle">A</div>
                <div>
                    <div style="font-weight:700;">Alex Rivera</div>
                    <div class="preview-meta">Founder • 2h ago</div>
                </div>
            </div>
            <div style="font-size:1.02rem; line-height:1.7; color:#e8eef8;">{preview_body}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def build_history_entry(topic, selected_length, selected_language, selected_tone, selected_hook, variants):
    return {
        "timestamp": datetime.datetime.now().isoformat(timespec="minutes"),
        "topic": topic,
        "length": selected_length,
        "language": selected_language,
        "tone": selected_tone,
        "hook": selected_hook,
        "variants": variants,
    }


def main():
    if "generated_variants" not in st.session_state:
        st.session_state.generated_variants = []
    if "selected_variant" not in st.session_state:
        st.session_state.selected_variant = 0
    if "post_text" not in st.session_state:
        st.session_state.post_text = ""
    if "history" not in st.session_state:
        st.session_state.history = []
    if "last_generation" not in st.session_state:
        st.session_state.last_generation = {}
    if "selected_hashtags" not in st.session_state:
        st.session_state.selected_hashtags = []
    if "tavily_sources" not in st.session_state:
        st.session_state.tavily_sources = []
    if "tavily_source_status" not in st.session_state:
        st.session_state.tavily_source_status = ""

    with st.sidebar:
        (
            topic_mode,
            selected_tag,
            custom_topic,
            selected_length,
            selected_language,
            selected_tone,
            selected_hook,
            selected_emoji_density,
            selected_variant_count,
            generate_clicked,
        ) = render_sidebar()

        topic_name = custom_topic if topic_mode == "Custom Topic" else selected_tag
        hashtag_options = get_hashtag_suggestions(topic_name)
        valid_default_hashtags = [tag for tag in st.session_state.selected_hashtags if tag in hashtag_options]
        selected_hashtags = st.multiselect(
            "# Hashtag suggestions",
            options=hashtag_options,
            default=valid_default_hashtags or hashtag_options[:4],
            help="Toggle hashtags to keep them separate and copy them when you publish.",
        )
        st.session_state.selected_hashtags = list(selected_hashtags)

        with st.expander("🕘 Recent history", expanded=False):
            if st.session_state.history:
                for idx, item in enumerate(st.session_state.history[:5], start=1):
                    st.write(f"{idx}. {item['topic']} — {item['length']} / {item['tone']} / {item['hook']}")
            else:
                st.write("No history yet. Generate a post to see it here.")

    topic_name = custom_topic if topic_mode == "Custom Topic" else selected_tag
    show_home = not st.session_state.generated_variants

    st.markdown('<div class="sticky-header">', unsafe_allow_html=True)
    st.markdown("## 📝 LinkedIn Post Generator")
    st.caption("Generate polished posts with stronger hooks, better pacing, and multiple ready-to-compare variants.")
    st.markdown("</div>", unsafe_allow_html=True)

    if show_home:
        hero_col1, hero_col2 = st.columns([2, 1])
        with hero_col1:
            st.markdown("### Ready to write your next post?")
            st.write("Pick a topic, choose a tone, and generate multiple polished versions you can compare side-by-side.")
            st.markdown(
                """
                <div class="hero-summary">
                    <strong>Get a clearer starting point before you generate.</strong>
                    This generator combines structured post scaffolding with live Tavily context, hashtag suggestions, and instant variant comparisons.
                </div>
                <div class="hero-badge">🔍 Powered by live context from Tavily</div>
                """,
                unsafe_allow_html=True,
            )
        with hero_col2:
            st.markdown(
                """
                <div class="feature-card">
                    <div style="font-size: 0.9rem; color: #9aa6bf; margin-bottom: 6px;">Why it works</div>
                    <div><strong>🎯 Stronger hooks</strong><br><span style="color:#9aa6bf;">Proven opening patterns that pull readers in.</span></div>
                </div>
                <div class="feature-card">
                    <div><strong>📊 Better pacing</strong><br><span style="color:#9aa6bf;">Structured flow for readability and momentum.</span></div>
                </div>
                <div class="feature-card">
                    <div><strong>🔀 Multiple variants</strong><br><span style="color:#9aa6bf;">Compare and pick the version that fits best.</span></div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("### How it works")
        step_cols = st.columns(3)
        steps = [
            ("1. Pick a topic", "Choose from the list or enter a custom angle."),
            ("2. Choose a tone", "Set the voice, hook, and length to match your audience."),
            ("3. Generate", "Compare variants, refine the draft, and share it."),
        ]
        for idx, (title, desc) in enumerate(steps):
            with step_cols[idx]:
                st.markdown(
                    f"""
                    <div class="hero-step-card">
                        <div class="step-number">{idx + 1}</div>
                        <div><strong>{title}</strong><br><span style="color:#9aa6bf;">{desc}</span></div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        preview_cols = st.columns([1.1, 0.9])
        with preview_cols[0]:
            st.markdown("### Preview the experience")
            st.markdown(
                """
                <div class="sample-preview">
                    <div style="font-size: 0.9rem; color:#9aa6bf; margin-bottom: 8px;">Sample LinkedIn-style preview</div>
                    <div class="sample-line short"></div>
                    <div class="sample-line medium"></div>
                    <div class="sample-line tiny"></div>
                    <div class="sample-line medium"></div>
                    <div style="margin-top: 14px; color:#aeb8cb; font-size: 0.95rem;">Your generated post will appear here with a polished preview card and editable draft.</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with preview_cols[1]:
            st.markdown("### Example gallery")
            gallery_cols = st.columns(3)
            examples = [
                ("Professional", "A sharp, polished post for leadership and growth topics."),
                ("Witty", "A punchier voice for thought leadership and personal brand content."),
                ("Motivational", "An uplifting draft for career, resilience, and learning moments."),
            ]
            for idx, (tone, text) in enumerate(examples):
                with gallery_cols[idx]:
                    st.markdown(
                        f"""
                        <div class="example-card">
                            <div class="tone-chip">{tone}</div>
                            <div style="color:#e7ecf5; font-size: 0.96rem; line-height: 1.5;">{text}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

        st.markdown("---")
        st.info("👈 Start here: choose a custom topic or pick one from the list in the sidebar, then press Generate Post.")

    if generate_clicked:
        if topic_mode == "Custom Topic" and not custom_topic:
            st.error("Please enter a custom topic before generating a post.")
        else:
            placeholder = st.empty()
            with placeholder.container():
                st.markdown(
                    """
                    <div class="empty-state-card">
                        <div class="skeleton-line short"></div>
                        <div class="skeleton-line medium"></div>
                        <div class="skeleton-line tiny"></div>
                        <div class="skeleton-line medium"></div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            with st.spinner("Generating your post variants... this may take a moment."):
                clean_tone = selected_tone.split(" ")[0]
                variants, tavily_sources = generate_post(
                    selected_length,
                    selected_language,
                    selected_tag,
                    clean_tone,
                    custom_topic,
                    hook=selected_hook,
                    emoji_density=selected_emoji_density,
                    variant_count=selected_variant_count,
                )
                st.session_state.generated_variants = variants
                st.session_state.selected_variant = 0
                st.session_state.post_text = variants[0]
                st.session_state.last_generation = {
                    "tag": selected_tag,
                    "custom_topic": custom_topic,
                    "length": selected_length,
                    "language": selected_language,
                    "tone": selected_tone,
                    "hook": selected_hook,
                    "emoji_density": selected_emoji_density,
                    "variant_count": selected_variant_count,
                }
                st.session_state.tavily_sources = tavily_sources or []
                st.session_state.tavily_source_status = "live" if tavily_sources else "fallback"
                st.session_state.history.insert(0, build_history_entry(topic_name, selected_length, selected_language, selected_tone, selected_hook, variants))
                st.session_state.history = st.session_state.history[:10]
            placeholder.empty()

    if st.session_state.generated_variants:
        st.markdown("---")
        st.markdown("## ✨ Output variants")
        variant_cols = st.columns(len(st.session_state.generated_variants))
        for idx, variant in enumerate(st.session_state.generated_variants):
            with variant_cols[idx]:
                title = f"Variant {idx + 1}"
                if idx == st.session_state.selected_variant:
                    title += " ✅"
                st.markdown(f"#### {title}")
                st.text_area(label="", value=variant, height=220, key=f"variant_{idx}", disabled=True, label_visibility="collapsed")
                if st.button(f"Use this variant", key=f"use_variant_{idx}", use_container_width=True):
                    st.session_state.selected_variant = idx
                    st.session_state.post_text = variant
                    st.session_state.final_editor = variant

        st.markdown("---")
        editor_col, preview_col = st.columns([0.6, 0.4])
        with editor_col:
            st.markdown("## 📝 Final draft")
            if "final_editor" not in st.session_state or st.session_state.final_editor != st.session_state.post_text:
                st.session_state.final_editor = st.session_state.post_text
            final_post = st.text_area(label="Edit your final post:", value=st.session_state.final_editor, height=340, key="final_editor", label_visibility="collapsed")
            st.session_state.post_text = final_post
            char_count = len(final_post)
            word_count = len(final_post.split())
            if char_count <= ideal_range[0]:
                progress_class, message = "warn", "Shorter than the sweet spot."
            elif char_count >= ideal_range[1] and char_count <= max_chars:
                progress_class, message = "good", "Perfect length for LinkedIn engagement."
            elif char_count > max_chars:
                progress_class, message = "danger", "This is above LinkedIn’s practical character limit."
            else:
                progress_class, message = "warn", "Aiming for the ideal 1300-2000 character range."
            progress_pct = min(char_count / max_chars, 1.0)
            st.markdown(f'<div class="progress-track"><div class="progress-fill {progress_class}" style="width:{progress_pct * 100:.0f}%"></div></div>', unsafe_allow_html=True)
            st.caption(f"{char_count} / {max_chars} chars · {word_count} words · {message}")

            if st.session_state.selected_hashtags:
                st.markdown("#### Hashtag chips")
                chip_cols = st.columns(min(4, len(st.session_state.selected_hashtags)))
                for idx, tag in enumerate(st.session_state.selected_hashtags):
                    with chip_cols[idx % len(chip_cols)]:
                        if st.button(f"✕ {tag}", key=f"chip_{idx}", use_container_width=True):
                            st.session_state.selected_hashtags.remove(tag)
                            st.rerun()

        with preview_col:
            st.markdown("## 👀 Live preview")
            render_preview_card(st.session_state.post_text)
            if st.session_state.tavily_sources:
                st.success(f"🔍 Grounded with live context from {len(st.session_state.tavily_sources)} source(s)")
            else:
                st.warning("⚠️ Generated without live context")
            st.info("This preview mirrors the polished LinkedIn-style card you can share.")

        if st.session_state.tavily_sources:
            with st.expander("🔗 Live context sources", expanded=False):
                for source in st.session_state.tavily_sources:
                    title = source.get("title") or "Source"
                    content = source.get("content") or ""
                    url = source.get("url")
                    if url:
                        st.markdown(f"- [{title}]({url})  \n  {content}")
                    else:
                        st.markdown(f"- **{title}**  \n  {content}")

        st.markdown("---")
        action_col1, action_col2, action_col3 = st.columns([1, 1, 1])
        with action_col1:
            if st.button("♻️ Regenerate", use_container_width=True):
                if st.session_state.last_generation:
                    with st.spinner("Regenerating a fresh batch of variants..."):
                        variants, tavily_sources = generate_post(
                            st.session_state.last_generation["length"],
                            st.session_state.last_generation["language"],
                            st.session_state.last_generation["tag"],
                            st.session_state.last_generation["tone"].split(" ")[0],
                            st.session_state.last_generation["custom_topic"],
                            hook=st.session_state.last_generation["hook"],
                            emoji_density=st.session_state.last_generation["emoji_density"],
                            variant_count=st.session_state.last_generation["variant_count"],
                        )
                        st.session_state.generated_variants = variants
                        st.session_state.selected_variant = 0
                        st.session_state.post_text = variants[0]
                        st.session_state.tavily_sources = tavily_sources or []
                        st.session_state.tavily_source_status = "live" if tavily_sources else "fallback"
                        st.session_state.history.insert(0, build_history_entry(topic_name, st.session_state.last_generation["length"], st.session_state.last_generation["language"], st.session_state.last_generation["tone"], st.session_state.last_generation["hook"], variants))
                        st.session_state.history = st.session_state.history[:10]
        with action_col2:
            st.download_button("⬇️ Download Final", data=st.session_state.post_text, file_name="linkedin_post.txt", mime="text/plain", use_container_width=True)
        with action_col3:
            if st.button("📋 Copy final post", use_container_width=True):
                st.toast("Copied to clipboard!", icon="✅")

        st.markdown("---")
        st.info(f"**Mode:** {selected_length} | {selected_language} | {selected_tone} | {selected_hook} | {selected_emoji_density} emojis\n\n**Topic:** {topic_name}")
    else:
        st.markdown("---")
        st.info("Generate a batch to see multiple variants, a live preview card, and the character tracker.")


if __name__ == "__main__":
    main()
