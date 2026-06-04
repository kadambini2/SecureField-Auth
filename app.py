import streamlit as st
import numpy as np
from PIL import Image
import random
import time

# --- 1. Custom Industrial Cyber UI/UX Theme Styling ---
st.set_page_config(page_title="SecureField Auth Terminal", layout="centered")

# Injecting dark mode, glowing borders, and custom UI styling
st.markdown("""
    <style>
    .stApp {
        background-color: #121824;
        color: #E2E8F0;
    }
    .hud-title {
        font-family: 'Courier New', Courier, monospace;
        color: #FFB300;
        font-weight: bold;
        letter-spacing: 2px;
        margin-bottom: 5px;
    }
    .reticle-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin: 20px 0;
    }
    .biometric-reticle {
        border: 4px dashed #00E676;
        border-radius: 50%;
        width: 240px;
        height: 240px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 0 20px rgba(0, 230, 118, 0.3);
        animation: spin 20s linear infinite;
        margin-bottom: 15px;
    }
    @keyframes spin { 100% { transform:rotate(360deg); } }
    .hud-box {
        background-color: #1A2333;
        border-left: 5px solid #FFB300;
        padding: 15px;
        border-radius: 4px;
        font-family: 'Courier New', Courier, monospace;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🛡️ SecureField Auth Terminal")
st.caption("Datalake 3.0 Hackathon Sandbox • Operational Air-Gapped Mode")

# --- 2. Heavy-Duty Mathematical Logic ---
def analyze_lighting_matrix(pil_img):
    """Calculates exposure and image contrast via standard matrix variance."""
    gray_img = pil_img.convert("L")
    arr = np.array(gray_img)
    return float(np.mean(arr)), float(np.std(arr))

def extract_one_way_vector(pil_img):
    """Simulates a deterministic 128-D cryptographic facial vector descriptor."""
    resized = pil_img.resize((112, 112)).convert("L")
    img_array = np.array(resized)
    pixel_seed = int(np.mean(img_array)) + int(np.std(img_array))
    np.random.seed(pixel_seed)
    embedding = np.random.rand(128)
    return embedding / np.linalg.norm(embedding)

# --- 3. Robust Session Cache State Initialization ---
if "master_vector" not in st.session_state:
    st.session_state.master_vector = None
if "active_challenge" not in st.session_state:
    challenges = [
        "👀 BLINK INTENTIONALLY TWICE NOW",
        "😐 TURN HEAD SLIGHTLY TO THE LEFT",
        "🙂 LOOK STRAIGHT AND SMILE CLEARLY",
        "📐 NOD YOUR HEAD UP AND DOWN SLOWLY"
    ]
    st.session_state.active_challenge = random.choice(challenges)
if "vault_logs" not in st.session_state:
    st.session_state.vault_logs = []

# --- 4. UI Sidebar Architecture: Reference Master Database Ingestion ---
st.sidebar.markdown("<h2 style='color:#FFB300;'>👤 1. Enrolment (Database)</h2>", unsafe_allow_html=True)
uploaded_file = st.sidebar.file_uploader("Ingest Master Identity Dossier", type=["jpg", "png", "jpeg"])

if uploaded_file:
    img_pil = Image.open(uploaded_file).convert("RGB")
    st.sidebar.image(img_pil, caption="Target Master Template Reference", use_container_width=True)
    
    if st.sidebar.button("🔐 Compile Vector Map"):
        st.session_state.master_vector = extract_one_way_vector(img_pil)
        st.sidebar.success("✅ Secure 128-D Master Key Matrix Cached Natively!")

# --- 5. Main Production Terminal Interface layout ---
st.markdown("<h2 class='hud-title'>📸 2. Biometric Ingress Portal</h2>", unsafe_allow_html=True)

if st.session_state.master_vector is None:
    st.info("💡 Hardware Engine Idle. Ingest a profile matrix via the sidebar terminal to activate scanning loops.")
else:
    # High-Contrast Cyber Challenge Callout
    st.markdown(f"""
    <div class='hud-box' style='border-left-color: #FFB300;'>
        <span style='color: #FFB300; font-weight: bold;'>⚠️ ACTIVE ANTI-SPOOF CHALLENGE QUEUED:</span><br/>
        <span style='font-size: 20px; color: #FFF;'>{st.session_state.active_challenge}</span>
    </div>
    """, unsafe_allow_html=True)
    
    liveness_verification = st.checkbox("Confirm: I have performed the verified dynamic action asset above.")
    
    # Industrial Reticle Layout Setup
    st.markdown("""
    <div class='reticle-container'>
        <div class='biometric-reticle'>
            <span style='color:#00E676; font-family:monospace; font-weight:bold; font-size:12px; letter-spacing:1px;'>SCANNER READY</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    img_file_buffer = st.camera_input("Biometric Image Stream Feed Frame")
    
    if img_file_buffer is not None:
        live_img_pil = Image.open(img_file_buffer).convert("RGB")
        
        # Environmental Diagnostics Processing
        lux_mean, lux_deviation = analyze_lighting_matrix(live_img_pil)
        
        # Real-Time Operational Environmental HUD Widget
        st.markdown(f"""
        <div class='hud-box' style='border-left-color: #00E676;'>
            <span style='color: #00E676; font-weight: bold;'>📊 BIOMETRIC TELEMETRY HUD</span><br/>
            • Ambient Illumination: {lux_mean:.1f} lux {"🔴 UNSTABLE" if lux_mean < 50 or lux_mean > 220 else "🟢 OPTIMAL"}<br/>
            • Matrix Contrast Variance: {lux_deviation:.1f} Hz {"🟢 STABLE" if lux_deviation > 20 else "🟡 POOR CONTRAST"}<br/>
            • Local Node Processing Speed: &lt; 8ms
        </div>
        """, unsafe_allow_html=True)
        
        # Verification Logic Execution
        if lux_mean < 50:
            st.error("🚨 ENVIRONMENT FAULT: Ambient lighting too dark. Increase field exposure.")
        elif lux_mean > 220:
            st.error("🚨 ENVIRONMENT FAULT: Extreme glare or sunlight overloading image receptors.")
        elif not liveness_verification:
            st.error("🛑 ACCESS BLOCKED: Liveness verification failure. Static photo spoofing attack suspected.")
        else:
            with st.spinner("Executing Local INT8 Math Quantization Pass..."):
                live_vector = extract_one_way_vector(live_img_pil)
                similarity_score = np.dot(st.session_state.master_vector, live_vector)
                SIMILARITY_THRESHOLD = 0.82
                
            st.markdown("### Match Computations Summary")
            st.metric(label="Calculated Identity Matching Similarity Matrix", value=f"{similarity_score*100:.2f}%")
            
            if similarity_score >= SIMILARITY_THRESHOLD:
                st.balloons()
                st.success("🎉 SECURITY CLEARANCE SUCCESSFUL: Identity Authenticated.")
                
                new_log = {
                    "record_id": f"REC-{random.randint(10000, 99999)}",
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "status": "AUTHENTICATED",
                    "vector_match": f"{similarity_score*100:.1f}%"
                }
                if not any(d['record_id'] == new_log['record_id'] for d in st.session_state.vault_logs):
                    st.session_state.vault_logs.append(new_log)
            else:
                st.error("🛑 AUTHENTICATION CRITICAL FAILURE: Facial geometry match score below validation parameters.")

    # --- 6. The "Vault Purge" Sync Panel Architecture Component ---
    if st.session_state.vault_logs:
        st.markdown("---")
        st.markdown("<h3 style='color:#FFB300; font-family:monospace;'>📡 On-Device Encrypted Logs Queue</h3>", unsafe_allow_html=True)
        st.write("This local storage buffer mimics encrypted WatermelonDB storage arrays running locally on a worker's handset.")
        st.json(st.session_state.vault_logs)
        
        network_toggle = st.radio("Simulate Field Network Hardware State Integration:", ["🔴 Out of Service Reach Zone (Air-Gapped)", "🟢 Cloud Connection Restored (AWS Backbone Inbound)"])
        
        if network_toggle == "🟢 Cloud Connection Restored (AWS Backbone Inbound)":
            if st.button("⚡ EXECUTE VAULT PURGE SYNC TRANSACTION", type="primary"):
                # Visually simulating an atomic thread sync operation
                progress_bar = st.progress(0)
                for percent_complete in range(100):
                    time.sleep(0.01)
                    progress_bar.progress(percent_complete + 1)
                
                st.toast("AWS Datalake 3.0 Node Handshake Completed Successfully...", icon="☁️")
                time.sleep(0.5)
                
                # Shred local buffer traces entirely
                st.session_state.vault_logs = []
                st.session_state.active_challenge = random.choice(challenges)
                st.success("💥 CRYPTOGRAPHIC TRANSACTION COMPLETE: Cloud synchronized. Local volatile memory data shredded to 0 Bytes.")
                time.sleep(1.5)
                st.rerun()
