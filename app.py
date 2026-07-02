import streamlit as st
import groq
import json
import os
from database import customers, complaints, ticket_counter

client = groq.Groq(api_key="YOUR_API_KEY")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "customer" not in st.session_state:
    st.session_state.customer = None

def get_ai_response(customer_message, customer_data):
    prompt = f"""
You are an Airtel customer support AI agent.

Current customer data:
{json.dumps(customer_data, indent=2)}

You can help with:
1. FAILED RECHARGE - money deducted but recharge not applied, apologize and say refund in 3-5 business days
2. BILLING DISPUTE - explain charges from billing history
3. NETWORK COMPLAINT - acknowledge, give 24-48 hour resolution timeline
4. ESCALATION - complex issues, summarize context for human agent

Always address customer by name. Be empathetic and specific.

Customer message: {customer_message}
"""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# Page config
st.set_page_config(
    page_title="Airtel AI Support",
    page_icon="📱",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background-color: #f5f5f5;
    }

     .stApp p, .stApp div, .stMarkdown p {
    color: #1a1a1a !important;
    }

    [data-testid="stChatMessage"] p {
    color: #1a1a1a !important;
    }

    [data-testid="stChatMessageContent"] p {
    color: #1a1a1a !important;
    }
    
    /* Header */
    .airtel-header {
        background: linear-gradient(135deg, #E40000 0%, #C00000 100%);
        padding: 20px 30px;
        border-radius: 12px;
        margin-bottom: 24px;
        display: flex;
        align-items: center;
        gap: 16px;
    }
    .airtel-header h1 {
        color: white;
        margin: 0;
        font-size: 26px;
        font-weight: 700;
        letter-spacing: 0.5px;
    }
    .airtel-header p {
        color: rgba(255,255,255,0.85);
        margin: 4px 0 0 0;
        font-size: 14px;
    }
    
    /* Login card */
    .login-card {
        background: white;
        border-radius: 16px;
        padding: 40px;
        max-width: 460px;
        margin: 40px auto;
        box-shadow: 0 4px 24px rgba(0,0,0,0.08);
        text-align: center;
    }
    .login-card h2 {
        color: #1a1a1a;
        margin-bottom: 8px;
    }
    .login-card p {
        color: #666;
        margin-bottom: 24px;
        font-size: 14px;
    }
    
    /* Demo credentials */
    .demo-credentials {
        background: #fff8e1;
        border: 1px solid #ffe082;
        border-radius: 8px;
        padding: 12px 16px;
        margin-top: 16px;
        text-align: left;
        font-size: 13px;
        color: #555;
    }
    .demo-credentials strong {
        color: #333;
    }
    
    /* Account card */
    .account-card {
        background: white;
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 16px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    }
    
    /* Warning badge */
    .warning-badge {
        background: #fff3cd;
        border: 1px solid #ffc107;
        border-radius: 8px;
        padding: 8px 14px;
        font-size: 13px;
        color: #856404;
        margin-bottom: 12px;
    }
    
    /* Chat container */
    .chat-container {
        background: white;
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        min-height: 400px;
    }
    
    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Button styling */
    .stButton > button {
        background: #E40000;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 24px;
        font-weight: 600;
        width: 100%;
    }
    .stButton > button:hover {
        background: #C00000;
        color: white;

    .stChatMessage p {
    color: #1a1a1a !important;
    }

    
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="airtel-header">
    <div>
        <h1>Airtel AI Support</h1>
        <p>Intelligent support — we don't just talk, we execute</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### About This Agent")
    st.markdown("""
    This AI support agent handles the most common Airtel customer issues autonomously:
    
    - Failed recharges & refunds
    - Billing disputes
    - Network complaints
    - Complex escalations
    
    Built to simulate how **Commotion's agentic AI** works in enterprise telecom deployments.
    """)
    st.divider()
    st.markdown("### What It Can Do")
    st.markdown("""
    **Resolves autonomously:**
    - Failed recharge → initiates refund
    - Billing dispute → explains from account history
    - Network issue → raises ticket with timeline
    
    **Escalates intelligently:**
    - Summarizes full context for human agent
    - Customer never repeats themselves
    """)
    st.divider()
    st.markdown("Built by **Shiva** | [GitHub](#)", unsafe_allow_html=True)

# Main content
if not st.session_state.customer:
    st.markdown("""
    <div class="login-card">
        <h2>Welcome to Airtel Support</h2>
        <p>Enter your registered mobile number to get started</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        phone = st.text_input("Mobile Number", placeholder="Enter 10-digit number")
        if st.button("Start Chat"):
            customer = customers.get(phone)
            if customer:
                st.session_state.customer = customer
                st.session_state.customer["phone"] = phone
                st.rerun()
            else:
                st.error("Number not found. Use the demo credentials below.")
        
        st.markdown("""
        <div class="demo-credentials">
            <strong>Demo credentials:</strong><br>
            9876543210 — Rahul Sharma (failed recharge case)<br>
            9123456780 — Priya Patel (low data + network complaint)
        </div>
        """, unsafe_allow_html=True)

else:
    customer = st.session_state.customer
    
    col1, col2 = st.columns([2, 1])
    
    with col2:
        # Account summary card
        data_remaining = customer.get("data_remaining", "N/A")
        validity = customer.get("validity", "N/A")
        
        st.markdown(f"""
        <div class="account-card">
            <strong>{customer['name']}</strong><br>
            <small style="color:#666">{customer['phone']}</small><br><br>
            <strong>Plan:</strong> {customer['plan']}<br>
            <strong>Data:</strong> {data_remaining}<br>
            <strong>Validity:</strong> {validity}
        </div>
        """, unsafe_allow_html=True)
        
        # Low data warning
        if data_remaining == "0 GB":
            st.markdown("""
            <div class="warning-badge">
                Data exhausted. Consider recharging.
            </div>
            """, unsafe_allow_html=True)
        
        if st.button("End Session"):
            st.session_state.messages = []
            st.session_state.customer = None
            st.rerun()
    
    with col1:
        st.markdown(f"#### Hi {customer['name']}, how can I help you today?")
        
        # Chat messages
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])
        
        user_input = st.chat_input("Type your issue here...")
        
        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.write(user_input)
            with st.chat_message("assistant"):
                with st.spinner(""):
                    response = get_ai_response(user_input, customer)
                    st.write(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
