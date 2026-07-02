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
    },
    "9876543212": {
        "name": "Amit Verma",
        "plan": "Airtel 499 Unlimited 5G",
        "data_remaining": "12.5 GB",
        "validity": "18 days",
        "last_recharge": "2026-06-15",
        "balance": 45,
        "pending_complaints": [],
        "billing_history": [
            {"date": "2026-06-15", "amount": 499, "status": "success"},
            {"date": "2026-05-16", "amount": 499, "status": "success"}
        ],
        "security_alerts": [
            {
                "date": "2026-07-02",
                "type": "SIM Replacement Request",
                "status": "Pending Verification"
            },
            {
                "date": "2026-07-02",
                "type": "New Device Login",
                "status": "Detected"
            }
        ]
    }
}

complaints = {}
ticket_counter = 1000
