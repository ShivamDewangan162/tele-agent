import streamlit as st
import groq
import json
import os
import random
import sqlite3

client = groq.Groq(api_key=os.environ.get("GROQ_API_KEY"))

def get_customer_from_db(phone):
    conn = sqlite3.connect('airtel.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers WHERE phone = ?", (phone,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return None
    
    customer = {
        "phone": row[0],
        "name": row[1],
        "plan": row[2],
        "data_remaining": row[3],
        "validity": row[4],
        "last_recharge": row[5]
    }
    
    cursor.execute("SELECT date, amount, status, note FROM billing_history WHERE phone = ? ORDER BY date DESC", (phone,))
    billing_rows = cursor.fetchall()
    customer["billing_history"] = [
        {"date": r[0], "amount": r[1], "status": r[2], "note": r[3]} for r in billing_rows
    ]
    
    conn.close()
    return customer

if "messages" not in st.session_state:
    st.session_state.messages = []
if "customer" not in st.session_state:
    st.session_state.customer = None
if "tickets" not in st.session_state:
    st.session_state.tickets = []
if "escalated" not in st.session_state:
    st.session_state.escalated = False

def generate_ticket_id():
    return f"TKT-{random.randint(100000, 999999)}"

def detect_intent(message):
    message = message.lower()
    if any(w in message for w in ["escalate", "manager", "senior", "unacceptable", "complaint", "fed up", "frustrated"]):
        return "escalation"
    if any(w in message for w in ["recharge", "deducted", "not applied", "failed", "money gone"]):
        return "recharge"
    if any(w in message for w in ["network", "signal", "5g", "4g", "internet", "slow", "not working"]):
        return "network"
    if any(w in message for w in ["bill", "charged", "charge", "amount", "deduction", "twice"]):
        return "billing"
    return "general"

def get_ai_response(customer_message, customer_data, intent):
    if intent == "escalation":
        billing = customer_data.get("billing_history", [])
        failed = [b for b in billing if b.get("status") == "failed"]
        failed_summary = f"Failed recharge on {failed[0]['date']} for Rs.{failed[0]['amount']}" if failed else "No failed recharges"

        escalation_summary = f"""
ESCALATION SUMMARY
==================
Customer: {customer_data['name']}
Phone: {customer_data.get('phone', 'N/A')}
Plan: {customer_data['plan']}
Data Remaining: {customer_data['data_remaining']}
Validity: {customer_data['validity']}
Billing Issue: {failed_summary}
Chat History: {len(st.session_state.messages)} messages exchanged
Urgency: HIGH
==================
"""
        return "ESCALATE", escalation_summary

    prompt = f"""
You are an Airtel customer support AI agent.

Current customer data:
{json.dumps(customer_data, indent=2)}

Intent detected: {intent}

You can help with:
1. FAILED RECHARGE - money deducted but recharge not applied, apologize and say refund in 3-5 business days. Generate a refund reference.
2. BILLING DISPUTE - explain charges clearly from billing history
3. NETWORK COMPLAINT - acknowledge, give 24-48 hour resolution timeline, mention a ticket will be raised
4. GENERAL - answer helpfully based on account data

Always address customer by name. Be empathetic, specific, and concise.

Customer message: {customer_message}
"""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return "RESPOND", response.choices[0].message.content

st.set_page_config(page_title="Airtel AI Support", page_icon="📱", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #f5f5f5; }
    .stApp p, .stApp div, .stMarkdown p { color: #1a1a1a !important; }
    [data-testid="stChatMessage"] p { color: #1a1a1a !important; }
    [data-testid="stChatMessageContent"] p { color: #1a1a1a !important; }
    .airtel-header {
        background: linear-gradient(135deg, #E40000 0%, #C00000 100%);
        padding: 20px 30px; border-radius: 12px; margin-bottom: 24px;
    }
    .airtel-header h1 { color: white; margin: 0; font-size: 26px; font-weight: 700; }
    .airtel-header p { color: rgba(255,255,255,0.85); margin: 4px 0 0 0; font-size: 14px; }
    .account-card {
        background: white; border-radius: 12px; padding: 16px 20px;
        margin-bottom: 16px; box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    }
    .warning-badge {
        background: #fff3cd; border: 1px solid #ffc107; border-radius: 8px;
        padding: 8px 14px; font-size: 13px; color: #856404; margin-bottom: 12px;
    }
    .ticket-card {
        background: #e8f5e9; border: 1px solid #4caf50; border-radius: 10px;
        padding: 14px 18px; margin: 10px 0; font-size: 13px;
    }
    .escalation-card {
        background: #fff3e0; border: 2px solid #ff9800; border-radius: 10px;
        padding: 16px 20px; margin: 10px 0; font-size: 13px; white-space: pre-wrap;
    }
    .demo-credentials {
        background: #fff8e1; border: 1px solid #ffe082; border-radius: 8px;
        padding: 12px 16px; margin-top: 16px; font-size: 13px; color: #555;
    }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;}
    .stButton > button {
        background: #E40000; color: white; border: none;
        border-radius: 8px; padding: 10px 24px; font-weight: 600; width: 100%;
    }
    .stButton > button:hover { background: #C00000; color: white; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="airtel-header">
    <div>
        <h1>Airtel AI Support</h1>
        <p>Intelligent support</p>
    </div>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### About This Agent")
    st.markdown("""
    This AI support agent handles the most common Airtel customer issues autonomously:
    - Failed recharges & refunds
    - Billing disputes
    - Network complaints
    - Complex escalations
    
    Account data is queried live from a SQLite database.
    """)
    st.divider()
    st.markdown("Built by **Shiva** | IIT Bombay CTARA")

    if st.session_state.tickets:
        st.divider()
        st.markdown("### Active Tickets")
        for t in st.session_state.tickets:
            st.markdown(f"Ticket `{t['id']}` -- {t['type']}")

if not st.session_state.customer:
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("""
        <div style="background:white;border-radius:16px;padding:40px;box-shadow:0 4px 24px rgba(0,0,0,0.08);text-align:center;">
            <h2 style="color:#1a1a1a">Welcome to Airtel Support</h2>
            <p style="color:#666">Enter your registered mobile number to get started</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("")
        phone = st.text_input("Mobile Number", placeholder="Enter 10-digit number")
        if st.button("Start Chat"):
            customer = get_customer_from_db(phone)
            if customer:
                st.session_state.customer = customer
                st.rerun()
            else:
                st.error("Number not found. Use demo credentials below.")
        st.markdown("""
        <div class="demo-credentials">
            <strong>Demo credentials:</strong><br>
            9876543210 -- Rahul Sharma (failed recharge case)<br>
            9123456780 -- Priya Patel (low data + network complaint)<br>
            9876543212 -- Amit Verma
        </div>
        """, unsafe_allow_html=True)

else:
    customer = st.session_state.customer
    col1, col2 = st.columns([2, 1])

    with col2:
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

        if data_remaining == "0 GB":
            st.markdown('<div class="warning-badge">Data exhausted. Consider recharging.</div>', unsafe_allow_html=True)

        if st.button("End Session"):
            st.session_state.messages = []
            st.session_state.customer = None
            st.session_state.tickets = []
            st.session_state.escalated = False
            st.rerun()

    with col1:
        st.markdown(f"#### Hi {customer['name']}, how can I help you today?")

        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                if msg.get("type") == "ticket":
                    st.markdown(f'<div class="ticket-card">Ticket Raised<br>{msg["content"]}</div>', unsafe_allow_html=True)
                elif msg.get("type") == "escalation":
                    st.markdown(f'<div class="escalation-card">Escalation Summary for Human Agent<br><br>{msg["content"]}</div>', unsafe_allow_html=True)
                else:
                    st.write(msg["content"])

        if not st.session_state.escalated:
            user_input = st.chat_input("Type your issue here...")

            if user_input:
                st.session_state.messages.append({"role": "user", "content": user_input})
                intent = detect_intent(user_input)
                action, response = get_ai_response(user_input, customer, intent)

                if action == "ESCALATE":
                    ticket_id = generate_ticket_id()
                    st.session_state.tickets.append({"id": ticket_id, "type": "Escalation"})
                    st.session_state.escalated = True
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": f"I understand your frustration. I'm escalating this to a senior agent right away. Your escalation ticket is {ticket_id}.",
                        "type": "text"
                    })
                    st.session_state.messages.append({"role": "assistant", "content": response, "type": "escalation"})
                else:
                    if intent == "network":
                        ticket_id = generate_ticket_id()
                        st.session_state.tickets.append({"id": ticket_id, "type": "Network Complaint"})
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": f"Ticket ID: {ticket_id}\nType: Network Complaint\nStatus: Open\nEstimated Resolution: 24-48 hours",
                            "type": "ticket"
                        })
                    st.session_state.messages.append({"role": "assistant", "content": response, "type": "text"})

                st.rerun()
        else:
            st.info("This conversation has been escalated to a senior agent. They will contact you within 2 hours.")
