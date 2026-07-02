Telecom AI Support Agent

An AI support agent that doesn't just answer telecom customer queries but also resolves them. When a problem needs human intervention, it seamlessly hands over the case with a complete summary, so customers don't have to repeat themselves.

Live app: tele-agent-fde.streamlit.app
Demo login: 9876543210

What it does

Failed recharge : Detects it in billing history, confirms refund + timeline
Billing dispute : Explains charges from actual account data
Network complaint : Raises a ticket, gives resolution timeline
Escalation : Auto-generates a complete context summary for the human agent, customer never repeats themselves

How it works
Customer logs in → intent is classified → LLM (Llama 3.3 70B via Groq) generates a grounded response using real account data → network issues and escalations auto-generate tickets → escalation summaries are built with plain logic, not the LLM, to keep billing data 100% accurate in the handoff.
