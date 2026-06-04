import streamlit as st
import mediapipe as mp
import numpy as np
from PIL import Image
import io

# --- Configuration & Initialization ---
st.set_page_config(page_title="Offline Biometric Verification", layout="centered")
st.title("🛡️ Secure Face Recognition & Liveness Probe")
st.caption("Hackathon Simulation Sandbox - 100% Offline Architecture")

# Initialize MediaPipe Face Mesh (Lightweight landmark tracking)
@st.cache_resource
def load_mediapipe_models():
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7
    )
    return face_mesh

face_mesh = load_mediapipe_models()

# --- Helper Functions ---
def calculate_ear(landmarks, eye_indices):
    """Calculate Eye Aspect Ratio (EAR) to detect eye blinks."""
    # Vertical landmarks
    p2_p6 = np.linalg.norm(np.array(landmarks[eye_indices[1]]) - np.array(landmarks[eye_indices[5]]))
    p3_p5 = np.linalg.norm(np.array(landmarks[eye_indices[2]]) - np.array(landmarks[eye_indices[4]]))
    # Horizontal landmark
    p1_p4 = np.linalg.norm(np.array(landmarks[eye_indices[0]]) - np.array(landmarks[eye_indices[3]]))
    
    ear = (p2_p6 + p3_p5) / (2.0 * p1_p4)
    return ear

def mock_extract_embedding(pil_img):
    """
    Simulates generating a 128-D vector embedding (e.g., MobileFaceNet behavior).
    Uses Pillow and NumPy instead of OpenCV.
    """
    # Resize and convert to grayscale using PIL
    resized_gray = pil_img.resize((112, 112)).convert("L")
    gray_array = np.array(resized_gray)
    
    # Using normalized mean as a deterministic dummy descriptor for this sandbox
    np.random.seed(int(np.mean(gray_array)))
    embedding = np.random.rand(128)
    return embedding / np.linalg.norm(embedding)

# --- App States & Persistent Mock Database ---
if "registered_embedding" not in st.session_state:
    st.session_state.registered_embedding = None
if "blink_count" not in st.session_state:
    st.session_state.blink_count = 0
if "eye_closed" not in st.session_state:
    st.session_state.eye_closed = False

# --- UI Sidebar: Database Enrollment ---
st.sidebar.header("👤 1. Enrolment (Database)")
uploaded_file = st.sidebar.file_uploader("Upload Master Identity Photo", type=["jpg", "png", "jpeg"])

if uploaded_file:
    # Open image using PIL
    img_pil = Image.open(uploaded_file).convert("RGB")
    img_rgb = np.array(img_pil)
    
    # Process reference image to generate embedding
    results = face_mesh.process(img_rgb)
    if results.multi_face_landmarks:
        st.sidebar.image(img_pil, caption="Enrolled Profile", use_container_width=True)
        if st.sidebar.button("Generate Master Embedding"):
            st.session_state.registered_embedding = mock_extract_embedding(img_pil)
            st.sidebar.success("✅ Secure 128-D Vector Saved Locally!")
    else:
        st.sidebar.error("No face detected in reference photo. Use a clear, well-lit portrait.")

# --- Main Interface: Field Authentication & Verification Pipeline ---
st.header("📸 2. Field Authentication Terminal")

if st.session_state.registered_embedding is None:
    st.info("💡 Please enroll a profile photo using the sidebar panel first to begin verification testing.")
else:
    # Camera Input frame capture
    img_file_buffer = st.camera_input("Position face clearly within the camera frame")
    
    if img_file_buffer is not None:
        # Convert frame buffer directly to a PIL Image
        live_img_pil = Image.open(img_file_buffer).convert("RGB")
        img_rgb = np.array(live_img_pil)
        h, w, _ = img_rgb.shape
        
        # 1. Landmark & Mesh Processing
        results = face_mesh.process(img_rgb)
        
        if results.multi_face_landmarks:
            landmarks = results.multi_face_landmarks[0].landmark
            
            # Extract point coordinates scaled to image resolution
            coord_list = [(int(lm.x * w), int(lm.y * h)) for lm in landmarks]
            
            # Landmark Index Maps for Compound Eye Configurations
            LEFT_EYE = [33, 160, 158, 133, 153, 144]
            RIGHT_EYE = [362, 385, 387, 263, 373, 380]
            
            # 2. Pipeline Stage A: Calculate Eye Aspect Ratio (Liveness Metric)
            left_ear = calculate_ear(coord_list, LEFT_EYE)
            right_ear = calculate_ear(coord_list, RIGHT_EYE)
            avg_ear = (left_ear + right_ear) / 2.0
            
            # Blink detection state threshold machine
            EAR_THRESHOLD = 0.22
            if avg_ear < EAR_THRESHOLD:
                if not st.session_state.eye_closed:
                    st.session_state.eye_closed = True
            else:
                if st.session_state.eye_closed:
                    st.session_state.blink_count += 1
                    st.session_state.eye_closed = False
            
            # 3. Pipeline Stage B: Verify Identity via Vector Similarity Matching
            live_embedding = mock_extract_embedding(live_img_pil)
            # Compute cosine similarity
            similarity_score = np.dot(st.session_state.registered_embedding, live_embedding)
            
            # --- Results Dashboard & Visual Assessment Metric Cards ---
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(label="Current EAR Metrics", value=f"{avg_ear:.3f}")
            with col2:
                st.metric(label="Registered Blinks", value=st.session_state.blink_count)
            with col3:
                st.metric(label="Vector Match Score", value=f"{similarity_score*100:.1f}%")
            
            # --- Verification Decision Rules ---
            SIMILARITY_THRESHOLD = 0.85
            
            st.markdown("---")
            if similarity_score >= SIMILARITY_THRESHOLD and st.session_state.blink_count >= 1:
                st.balloons()
                st.success("🎉 **ACCESS GRANTED:** Authentication Successful!")
                st.caption("Criteria Fulfilled: Identity Matches Database & Passive Liveness Checked.")
                
                # Mock Sync and Purge implementation simulation trigger
                if st.button("Simulate AWS Sync & Local Cache Purge"):
                    st.toast("Syncing telemetry logs securely with AWS Datalake 3.0 backend...")
                    st.session_state.blink_count = 0
                    st.session_state.eye_closed = False
                    st.success("💥 Transaction complete. Local volatile cache cleared down.")
            else:
                st.warning("🚨 **PENDING VERIFICATION:** Verification conditions incomplete.")
                if similarity_score < SIMILARITY_THRESHOLD:
                    st.write("❌ Identity profile mismatch or poor field environment conditions.")
                if st.session_state.blink_count < 1:
                    st.write("⏳ *Liveness action required: Please blink your eyes intentionally to clear spoof checks.*")
        else:
            st.error("No active facial presence detected in frame. Adjust alignment and avoid heavy shadows.")
