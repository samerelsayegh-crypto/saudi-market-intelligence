"""
Saudi Market Lead Tracker Service
Local JSON-based CRM for opportunity and lead management.
"""
import json
import os
from datetime import datetime, timedelta
from typing import List, Optional
import uuid


DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
LEADS_FILE = os.path.join(DATA_DIR, "leads.json")


def _ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)


def _load_leads() -> List[dict]:
    """Load leads from JSON file."""
    _ensure_data_dir()
    if os.path.exists(LEADS_FILE):
        with open(LEADS_FILE, "r") as f:
            return json.load(f)
    return _get_seed_leads()


def _save_leads(leads: List[dict]):
    """Save leads to JSON file."""
    _ensure_data_dir()
    with open(LEADS_FILE, "w") as f:
        json.dump(leads, f, indent=2, default=str)


def _get_seed_leads() -> List[dict]:
    """Return pre-seeded sample leads."""
    leads = [
        {
            "id": str(uuid.uuid4())[:8],
            "company": "Saudi Aramco",
            "contact_name": "Mohammed Al-Rashid",
            "contact_title": "VP Procurement",
            "contact_email": "m.alrashid@example.com",
            "sector": "Energy",
            "region": "Eastern Province",
            "opportunity": "Digital Twin Platform for Refinery Operations",
            "estimated_value_sar": 45000000,
            "probability": 65,
            "stage": "Proposal",
            "source": "Etimad Tender",
            "notes": "Follow-up meeting scheduled. Need technical demo for refinery digital twin capabilities.",
            "last_contact": (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d"),
            "created": (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"),
            "next_action": "Send technical proposal by March 1",
        },
        {
            "id": str(uuid.uuid4())[:8],
            "company": "NEOM Company",
            "contact_name": "Sarah Al-Mutairi",
            "contact_title": "Director of Smart Infrastructure",
            "contact_email": "s.almutairi@example.com",
            "sector": "Technology",
            "region": "Tabuk",
            "opportunity": "IoT Sensor Network for The Line Residential Zone",
            "estimated_value_sar": 120000000,
            "probability": 40,
            "stage": "Qualified",
            "source": "Direct Outreach",
            "notes": "Initial meeting positive. They need a scalable IoT solution for 50,000 residential units.",
            "last_contact": (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d"),
            "created": (datetime.now() - timedelta(days=45)).strftime("%Y-%m-%d"),
            "next_action": "Prepare capability presentation for March 5 meeting",
        },
        {
            "id": str(uuid.uuid4())[:8],
            "company": "Red Sea Global",
            "contact_name": "Ahmad Al-Dosari",
            "contact_title": "Head of IT Projects",
            "contact_email": "a.aldosari@example.com",
            "sector": "Tourism",
            "region": "Tabuk / Madinah",
            "opportunity": "Smart Resort Management Platform - Shura Island",
            "estimated_value_sar": 28000000,
            "probability": 75,
            "stage": "Negotiation",
            "source": "Conference / LEAP 2026",
            "notes": "Strong fit. Competitor is Oracle Hospitality. Our edge is AI personalization and Arabic NLP.",
            "last_contact": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"),
            "created": (datetime.now() - timedelta(days=60)).strftime("%Y-%m-%d"),
            "next_action": "Submit final pricing by Feb 20",
        },
        {
            "id": str(uuid.uuid4())[:8],
            "company": "Ministry of Health",
            "contact_name": "Dr. Fatima Al-Zahrani",
            "contact_title": "Deputy Director Digital Health",
            "contact_email": "f.alzahrani@example.com",
            "sector": "Healthcare",
            "region": "Riyadh",
            "opportunity": "National Telemedicine Platform Integration",
            "estimated_value_sar": 15000000,
            "probability": 55,
            "stage": "Proposal",
            "source": "Etimad Tender",
            "notes": "RFP response submitted. Waiting for technical evaluation results. Strong local partner required.",
            "last_contact": (datetime.now() - timedelta(days=14)).strftime("%Y-%m-%d"),
            "created": (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d"),
            "next_action": "Follow up on evaluation timeline",
        },
        {
            "id": str(uuid.uuid4())[:8],
            "company": "Diriyah Gate Development Authority",
            "contact_name": "Khalid Al-Otaibi",
            "contact_title": "Smart City Program Manager",
            "contact_email": "k.alotaibi@example.com",
            "sector": "Construction",
            "region": "Riyadh",
            "opportunity": "Heritage District Smart Lighting & Environmental Monitoring",
            "estimated_value_sar": 35000000,
            "probability": 30,
            "stage": "Prospect",
            "source": "MEED Intelligence",
            "notes": "Initial research phase. Need to understand heritage preservation requirements. Specialized LED and IoT sensors needed.",
            "last_contact": (datetime.now() - timedelta(days=21)).strftime("%Y-%m-%d"),
            "created": (datetime.now() - timedelta(days=15)).strftime("%Y-%m-%d"),
            "next_action": "Request introductory meeting through local partner",
        },
        {
            "id": str(uuid.uuid4())[:8],
            "company": "Qiddiya Investment Company",
            "contact_name": "Omar Al-Harbi",
            "contact_title": "VP Entertainment Technology",
            "contact_email": "o.alharbi@example.com",
            "sector": "Entertainment",
            "region": "Riyadh",
            "opportunity": "Theme Park Ride Control Systems & Digital Ticketing",
            "estimated_value_sar": 85000000,
            "probability": 20,
            "stage": "Prospect",
            "source": "Industry Event",
            "notes": "Met at IAAPA Expo. Very early stage. Six Flags partnership may dictate vendor selection.",
            "last_contact": (datetime.now() - timedelta(days=35)).strftime("%Y-%m-%d"),
            "created": (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d"),
            "next_action": "Research Six Flags technology partners and identify entry point",
        },
        {
            "id": str(uuid.uuid4())[:8],
            "company": "Saudi Electricity Company",
            "contact_name": "Noura Al-Qahtani",
            "contact_title": "Director of Smart Grid Programs",
            "contact_email": "n.alqahtani@example.com",
            "sector": "Energy",
            "region": "Multiple",
            "opportunity": "Smart Grid Analytics & Demand Response Platform",
            "estimated_value_sar": 62000000,
            "probability": 50,
            "stage": "Qualified",
            "source": "Partner Referral",
            "notes": "Partner (Schneider Electric) referred us for analytics layer. Need to align with their AMI rollout timeline.",
            "last_contact": (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d"),
            "created": (datetime.now() - timedelta(days=25)).strftime("%Y-%m-%d"),
            "next_action": "Technical deep-dive with Schneider and SEC teams on March 10",
        },
    ]
    _save_leads(leads)
    return leads


def get_leads() -> List[dict]:
    """Get all leads."""
    return _load_leads()


def add_lead(lead: dict) -> dict:
    """Add a new lead."""
    leads = _load_leads()
    lead["id"] = str(uuid.uuid4())[:8]
    lead["created"] = datetime.now().strftime("%Y-%m-%d")
    lead["last_contact"] = datetime.now().strftime("%Y-%m-%d")
    leads.append(lead)
    _save_leads(leads)
    return lead


def update_lead(lead_id: str, updates: dict) -> Optional[dict]:
    """Update an existing lead."""
    leads = _load_leads()
    for i, lead in enumerate(leads):
        if lead["id"] == lead_id:
            leads[i].update(updates)
            _save_leads(leads)
            return leads[i]
    return None


def delete_lead(lead_id: str) -> bool:
    """Delete a lead."""
    leads = _load_leads()
    original_len = len(leads)
    leads = [l for l in leads if l["id"] != lead_id]
    if len(leads) < original_len:
        _save_leads(leads)
        return True
    return False


def get_pipeline_summary(leads: List[dict]) -> dict:
    """Generate pipeline summary statistics."""
    stages = ["Prospect", "Qualified", "Proposal", "Negotiation", "Won", "Lost"]
    stage_data = {stage: {"count": 0, "value": 0, "weighted": 0} for stage in stages}
    
    for lead in leads:
        stage = lead.get("stage", "Prospect")
        if stage in stage_data:
            stage_data[stage]["count"] += 1
            val = lead.get("estimated_value_sar", 0)
            prob = lead.get("probability", 0)
            stage_data[stage]["value"] += val
            stage_data[stage]["weighted"] += val * (prob / 100)
    
    total_pipeline = sum(d["value"] for s, d in stage_data.items() if s not in ["Won", "Lost"])
    total_weighted = sum(d["weighted"] for s, d in stage_data.items() if s not in ["Won", "Lost"])
    
    return {
        "stages": stage_data,
        "total_pipeline_value": total_pipeline,
        "total_weighted_value": total_weighted,
        "total_leads": len(leads),
        "active_leads": len([l for l in leads if l.get("stage") not in ["Won", "Lost"]]),
        "avg_probability": sum(l.get("probability", 0) for l in leads) / max(len(leads), 1),
    }


def calculate_lead_score(lead: dict) -> int:
    """Calculate opportunity score (0-100) based on multiple factors."""
    score = 0
    
    # Value component (0-30 pts)
    value = lead.get("estimated_value_sar", 0)
    if value >= 100000000:
        score += 30
    elif value >= 50000000:
        score += 25
    elif value >= 20000000:
        score += 20
    elif value >= 10000000:
        score += 15
    else:
        score += 10
    
    # Probability component (0-30 pts)
    prob = lead.get("probability", 0)
    score += int(prob * 0.3)
    
    # Stage component (0-20 pts)
    stage_scores = {"Prospect": 5, "Qualified": 10, "Proposal": 15, "Negotiation": 20}
    score += stage_scores.get(lead.get("stage", ""), 0)
    
    # Recency component (0-20 pts)
    try:
        last_contact = datetime.strptime(lead.get("last_contact", ""), "%Y-%m-%d")
        days_since = (datetime.now() - last_contact).days
        if days_since <= 7:
            score += 20
        elif days_since <= 14:
            score += 15
        elif days_since <= 30:
            score += 10
        else:
            score += 5
    except (ValueError, TypeError):
        score += 5
    
    return min(score, 100)
