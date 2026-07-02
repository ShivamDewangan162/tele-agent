import streamlit as st
import json
from database import customers, complaints, ticket_counter

# Initialize Groq
from groq import Groq
import os
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "customer" not in st.session_state:
    st.session_state.customer = None

def get_customer(phone):
    return customers.get(phone)

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

# UI
st.title("Airtel AI Support Agent")
st.caption("Powered by Commotion-style agentic AI")

if not st.session_state.customer:
    st.subheader("Please enter your mobile number to begin")
    phone = st.text_input("Mobile Number (10 digits)")
    if st.button("Start Chat"):
        customer = get_customer(phone)
        if customer:
            st.session_state.customer = customer
            st.session_state.customer["phone"] = phone
            st.rerun()
        else:
            st.error("Number not found. Try 9876543210 or 9123456780")
else:
    customer = st.session_state.customer
    st.success(f"Welcome, {customer['name']}! How can I help you today?")

    with st.expander("Your Account"):
        st.write(f"**Plan:** {customer['plan']}")
        st.write(f"**Data Remaining:** {customer['data_remaining']}")
        st.write(f"**Validity:** {customer['validity']}")

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_input = st.chat_input("Type your issue here...")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = get_ai_response(user_input, customer)
                st.write(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

    if st.button("End Session"):
        st.session_state.messages = []
        st.session_state.customer = None
        st.rerun()
