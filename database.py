customers = {
    "9876543210": {
        "name": "Rahul Sharma",
        "plan": "Airtel 599 Unlimited",
        "data_remaining": "2.3 GB",
        "validity": "12 days",
        "last_recharge": "2026-06-15",
        "balance": 0,
        "pending_complaints": [],
        "billing_history": [
            {"date": "2026-06-15", "amount": 599, "status": "success"},
            {"date": "2026-05-14", "amount": 599, "status": "success"},
            {"date": "2026-04-13", "amount": 599, "status": "failed", "note": "Amount deducted, recharge not applied"}
        ]
    },
    "9123456780": {
        "name": "Priya Patel",
        "plan": "Airtel 299 Basic",
        "data_remaining": "0 GB",
        "validity": "2 days",
        "last_recharge": "2026-06-01",
        "balance": 0,
        "pending_complaints": ["NW-2024-001"],
        "billing_history": [
            {"date": "2026-06-01", "amount": 299, "status": "success"},
            {"date": "2026-05-02", "amount": 299, "status": "failed", "note": "Amount deducted, recharge not applied"}
        ]
    }
}

complaints = {}
ticket_counter = 1000
