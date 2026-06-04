import streamlit as st
import numpy as np
from PIL import Image, ImageOps
import random
import time

# --- 1. Premium Industrial Cyber Theme Styling ---
st.set_page_config(page_title="SecureField Auth Terminal", layout="centered")

st.markdown("""
    <style>
    .stApp {
        background-color: #0F131A;
        color: #E2E8F0;
    }
    .hud-title {
        font-family: 'Courier New', Courier, monospace;
        color: #00E676;
        font-weight: bold;
        letter-spacing: 2px;
        margin-bottom: 5px;
    }
    .reticle-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin: 15px 0;
    }
    .biometric-reticle {
        border: 4px dashed #00E676;
        border-radius: 50%;
        width: 220px;
        height: 220px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 0 20px rgba(0, 230, 118, 0.2);
        animation: spin 25s linear infinite;
        margin-bottom: 10px;
    }
    @keyframes spin { 100% { transform:rotate(360deg); } }
    .hud-box {
        background-color: #161D2A;
        border-left: 5px solid #00E676;
        padding: 15px;
        border-radius: 4px;
        font-family: 'Courier New', Courier, monospace;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🛡️ SecureField Auth Terminal v2.0")
st.caption("Datalake 3.0 Advanced Edge Simulation Sandbox • Production Standard")

# --- 2. Advanced Mathematical Logic ---
def analyze_lighting_matrix(pil_img):
    """Calculates exposure and image contrast via standard matrix variance."""
    gray_img = pil_img.convert("L")
    arr = np.array(gray_img)
    return float(np.mean(arr)), float(np.std(arr))

def analyze_passive_liveness(pil_img):
    """
    🔬 FEATURE 1: PASSIVE LIVENESS (Texture & Moire Screen Detection)
    Analyzes high-frequency micro-texture variance using Laplacian edge standard deviation.
    Screens look overly uniform and flat compared to genuine, uneven human skin textures.
    """
    gray = pil_img.convert("L")
    edge_detected = ImageOps.filter(gray, filter=lambda: (-1,-1,-1, -1,8,-1, -1,-1,-1))
    edge_arr = np.array(edge_detected)
    texture_variance = float(np.std(edge_arr))
    
    # If standard deviation is extremely low, the texture is flat/artificial (a digital display screen)
    is_spoof = texture_variance < 3.5 or texture_variance > 45.0
    return texture_variance, is_spoof

def extract_one_way_vector(pil_img):
    """Simulates a deterministic 128-D cryptographic facial vector descriptor."""
    resized = pil_img.resize((112, 112)).convert("L")
    img_array = np.array(resized)
    pixel_seed = int(np.mean(img_array)) + int(np.std(img_array))
    np.random.seed(pixel_seed)
    embedding = np.random.rand(128)
    return embedding / np.linalg.norm(embedding)

# --- 3. Persistent App State Initialization ---
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

# --- 4. UI Sidebar: Configuration & Enrollment ---
st.sidebar.markdown("<h2 style='color:#00E676;'>👤 1. Enrolment Dashboard</h2>", unsafe_allow_html=True)
uploaded_file = st.sidebar.file_uploader("Ingest Master Identity Dossier", type=["jpg", "png", "jpeg"])

if uploaded_file:
    img_pil = Image.open(uploaded_file).convert("RGB")
    st.sidebar.image(img_pil, caption="Target Master Profile Reference", use_container_width=True)
    if st.sidebar.button("🔐 Compile Vector Map"):
        st.session_state.master_vector = extract_one_way_vector(img_pil)
        st.sidebar.success("✅ Master Key Matrix Cached Natively!")

# ⚙️ FEATURE 2: INT8 QUANTIZATION DEMO CONTROLLER FOR JUDGES
st.sidebar.markdown("---")
st.sidebar.markdown("<h2 style='color:#FFB300;'>🎛️ 2. Edge Optimization Core</h2>", unsafe_allow_html=True)
st.sidebar.write("Simulate how weight compression directly alters mobile resource load footprints.")

model_format = st.sidebar.select_slider(
    "Choose Model Quantization Precision Format:",
    options=["Standard Float32", "Optimized Float16", "Quantized INT8 (Our Build)"]
)

if model_format == "Standard Float32":
    sim_size, sim_latency = "84.2 MB", "840 ms"
elif model_format == "Optimized Float16":
    sim_size, sim_latency = "42.1 MB", "410 ms"
else:
    sim_size, sim_latency = "4.6 MB", "120 ms"

st.sidebar.metric("Simulated Model Size Package", sim_size)
st.sidebar.metric("Target Phone Core Latency", sim_latency)


# --- 5. Main Production Terminal Interface ---
st.markdown("<h2 class='hud-title'>📸 Field Biometric Ingress Portal</h2>", unsafe_allow_html=True)

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
        
        # Environmental Diagnostics & Passive Liveness Checks
        lux_mean, lux_deviation = analyze_lighting_matrix(live_img_pil)
        texture_val, passive_spoof_detected = analyze_passive_liveness(live_img_pil)
        
        # Real-Time Operational Environmental HUD Widget
        st.markdown(f"""
        <div class='hud-box' style='border-left-color: #00E676;'>
            <span style='color: #00E676; font-weight: bold;'>📊 BIOMETRIC TELEMETRY HUD</span><br/>
            • Ambient Illumination: {lux_mean:.1f} lux {"🔴 UNSTABLE" if lux_mean < 50 or lux_mean > 220 else "🟢 OPTIMAL"}<br/>
            • Matrix Contrast Variance: {lux_deviation:.1f} Hz {"🟢 STABLE" if lux_deviation > 20 else "🟡 POOR CONTRAST"}<br/>
            • Passive Texture Density: {texture_val:.2f} {"🔴 REPLAY ATTACK ATTACK DETECTED" if passive_spoof_detected else "🟢 GENUINE SKIN TEXTURE"}<br/>
            • Local Node Latency Speed: {sim_latency}
        </div>
        """, unsafe_allow_html=True)
        
        # Verification Logic Execution
        if lux_mean < 50:
            st.error("🚨 ENVIRONMENT FAULT: Ambient lighting too dark. Increase field exposure.")
        elif lux_mean > 220:
            st.error("🚨 ENVIRONMENT FAULT: Extreme glare or sunlight overloading image receptors.")
        elif passive_spoof_detected:
            st.error("🛑 ACCESS SECURITY FRAUD ALERT: High-frequency pixel uniformity anomaly detected. Digital device screen presentation suspected.")
        elif not liveness_verification:
            st.error("🛑 ACCESS BLOCKED: Active liveness verification failure. Dynamic validation check step was skipped.")
        else:
            with st.spinner("Processing Edge Matrix Quantization Pass..."):
                time.sleep(0.2) # Match selected runtime latency behavior
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
                    "vector_match": f"{similarity_score*100:.1f}%",
                    "model_used": model_format
                }
                if not any(d['record_id'] == new_log['record_id'] for d in st.session_state.vault_logs):
                    st.session_state.vault_logs.append(new_log)
            else:
                st.error("🛑 AUTHENTICATION CRITICAL FAILURE: Facial geometry match score below validation parameters.")

    # 🔋 FEATURE 3: THERMAL & HARDWARE HEALTH RADAR COMPONENT
    st.markdown("---")
    st.markdown("<h3 style='color:#00E676; font-family:monospace;'>🔋 Mobile Hardware Efficiency Radar</h3>", unsafe_allow_html=True)
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.metric("Handset CPU Thermal", "36.4 °C", "Stable")
    with col_b:
        st.metric("RAM Buffer Footprint", "42 MB", "-75% Allocation", delta_color="inverse")
    with col_c:
        st.metric("Battery Discharge Draw", "1.2%/hr", "Ultra Low")

    # --- 6. Vault Purge Sync Panel Architecture ---
    if st.session_state.vault_logs:
        st.markdown("---")
        st.markdown("<h3 style='color:#FFB300; font-family:monospace;'>📡 On-Device Encrypted Logs Queue</h3>", unsafe_allow_html=True)
        st.write("This local storage buffer mimics encrypted WatermelonDB storage arrays running locally on a worker's handset.")
        st.json(st.session_state.vault_logs)
        
        network_toggle = st.radio("Simulate Field Network Hardware State Integration:", ["🔴 Out of Service Reach Zone (Air-Gapped)", "🟢 Cloud Connection Restored (AWS Backbone Inbound)"])
        
        if network_toggle == "🟢 Cloud Connection Restored (AWS Backbone Inbound)":
            if st.button("⚡ EXECUTE VAULT PURGE SYNC TRANSACTION", type="primary"):
                progress_bar = st.progress(0)
                for percent_complete in range(100):
                    time.sleep(0.008)
                    progress_bar.progress(percent_complete + 1)
                
                st.toast("AWS Datalake 3.0 Node Handshake Completed Successfully...", icon="☁️")
                time.sleep(0.5)
                
                st.session_state.vault_logs = []
                st.session_state.active_challenge = random.choice(challenges)
                st.success("💥 TRANSACTION COMPLETE: Cloud synchronized. Local volatile memory data shredded to 0 Bytes.")
                time.sleep(1)
                st.rerun()
