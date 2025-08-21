# neuro_nudge_app.py
import streamlit as st
import time
import json
from datetime import datetime
import random

# Page configuration
st.set_page_config(
    page_title="NeuroNudge",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for gentle styling
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        background-color: #6c757d;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 24px;
        font-size: 18px;
    }
    .stButton>button:hover {
        background-color: #5a6268;
        color: white;
    }
    .task-item {
        background-color: #e9ecef;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
        border-left: 5px solid #6c757d;
    }
    .progress-bar {
        height: 20px;
        background-color: #e9ecef;
        border-radius: 10px;
        margin: 10px 0;
    }
    .progress-fill {
        height: 100%;
        background-color: #4CAF50;
        border-radius: 10px;
        text-align: center;
        color: white;
        line-height: 20px;
        transition: width 0.5s;
    }
    .nudge-box {
        background-color: #d1ecf1;
        border-left: 5px solid #0c5460;
        padding: 15px;
        border-radius: 10px;
        margin: 15px 0;
    }
    @keyframes grow {
        from { transform: scale(1); }
        to { transform: scale(1.05); }
    }
    .growing-companion {
        animation: grow 1s infinite alternate;
        text-align: center;
        font-size: 50px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state variables
if 'current_task' not in st.session_state:
    st.session_state.current_task = ""
if 'subtasks' not in st.session_state:
    st.session_state.subtasks = []
if 'timer_active' not in st.session_state:
    st.session_state.timer_active = False
if 'timer_duration' not in st.session_state:
    st.session_state.timer_duration = 25 * 60  # 25 minutes in seconds
if 'timer_start' not in st.session_state:
    st.session_state.timer_start = 0
if 'mood' not in st.session_state:
    st.session_state.mood = "neutral"
if 'progress' not in st.session_state:
    st.session_state.progress = 0
if 'companion_level' not in st.session_state:
    st.session_state.companion_level = 1

# Mock functions - to be replaced with actual implementations
def analyze_mood(text):
    """Mock mood analysis - will be replaced with Hugging Face model"""
    positive_words = ["good", "great", "happy", "excited", "ready", "focus"]
    negative_words = ["tired", "sad", "anxious", "stressed", "overwhelmed"]
    
    if any(word in text.lower() for word in positive_words):
        return "positive"
    elif any(word in text.lower() for word in negative_words):
        return "negative"
    return "neutral"

def break_down_task(task):
    """Mock task breakdown - will be replaced with LLM"""
    subtasks = []
    if "clean" in task.lower() and "room" in task.lower():
        subtasks = ["Pick up clothes from floor", "Make the bed", "Dust surfaces", "Vacuum the floor"]
    elif "write" in task.lower() and "report" in task.lower():
        subtasks = ["Outline main sections", "Research information", "Write first draft", "Revise and edit"]
    else:
        subtasks = [f"Step {i+1}: Work on {task}" for i in range(3)]
    
    return subtasks

def get_nudge_message(mood):
    """Get a gentle nudge based on mood"""
    positive_nudges = [
        "You're doing great! Keep up the momentum! 🌟",
        "Your progress is amazing! Let's keep going! 💪",
        "Wow, you're on fire! Ready for the next step? 🔥"
    ]
    
    neutral_nudges = [
        "Let's take this one step at a time. You've got this! 👍",
        "Breaking things down makes them more manageable. Ready to continue? 📋",
        "Focus on just this one thing right now. You can do it! ✨"
    ]
    
    negative_nudges = [
        "It's okay to feel overwhelmed. Let's just focus on one small thing. 🌱",
        "Be kind to yourself. How about we try a shorter focus session? 🕊️",
        "Remember to breathe. You're doing better than you think. 💚"
    ]
    
    if mood == "positive":
        return random.choice(positive_nudges)
    elif mood == "negative":
        return random.choice(negative_nudges)
    else:
        return random.choice(neutral_nudges)

# App layout
st.title("🧠 NeuroNudge")
st.markdown("### Productivity, Gently Done")

# Sidebar for settings and progress
with st.sidebar:
    st.header("Settings")
    
    # Mood input
    mood_input = st.text_area("How are you feeling today?")
    if mood_input:
        st.session_state.mood = analyze_mood(mood_input)
        st.write(f"Detected mood: {st.session_state.mood}")
    
    # Timer settings
    st.subheader("Focus Timer")
    timer_minutes = st.slider("Session length (minutes)", 5, 60, 25)
    st.session_state.timer_duration = timer_minutes * 60
    
    # Progress companion
    st.subheader("Progress Companion")
    companion_emojis = ["🌱", "🌿", "🌳", "🌺", "🌷", "🌸", "🍀", "🎋"]
    companion_index = min(st.session_state.companion_level - 1, len(companion_emojis) - 1)
    st.markdown(f'<div class="growing-companion">{companion_emojis[companion_index]}</div>', unsafe_allow_html=True)
    st.write(f"Level {st.session_state.companion_level}")
    
    # Progress bar
    st.subheader("Overall Progress")
    progress_percent = min(st.session_state.progress, 100)
    st.markdown(f"""
    <div class="progress-bar">
        <div class="progress-fill" style="width: {progress_percent}%;">{progress_percent}%</div>
    </div>
    """, unsafe_allow_html=True)

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    # Task input
    st.subheader("Your Task")
    task_input = st.text_input("What would you like to work on?")
    
    if task_input and not st.session_state.current_task:
        if st.button("Break Down Task"):
            st.session_state.current_task = task_input
            st.session_state.subtasks = break_down_task(task_input)
    
    # Display subtasks
    if st.session_state.subtasks:
        st.subheader("Action Steps")
        for i, subtask in enumerate(st.session_state.subtasks):
            st.markdown(f"""
            <div class="task-item">
                <input type="checkbox" id="task{i}" name="task{i}" value="done">
                <label for="task{i}"> {subtask}</label>
            </div>
            """, unsafe_allow_html=True)
        
        # Timer section
        st.subheader("Focus Timer")
        timer_placeholder = st.empty()
        
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("Start Focus Session") and not st.session_state.timer_active:
                st.session_state.timer_active = True
                st.session_state.timer_start = time.time()
        
        with col_b:
            if st.button("Take a Break") and st.session_state.timer_active:
                st.session_state.timer_active = False
                st.session_state.progress += 10
                if st.session_state.progress % 30 == 0:
                    st.session_state.companion_level += 1
                st.balloons()
        
        # Timer logic
        if st.session_state.timer_active:
            elapsed = time.time() - st.session_state.timer_start
            remaining = max(0, st.session_state.timer_duration - elapsed)
            
            mins, secs = divmod(int(remaining), 60)
            timer_placeholder.metric("Time Remaining", f"{mins:02d}:{secs:02d}")
            
            # Progress bar for current session
            progress_percent = 100 * (elapsed / st.session_state.timer_duration)
            st.markdown(f"""
            <div class="progress-bar">
                <div class="progress-fill" style="width: {progress_percent}%;">{int(progress_percent)}%</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Check if timer is complete
            if remaining <= 0:
                st.session_state.timer_active = False
                st.session_state.progress += 10
                if st.session_state.progress % 30 == 0:
                    st.session_state.companion_level += 1
                st.success("Great job! Session completed! 🎉")
                st.balloons()

with col2:
    # Gentle nudges and reminders
    st.subheader("Gentle Nudges")
    st.markdown(f'<div class="nudge-box">{get_nudge_message(st.session_state.mood)}</div>', unsafe_allow_html=True)
    
    # Mood-based suggestions
    st.subheader("Suggestions")
    if st.session_state.mood == "positive":
        st.info("""
        🌟 You're in a great mindset! 
        - Try tackling the most challenging part of your task first
        - Consider extending your focus session by 5 minutes
        """)
    elif st.session_state.mood == "negative":
        st.info("""
        🕊️ Be kind to yourself today
        - Start with just 10 minutes of focused work
        - Remember that small steps still count as progress
        - Take more frequent breaks if needed
        """)
    else:
        st.info("""
        📋 Ready to get started?
        - Pick one small task to begin with
        - Set a reasonable timer that feels achievable
        - Remember you can adjust as you go
        """)
    
    # Calming sounds
    st.subheader("Calming Sounds")
    sound_option = st.selectbox("Background sound", ["None", "Rain", "Forest", "Cafe", "White Noise"])
    if sound_option != "None":
        st.write(f"Playing gentle {sound_option.lower()} sounds...")
        
    # Visual reminders
    st.subheader("Visual Reminder")
    reminder_text = st.text_input("Add a positive reminder for yourself", "I am capable of focused work")
    if reminder_text:
        st.markdown(f"**{reminder_text}** ✨")

# Footer
st.markdown("---")
st.markdown("NeuroNudge 🧠 | Productivity, Gently Done | Designed with neurodiversity in mind")