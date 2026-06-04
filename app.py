import streamlit as st
import numpy as np
from PIL import Image
import random
import time
import hashlib

# --- 1. Premium Industrial Cyber Global Styling ---
st.set_page_config(page_title="SecureField Auth Suite", layout="wide")

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
        width: 200px;
        height: 200px;
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
    .metric-card {
        background-color: #161D2A;
        padding: 15px;
        border-radius: 4px;
        border: 1px solid #232D3F;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. Heavy-Duty State & Session Database Initialization ---
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
    # Populate with mock historical dummy data for the Analytics Dashboard to look premium instantly
    st.session_state.vault_logs = [
        {"record_id": "REC-4412", "timestamp": "2026-06-04 08:30:12", "employee_id": "EMP-102", "status": "AUTHENTICATED", "vector_match": "89.4%", "tamper_status": "🟢 VALID_INTEGRITY", "model_used": "Quantized INT8 (Our Build)"},
        {"record_id": "REC-8921", "timestamp": "2026-06-04 09:15:45", "employee_id": "EMP-304", "status": "AUTHENTICATED", "vector_match": "94.1%", "tamper_status": "🟢 VALID_INTEGRITY", "model_used": "Quantized INT8 (Our Build)"},
        {"record_id": "REC-1150", "timestamp": "2026-06-04 11:02:19", "employee_id": "EMP-088", "status": "AUTHENTICATED", "vector_match": "86.7%", "tamper_status": "🟢 VALID_INTEGRITY", "model_used": "Quantized INT8 (Our Build)"}
    ]
if "similarity_threshold" not in st.session_state:
    st.session_state.similarity_threshold = 0.82
if "model_format" not in st.session_state:
    st.session_state.model_format = "Quantized INT8 (Our Build)"

# --- 3. Core Math Matrix Functions ---
def analyze_lighting_matrix(pil_img):
    gray_img = pil_img.convert("L")
    arr = np.array(gray_img)
    return float(np.mean(arr)), float(np.std(arr))

def analyze_passive_liveness(pil_img):
    """Analyzes micro-texture variance using a high-speed NumPy pixel gradient calculation."""
    gray = pil_img.convert("L")
    arr = np.array(gray, dtype=np.float32)
    dy, dx = np.gradient(arr)
    gradient_magnitude = np.sqrt(dx**2 + dy**2)
    texture_variance = float(np.std(gradient_magnitude))
    is_spoof = texture_variance < 5.0 or texture_variance > 55.0
    return texture_variance, is_spoof

def extract_one_way_vector(pil_img):
    resized = pil_img.resize((112, 112)).convert("L")
    img_array = np.array(resized)
    pixel_seed = int(np.mean(img_array)) + int(np.std(img_array))
    np.random.seed(pixel_seed)
    embedding = np.random.rand(128)
    return embedding / np.linalg.norm(embedding)

def generate_tamper_proof_signature(record_id, timestamp, status, emp_id):
    raw_payload = f"{record_id}-{timestamp}-{status}-{emp_id}-DATALAKE3.0SECRETKEY"
    return hashlib.sha256(raw_payload.encode()).hexdigest()[:32]


# --- 4. NAVIGATION PANEL SIDEBAR SYSTEM ---
st.sidebar.markdown("<h1 style='color:#00E676; font-family:monospace;'>🛸 SECUREFIELD CONTROL</h1>", unsafe_allow_html=True)
current_screen = st.sidebar.radio("Navigation View Portal:", ["📸 1. Authentication Gate", "📊 2. Analytics Insight Vault", "🛡️ 3. Security Config Matrix"])

st.sidebar.markdown("---")

# Global Settings managed via Navigation Bar
st.sidebar.markdown("<h3 style='color:#FFB300;'>👤 Global Identity Ingestion</h3>", unsafe_allow_html=True)
uploaded_file = st.sidebar.file_uploader("Ingest Master Identity Dossier", type=["jpg", "png", "jpeg"])

if uploaded_file:
    img_pil = Image.open(uploaded_file).convert("RGB")
    st.sidebar.image(img_pil, caption="Current System Reference Profile", width=160)
    if st.sidebar.button("🔐 Re-compile Identity Vector"):
        st.session_state.master_vector = extract_one_way_vector(img_pil)
        st.sidebar.success("✅ Master Key Matrix Updated Locally!")


# --- SCREEN 1: THE AUTHENTICATION GATE TERMINAL ---
if current_screen == "📸 1. Authentication Gate":
    st.markdown("<h2 class='hud-title'>📸 Biometric Field Ingress Portal</h2>", unsafe_allow_html=True)
    st.write("Offline gate hardware terminal simulation engine.")
    
    if st.session_state.master_vector is None:
        st.info("💡 Hardware Engine Idle. Ingest a template photo via the sidebar navigation panel to wake system loops.")
    else:
        mode_selection = st.radio("Select Authentication Workflow Mode:", ["Personal Device Login", "Supervisor Crew Processing Mode"])
        target_emp_id = "EMP-OWNER"
        if mode_selection == "Supervisor Crew Processing Mode":
            target_emp_id = st.text_input("Enter Target Crew Employee ID Number:", value="EMP-1024")
        
        st.markdown(f"""
        <div class='hud-box' style='border-left-color: #FFB300;'>
            <span style='color: #FFB300; font-weight: bold;'>⚠️ ACTIVE ANTI-SPOOF CHALLENGE QUEUED:</span><br/>
            <span style='font-size: 20px; color: #FFF;'>{st.session_state.active_challenge}</span>
        </div>
        """, unsafe_allow_html=True)
        
        liveness_verification = st.checkbox("Confirm: I have performed the verified dynamic action asset above.")
        
        st.markdown("<div class='reticle-container'><div class='biometric-reticle'><span style='color:#00E676; font-family:monospace; font-weight:bold; font-size:11px;'>SCANNER WAITING</span></div></div>", unsafe_allow_html=True)
        img_file_buffer = st.camera_input("Biometric Image Stream Feed Frame")
        
        if img_file_buffer is not None:
            live_img_pil = Image.open(img_file_buffer).convert("RGB")
            lux_mean, lux_deviation = analyze_lighting_matrix(live_img_pil)
            texture_val, passive_spoof_detected = analyze_passive_liveness(live_img_pil)
            
            # Simulated Latency depending on format settings
            sim_latency = "120 ms" if "INT8" in st.session_state.model_format else ("410 ms" if "Float16" in st.session_state.model_format else "840 ms")
            
            st.markdown(f"""
            <div class='hud-box' style='border-left-color: #00E676;'>
                <span style='color: #00E676; font-weight: bold;'>📊 LIVE TELEMETRY</span><br/>
                • Illumination Exposure: {lux_mean:.1f} lux<br/>
                • Texture Density Check: {texture_val:.2f} {"🔴 SPOOF SUSPECTED" if passive_spoof_detected else "🟢 PHYSICAL FACE SKIN"}<br/>
                • Execution Compression Delay: {sim_latency}<br/>
                • Core Processing: Active Local Air-Gapped Thread
            </div>
            """, unsafe_allow_html=True)
            
            if passive_spoof_detected:
                st.error("🛑 ACCESS SECURITY FRAUD ALERT: High-frequency digital screen presentation suspected.")
            elif not liveness_verification:
                st.error("🛑 ACCESS BLOCKED: Liveness validation check step was skipped.")
            else:
                live_vector = extract_one_way_vector(live_img_pil)
                similarity_score = np.dot(st.session_state.master_vector, live_vector)
                
                st.metric(label="Calculated Spatial Similarity Rating Match", value=f"{similarity_score*100:.2f}%")
                
                if similarity_score >= st.session_state.similarity_threshold:
                    st.balloons()
                    st.success("🎉 SECURITY CLEARANCE SUCCESSFUL: Identity Authenticated.")
                    
                    rec_id = f"REC-{random.randint(10000, 99999)}"
                    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                    crypto_sig = generate_tamper_proof_signature(rec_id, timestamp, "AUTHENTICATED", target_emp_id)
                    
                    new_log = {
                        "record_id": rec_id,
                        "timestamp": timestamp,
                        "employee_id": target_emp_id,
                        "status": "AUTHENTICATED",
                        "vector_match": f"{similarity_score*100:.1f}%",
                        "sha256_signature": crypto_sig,
                        "tamper_status": "🟢 VALID_INTEGRITY",
                        "model_used": st.session_state.model_format
                    }
                    if not any(d['record_id'] == new_log['record_id'] for d in st.session_state.vault_logs):
                        st.session_state.vault_logs.append(new_log)
                else:
                    st.error("🛑 AUTHENTICATION CRITICAL FAILURE: Facial metrics do not match master credentials.")


# --- SCREEN 2: ANALYTICS INSIGHT VAULT DASHBOARD ---
elif current_screen == "📊 2. Analytics Insight Vault":
    st.markdown("<h2 class='hud-title'>📊 Business Intelligence & Attendance Insight Vault</h2>", unsafe_allow_html=True)
    st.write("Real-time local cluster analytics for corporate tracking diagnostics.")
    
    # KPIs Rows
    total_scans = len(st.session_state.vault_logs)
    tamper_alerts = sum(1 for d in st.session_state.vault_logs if d["tamper_status"] != "🟢 VALID_INTEGRITY")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"<div class='metric-card'><span style='color:#00E676;font-size:14px;font-family:monospace;'>TOTAL FIELD PROCESSING RUNS</span><br/><b style='font-size:32px;'>{total_scans}</b></div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='metric-card'><span style='color:#FFB300;font-size:14px;font-family:monospace;'>NETWORK ARCHIVE MODE</span><br/><b style='font-size:32px;'>100% OFFLINE</b></div>", unsafe_allow_html=True)
    with c3:
        st.markdown(f"<div class='metric-card'><span style='color:#FF1744;font-size:14px;font-family:monospace;'>INTEGRITY TAMPER BREACHES</span><br/><b style='font-size:32px;'>{tamper_alerts}</b></div>", unsafe_allow_html=True)
        
    st.markdown("### On-Device Cache Storage Array Logs")
    
    if st.button("🚨 Simulate Attacker Database Injection (Tamper Test Log #1)"):
        if len(st.session_state.vault_logs) > 0:
            st.session_state.vault_logs[0]["employee_id"] = "COMPROMISED-ID-99"
            st.session_state.vault_logs[0]["tamper_status"] = "🟥 CORRUPTED_SIGNATURE_ALERT"
            st.toast("Malicious structural rewrite caught!", icon="⚡")
            st.rerun()
            
    st.json(st.session_state.vault_logs)
    
    st.markdown("---")
    st.markdown("### 📡 AWS Datalake 3.0 Relaying Pipeline Core")
    network_toggle = st.radio("Field Network State Integration Link:", ["🔴 Out of Service Reach Zone (Air-Gapped)", "🟢 Cloud Connection Restored (AWS Inbound Available)"])
    
    if network_toggle == "🟢 Cloud Connection Restored (AWS Inbound Available)":
        has_corruption = any(d['tamper_status'] != "🟢 VALID_INTEGRITY" for d in st.session_state.vault_logs)
        if has_corruption:
            st.error("🛑 SYNC CRITICAL STOP: A compromised payload record signature hash breaks security parameters. Synchronization terminated.")
        else:
            if st.button("⚡ EXECUTE ATOMIC SYNC RUN & VOLATILE CACHE PURGE", type="primary"):
                pb = st.progress(0)
                for p in range(100):
                    time.sleep(0.005)
                    pb.progress(p + 1)
                st.session_state.vault_logs = []
                st.success("💥 TRANSACTION AGGREGATED: AWS Backbone update success. Local disk logs wiped clean down to 0 Bytes.")
                st.rerun()


# --- SCREEN 3: SECURITY CONFIGURATION MATRIX ---
elif current_screen == "🛡️ 3. Security Config Matrix":
    st.markdown("<h2 class='hud-title'>🛡️ System Operational Configuration Matrix</h2>", unsafe_allow_html=True)
    st.write("Tune edge algorithms and monitor mobile system telemetry properties.")
    
    st.markdown("### 🎛️ Algorithmic Calibration Parameters")
    
    # Feature adjustment options
    st.session_state.similarity_threshold = st.slider(
        "Biometric Vector Cosine Match Match Threshold Strictness:",
        min_value=0.50, max_value=0.98, value=st.session_state.similarity_threshold, step=0.01
    )
    st.caption("Lower numbers accommodate dirt/sweat field distortions; higher numbers tighten defense constraints against high-res masks.")
    
    st.session_state.model_format = st.selectbox(
        "Edge Neural Engine Framework Compilation Weight Format Profile:",
        ["Standard Float32 (84.2 MB Footprint)", "Optimized Float16 (42.1 MB Footprint)", "Quantized INT8 (Our Build) (4.6 MB Footprint)"],
        index=2
    )
    
    st.markdown("---")
    st.markdown("### 🔋 Live Mobile Handset Resource Telemetry Monitor")
    
    col_x, col_y, col_z = st.columns(3)
    with col_x:
        st.metric("Phone System Core Thermal Index", "35.8 °C", "🟢 Stable Target")
    with col_y:
        st.metric("Active Model RAM Footprint Allocation", "4.2 MB" if "INT8" in st.session_state.model_format else "78.4 MB", "Safe State")
    with col_z:
        st.metric("Active Power Draw Efficiency Rating", "1.18%/hr", "Optimal Optimization")
        
    st.info("ℹ️ System Configuration state updates execute instantly without needing internet cloud connection updates.")
