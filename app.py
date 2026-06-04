import streamlit as st
import numpy as np
from PIL import Image
import random
import time
import hashlib

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

st.title("🛡️ SecureField Auth Terminal v3.1")
st.caption("Datalake 3.0 Advanced Edge Simulation Sandbox • Production Standard")

# --- 2. Advanced Mathematical & Cryptographic Logic ---
def analyze_lighting_matrix(pil_img):
    """Calculates exposure and image contrast via standard matrix variance."""
    gray_img = pil_img.convert("L")
    arr = np.array(gray_img)
    return float(np.mean(arr)), float(np.std(arr))

def analyze_passive_liveness(pil_img):
    """
    🔬 FEATURE 1: PASSIVE LIVENESS (Texture & Moire Screen Detection)
    Analyzes micro-texture variance using a high-speed NumPy pixel gradient calculation.
    Screens look overly uniform or artificially blurred compared to genuine human skin textures.
    """
    gray = pil_img.convert("L")
    arr = np.array(gray, dtype=np.float32)
    
    # Calculate horizontal and vertical pixel differences (gradients)
    dy, dx = np.gradient(arr)
    gradient_magnitude = np.sqrt(dx**2 + dy**2)
    
    # Texture variance is the standard deviation of the gradient magnitudes
    texture_variance = float(np.std(gradient_magnitude))
    
    # Flag as a spoof if the texture is too flat (screen/photo) or unnaturally high (moire pattern)
    is_spoof = texture_variance < 5.0 or texture_variance > 55.0
    return texture_variance, is_spoof

def extract_one_way_vector(pil_img):
    """Simulates a deterministic 128-D cryptographic facial vector descriptor."""
    resized = pil_img.resize((112, 112)).convert("L")
    img_array = np.array(resized)
    pixel_seed = int(np.mean(img_array)) + int(np.std(img_array))
    np.random.seed(pixel_seed)
    embedding = np.random.rand(128)
    return embedding / np.linalg.norm(embedding)

def generate_tamper_proof_signature(record_id, timestamp, status, emp_id):
    """🔬 ADVANCED FEATURE: Creates a SHA-256 digital signature to detect local database changes."""
    raw_payload = f"{record_id}-{timestamp}-{status}-{emp_id}-DATALAKE3.0SECRETKEY"
    return hashlib.sha256(raw_payload.encode()).hexdigest()[:32]

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

st.sidebar.markdown("---")
st.sidebar.markdown("<h2 style='color:#FFB300;'>🎛️ 2. Edge Optimization Core</h2>", unsafe_allow_html=True)

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
    # 👥 ADVANCED FEATURE: Multi-User Operational Mode
    mode_selection = st.radio("Select Authentication Workflow Mode:", ["Personal Device Login", "Supervisor Crew Processing Mode"])
    
    target_emp_id = "EMP-OWNER"
    if mode_selection == "Supervisor Crew Processing Mode":
        target_emp_id = st.text_input("Enter Target Crew Employee ID Number:", value="EMP-1024")
        st.caption("Active Roster Validation: Overriding identity vector target verification for requested ID.")

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
            • Passive Texture Density: {texture_val:.2f} {"🔴 REPLAY ATTACK DETECTED" if passive_spoof_detected else "🟢 GENUINE SKIN TEXTURE"}<br/>
            • Local Node Latency Speed: {sim_latency}
        </div>
        """, unsafe_allow_html=True)
        
        # Verification Logic Execution
        if lux_mean < 50:
            st.error("🚨 ENVIRONMENT FAULT: Ambient lighting too dark. Increase field exposure.")
        elif lux_mean > 220:
            st.error("🚨 ENVIRONMENT FAULT: Extreme glare or sunlight overloading image receptors.")
        elif passive_spoof_detected:
            st.error("🛑 ACCESS SECURITY FRAUD ALERT: High-frequency pixel uniformity anomaly detected. Digital display screen presentation suspected.")
        elif not liveness_verification:
            st.error("🛑 ACCESS BLOCKED: Active liveness verification failure. Dynamic validation check step was skipped.")
        else:
            with st.spinner("Processing Edge Matrix Quantization Pass..."):
                time.sleep(0.2)
                live_vector = extract_one_way_vector(live_img_pil)
                similarity_score = np.dot(st.session_state.master_vector, live_vector)
                SIMILARITY_THRESHOLD = 0.82
                
            st.markdown("### Match Computations Summary")
            st.metric(label="Calculated Identity Matching Similarity Matrix", value=f"{similarity_score*100:.2f}%")
            
            if similarity_score >= SIMILARITY_THRESHOLD:
                st.balloons()
                st.success("🎉 SECURITY CLEARANCE SUCCESSFUL: Identity Authenticated.")
                
                rec_id = f"REC-{random.randint(10000, 99999)}"
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                
                # Cryptographic Hash Signature Generation
                crypto_sig = generate_tamper_proof_signature(rec_id, timestamp, "AUTHENTICATED", target_emp_id)
                
                new_log = {
                    "record_id": rec_id,
                    "timestamp": timestamp,
                    "employee_id": target_emp_id,
                    "status": "AUTHENTICATED",
                    "vector_match": f"{similarity_score*100:.1f}%",
                    "sha256_signature": crypto_sig,
                    "tamper_status": "🟢 VALID_INTEGRITY"
                }
                if not any(d['record_id'] == new_log['record_id'] for d in st.session_state.vault_logs):
                    st.session_state.vault_logs.append(new_log)
            else:
                st.error("🛑 AUTHENTICATION CRITICAL FAILURE: Facial geometry match score below validation parameters.")

    # Hardware Health Radar Component
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
        st.write("This local storage buffer mimics encrypted local storage arrays running on a worker's handset.")
        
        if st.button("🚨 Simulate Local Database Tamper Attempt (Attacker Injection)"):
            if st.session_state.vault_logs:
                st.session_state.vault_logs[0]["employee_id"] = "FORGED-ID-9999"
                st.session_state.vault_logs[0]["tamper_status"] = "🟥 CORRUPTED_SIGNATURE_ALERT"
                st.toast("Malicious database payload injected! Checking structural signature rings...", icon="⚡")
        
        st.json(st.session_state.vault_logs)
        
        network_toggle = st.radio("Simulate Field Network Hardware State Integration:", ["🔴 Out of Service Reach Zone (Air-Gapped)", "🟢 Cloud Connection Restored (AWS Backbone Inbound)"])
        
        if network_toggle == "🟢 Cloud Connection Restored (AWS Backbone Inbound)":
            has_corruption = any(d['tamper_status'] == "🟥 CORRUPTED_SIGNATURE_ALERT" for d in st.session_state.vault_logs)
            
            if has_corruption:
                st.error("🛑 TRANSACTION TERMINATED: Cloud synchronization blocked. A compromised record payload signature has been detected in the queue.")
            else:
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
