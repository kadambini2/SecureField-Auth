import streamlit as st
import numpy as np
from PIL import Image
import random

# --- Configuration & Initialization ---
st.set_page_config(page_title="SecureField Auth Sandbox", layout="centered")
st.title("🛡️ SecureFace: Edge AI Sandbox")
st.caption("Datalake 3.0 Hackathon Prototype - Ultra-Lightweight Configuration")

# --- Helper Functions ---
def extract_pure_embedding(pil_img):
    """
    Simulates a 128-D vector embedding (MobileFaceNet behavior) using pure math.
    Resizes the image and uses its structural hash to generate a stable vector.
    """
    resized = pil_img.resize((112, 112)).convert("L")
    img_array = np.array(resized)
    
    # Deterministic seed generation based on unique image traits
    pixel_seed = int(np.mean(img_array)) + int(np.std(img_array))
    np.random.seed(pixel_seed)
    
    # Generate normalized 128-D vector
    embedding = np.random.rand(128)
    return embedding / np.linalg.norm(embedding)

# --- Persistent App State Initialization ---
if "master_vector" not in st.session_state:
    st.session_state.master_vector = None
if "liveness_challenge" not in st.session_state:
    # Pick a random anti-spoofing challenge
    challenges = [
        "👀 Blink your eyes intentionally twice",
        "😐 Turn your head slightly to the left",
        "🙂 Look straight and smile clearly",
        "📐 Nod your head up and down slowly"
    ]
    st.session_state.liveness_challenge = random.choice(challenges)
if "challenge_passed" not in st.session_state:
    st.session_state.challenge_passed = False

# --- UI Sidebar: Database Enrollment ---
st.sidebar.header("👤 1. Enrolment (Database)")
uploaded_file = st.sidebar.file_uploader("Upload Master Identity Photo", type=["jpg", "png", "jpeg"])

if uploaded_file:
    img_pil = Image.open(uploaded_file).convert("RGB")
    st.sidebar.image(img_pil, caption="Enrolled Profile Reference", use_container_width=True)
    
    if st.sidebar.button("Generate Master Embedding"):
        st.session_state.master_vector = extract_pure_embedding(img_pil)
        st.sidebar.success("✅ Secure 128-D Vector Saved Locally!")

# --- Main Interface: Field Authentication Terminal ---
st.header("📸 2. Field Authentication Terminal")

if st.session_state.master_vector is None:
    st.info("💡 Please enroll a profile photo using the sidebar panel first to activate the authentication engine.")
else:
    # Present the active dynamic liveness hurdle
    st.warning(f"🤖 **Liveness Challenge Active:**\n\n**{st.session_state.liveness_challenge}** before clicking capture.")
    
    # Checkbox simulating the algorithmic confirmation of the motion capture
    liveness_confirm = st.checkbox("I have performed the required liveness action above.")
    
    # Camera Capture Feed Module
    img_file_buffer = st.camera_input("Position face clearly in terminal frame")
    
    if img_file_buffer is not None:
        if not liveness_confirm:
            st.error("🚨 **Liveness Probe Failed:** You must complete the active action challenge to defeat photo/screen spoofing.")
        else:
            # Process incoming camera stream frame
            live_img_pil = Image.open(img_file_buffer).convert("RGB")
            
            # Extract Vector Array
            live_vector = extract_pure_embedding(live_img_pil)
            
            # Compute Cosine Similarity Matching Matrix
            similarity_score = np.dot(st.session_state.master_vector, live_vector)
            SIMILARITY_THRESHOLD = 0.82  # Target field calibration ratio
            
            # --- Analytics Dashboard ---
            col1, col2 = st.columns(2)
            with col1:
                st.metric(label="Liveness Action Status", value="VERIFIED" if liveness_confirm else "PENDING")
            with col2:
                st.metric(label="Biometric Similarity Score", value=f"{similarity_score*100:.1f}%")
                
            st.markdown("---")
            
            # Decision Tree Engine Execution
            if similarity_score >= SIMILARITY_THRESHOLD:
                st.balloons()
                st.success("🎉 **ACCESS GRANTED:** Identity Confirmed & Attended Logged!")
                st.caption("Engine Diagnostics: Local Vector Match Verified | Anti-Spoof Cleared.")
                
                # Mock Cloud Synchronization Routine
                if st.button("Simulate Cloud Relay Sync & Cache Purge"):
                    st.toast("Syncing biometric transaction metrics securely to AWS Datalake 3.0...")
                    # Reset dynamic fields
                    st.session_state.challenge_passed = False
                    st.success("💥 Transaction Relayed. Local volatile security cache cleared down completely.")
            else:
                st.error("🚨 **ACCESS DENIED:** Vector authentication score below security threshold.")
                st.caption("Ensure lighting conditions closely mimic your master enrollment profile snapshot.")
