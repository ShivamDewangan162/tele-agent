# Telecom AI Support Agent

An AI support agent that doesn't just answer telecom customer queries but also resolves them. When a problem needs human intervention, it seamlessly hands over the case with a complete summary, so customers don't have to repeat themselves.

[Live app](https://tele-agent-fde.streamlit.app)

Demo login: 9876543210

## What it does

- Failed recharge : Detects it in billing history, confirms refund + timeline
- Billing dispute : Explains charges from actual account data
- Network complaint : Raises a support ticket with an ID, gives resolution timeline
- Escalation : Raises an escalation ticket and auto-generates a full context summary for the human agent so that customer doesn't need to repeat themselves

## How it works

1. Customer logs in with their registered mobile number
2. The message is classified by intent, recharge, billing, network, or escalation
3. For most queries, an LLM (Llama 3.3 70B via Groq) generates a response grounded in the customer's real account data
4. For escalations, the summary is built with plain logic instead of the LLM, this keeps billing figures and dates exact.
5. Network complaints and escalations automatically generate a ticket ID

## Path to voice AI

Although this project uses a text-based interface, the underlying architecture is designed to be voice-ready. The core reasoning layer, including intent detection, account lookup, response generation, ticket creation, and escalation logic, is independent of the input channel. Supporting voice would simply require adding speech-to-text for user input and text-to-speech for responses, while the agent's decision making and business logic would remain unchanged.

## Stack
Streamlit, Groq (Llama 3.3 70B), Python

## Limitation
This is a simulation mock database instead of a live CRM, keyword-based intent detection instead of a trained classifier. In a real deployment these would connect to actual enterprise systems (Salesforce, Zendesk, etc.).**
