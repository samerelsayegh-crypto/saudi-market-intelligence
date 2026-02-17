"""
Saudi Tenders & RFP Service
Curated database of Saudi government and private tenders.
"""
import pandas as pd
from datetime import datetime, timedelta
import random


def get_tenders_data() -> pd.DataFrame:
    """Return curated Saudi tender/RFP database."""
    
    # Generate realistic tender data across Saudi sectors
    # Source URL mapping for each tender platform
    SOURCE_URLS = {
        "Etimad": "https://tenders.etimad.sa",
        "MEED": "https://www.meed.com/projects",
        "Direct": None,  # Will use entity-specific URLs below
    }
    
    ENTITY_URLS = {
        "NEOM Company": "https://www.neom.com/en-us/our-business",
        "NEOM Company / ACWA Power": "https://www.neom.com/en-us/our-business",
        "Red Sea Global": "https://www.redseaglobal.com/en/projects",
        "Qiddiya Investment Company": "https://qiddiya.com",
        "Diriyah Gate Development Authority": "https://www.dgda.gov.sa/en",
        "Royal Commission for AlUla": "https://www.rcu.gov.sa/en",
        "KAUST": "https://www.kaust.edu.sa",
        "GAMI": "https://www.gami.gov.sa/en",
    }
    
    tenders = [
        # Construction & Infrastructure
        {"id": "ETM-2026-001", "title": "NEOM Residential Zone - Phase 3 Civil Works", "entity": "NEOM Company", "sector": "Construction", "region": "Tabuk", "value_sar": 850000000, "deadline": "2026-03-15", "status": "Open", "source": "Etimad", "source_url": "https://tenders.etimad.sa", "description": "Civil and structural works for residential zone development in NEOM Bay area including foundations, superstructure, and external works."},
        {"id": "ETM-2026-002", "title": "Riyadh Metro Station Fit-Out Package B", "entity": "Royal Commission for Riyadh City", "sector": "Construction", "region": "Riyadh", "value_sar": 320000000, "deadline": "2026-02-28", "status": "Closing Soon", "source": "Etimad", "source_url": "https://tenders.etimad.sa", "description": "Interior fit-out and MEP works for 8 metro stations on Line 4 including architectural finishes, escalators, and safety systems."},
        {"id": "ETM-2026-003", "title": "King Salman Park - Landscape & Irrigation Contract", "entity": "Royal Commission for Riyadh City", "sector": "Construction", "region": "Riyadh", "value_sar": 180000000, "deadline": "2026-04-10", "status": "Open", "source": "Etimad", "source_url": "https://tenders.etimad.sa", "description": "Comprehensive landscaping, hardscaping, and smart irrigation systems for King Salman Park Phase 2."},
        {"id": "ETM-2026-004", "title": "Red Sea Airport Terminal Expansion", "entity": "Red Sea Global", "sector": "Construction", "region": "Madinah", "value_sar": 2400000000, "deadline": "2026-05-01", "status": "Open", "source": "Direct", "source_url": "https://www.redseaglobal.com/en/projects", "description": "Design and build of the expanded international terminal at Red Sea International Airport with 3M pax capacity."},
        {"id": "ETM-2026-005", "title": "Jeddah Historic District Restoration - Batch 7", "entity": "Ministry of Culture", "sector": "Construction", "region": "Jeddah", "value_sar": 95000000, "deadline": "2026-03-20", "status": "Open", "source": "Etimad", "source_url": "https://tenders.etimad.sa", "description": "Conservation and restoration of 15 historic buildings in Al-Balad district with traditional Hejazi architectural techniques."},
        {"id": "ETM-2026-006", "title": "Qiddiya Six Flags Theme Park - Ride Systems", "entity": "Qiddiya Investment Company", "sector": "Entertainment", "region": "Riyadh", "value_sar": 1600000000, "deadline": "2026-06-15", "status": "Open", "source": "Direct", "source_url": "https://qiddiya.com", "description": "Supply, installation, and commissioning of 28 ride systems for the Six Flags Qiddiya theme park."},
        
        # Technology & Digital
        {"id": "ETM-2026-010", "title": "National Cybersecurity Platform Upgrade", "entity": "National Cybersecurity Authority", "sector": "Technology", "region": "Riyadh", "value_sar": 450000000, "deadline": "2026-03-01", "status": "Closing Soon", "source": "Etimad", "source_url": "https://tenders.etimad.sa", "description": "Comprehensive upgrade of national cyber defense infrastructure including SOC modernization, threat intelligence, and AI-based detection."},
        {"id": "ETM-2026-011", "title": "Smart City IoT Infrastructure - Diriyah Gate", "entity": "Diriyah Gate Development Authority", "sector": "Technology", "region": "Riyadh", "value_sar": 280000000, "deadline": "2026-04-20", "status": "Open", "source": "Direct", "source_url": "https://www.dgda.gov.sa/en", "description": "Design, supply and installation of IoT sensors, edge computing nodes, and smart building management across Diriyah Gate."},
        {"id": "ETM-2026-012", "title": "Cloud Migration for Ministry of Health Systems", "entity": "Ministry of Health", "sector": "Technology", "region": "Riyadh", "value_sar": 120000000, "deadline": "2026-03-30", "status": "Open", "source": "Etimad", "source_url": "https://tenders.etimad.sa", "description": "Migration of 40+ legacy health information systems to secure cloud infrastructure with disaster recovery."},
        {"id": "ETM-2026-013", "title": "AI-Powered Traffic Management System - Jeddah", "entity": "Jeddah Municipality", "sector": "Technology", "region": "Jeddah", "value_sar": 175000000, "deadline": "2026-05-15", "status": "Open", "source": "Etimad", "source_url": "https://tenders.etimad.sa", "description": "Intelligent traffic management system using AI, computer vision, and adaptive signal control for 500+ intersections."},
        {"id": "ETM-2026-014", "title": "NEOM Digital Twin Platform Development", "entity": "NEOM Company", "sector": "Technology", "region": "Tabuk", "value_sar": 380000000, "deadline": "2026-07-01", "status": "Open", "source": "Direct", "source_url": "https://www.neom.com/en-us/our-business", "description": "Development of comprehensive 3D digital twin platform for urban planning, simulation, and real-time operations management."},
        
        # Energy
        {"id": "ETM-2026-020", "title": "NEOM Green Hydrogen Plant - Phase 2 EPC", "entity": "NEOM Company / ACWA Power", "sector": "Energy", "region": "Tabuk", "value_sar": 5200000000, "deadline": "2026-04-15", "status": "Open", "source": "Direct", "source_url": "https://www.neom.com/en-us/our-business", "description": "EPC contract for expansion of green hydrogen production facility targeting 600 tonnes per day output."},
        {"id": "ETM-2026-021", "title": "Solar PV Farm - Al Faisaliah 500MW", "entity": "Saudi Power Procurement Company", "sector": "Energy", "region": "Makkah", "value_sar": 1800000000, "deadline": "2026-03-25", "status": "Open", "source": "Etimad", "source_url": "https://tenders.etimad.sa", "description": "Development, construction, and operation of 500MW utility-scale solar photovoltaic park."},
        {"id": "ETM-2026-022", "title": "Electric Vehicle Charging Network - Phase 1", "entity": "Saudi Electricity Company", "sector": "Energy", "region": "Multiple", "value_sar": 260000000, "deadline": "2026-04-05", "status": "Open", "source": "Etimad", "source_url": "https://tenders.etimad.sa", "description": "Installation of 2,000 EV fast-charging stations across Riyadh, Jeddah, and Dammam highway corridors."},
        
        # Healthcare
        {"id": "ETM-2026-030", "title": "King Fahd Medical City Expansion - Tower B", "entity": "Ministry of Health", "sector": "Healthcare", "region": "Riyadh", "value_sar": 2100000000, "deadline": "2026-05-20", "status": "Open", "source": "Etimad", "source_url": "https://tenders.etimad.sa", "description": "Design and construction of 500-bed specialty hospital tower with cutting-edge medical equipment and smart patient systems."},
        {"id": "ETM-2026-031", "title": "Primary Healthcare Centers Network - Eastern Province", "entity": "Ministry of Health", "sector": "Healthcare", "region": "Eastern Province", "value_sar": 340000000, "deadline": "2026-04-01", "status": "Open", "source": "Etimad", "source_url": "https://tenders.etimad.sa", "description": "Construction and equipping of 25 primary healthcare centers across Eastern Province communities."},
        {"id": "ETM-2026-032", "title": "Telemedicine Platform National Rollout", "entity": "Saudi Health Council", "sector": "Healthcare", "region": "Multiple", "value_sar": 85000000, "deadline": "2026-03-10", "status": "Closing Soon", "source": "Etimad", "source_url": "https://tenders.etimad.sa", "description": "Development and deployment of national telemedicine platform supporting video consultations, e-prescriptions, and AI triage."},
        
        # Defense & Security
        {"id": "ETM-2026-040", "title": "Border Surveillance Systems Upgrade", "entity": "Ministry of Interior", "sector": "Defense", "region": "Multiple", "value_sar": 920000000, "deadline": "2026-06-01", "status": "Open", "source": "Etimad", "source_url": "https://tenders.etimad.sa", "description": "Upgrade of 2,500km border surveillance with thermal imaging, drone detection, and command & control integration."},
        {"id": "ETM-2026-041", "title": "Military Communication Infrastructure Modernization", "entity": "GAMI", "sector": "Defense", "region": "Riyadh", "value_sar": 1500000000, "deadline": "2026-07-15", "status": "Open", "source": "Direct", "source_url": "https://www.gami.gov.sa/en", "description": "Next-generation military communications network with satellite, tactical radio, and encrypted data systems."},
        
        # Transport & Logistics
        {"id": "ETM-2026-050", "title": "Jeddah-Makkah High-Speed Rail Extension Study", "entity": "Saudi Railways Authority", "sector": "Transport", "region": "Makkah", "value_sar": 45000000, "deadline": "2026-03-05", "status": "Closing Soon", "source": "Etimad", "source_url": "https://tenders.etimad.sa", "description": "Feasibility study and preliminary design for 80km high-speed rail extension connecting Jeddah airport to Makkah."},
        {"id": "ETM-2026-051", "title": "King Abdullah Port Container Terminal T3", "entity": "Saudi Ports Authority", "sector": "Transport", "region": "KAEC", "value_sar": 3200000000, "deadline": "2026-08-01", "status": "Open", "source": "Etimad", "source_url": "https://tenders.etimad.sa", "description": "Design, build but and operate third container terminal with 3M TEU capacity and automated yard systems."},
        {"id": "ETM-2026-052", "title": "Riyadh Bus Rapid Transit - Package 4", "entity": "Royal Commission for Riyadh City", "sector": "Transport", "region": "Riyadh", "value_sar": 550000000, "deadline": "2026-04-25", "status": "Open", "source": "Etimad", "source_url": "https://tenders.etimad.sa", "description": "Construction of 35km dedicated BRT lanes with 28 stations, passenger information systems, and depot facilities."},
        
        # Tourism & Entertainment
        {"id": "ETM-2026-060", "title": "AlUla Desert Resort - Luxury Eco-Lodge Development", "entity": "Royal Commission for AlUla", "sector": "Tourism", "region": "Madinah", "value_sar": 680000000, "deadline": "2026-05-10", "status": "Open", "source": "Direct", "source_url": "https://www.rcu.gov.sa/en", "description": "Development of 120-key ultra-luxury eco-resort integrated into AlUla canyon landscape with minimal environmental footprint."},
        {"id": "ETM-2026-061", "title": "Jeddah Waterfront Corniche Redevelopment", "entity": "Jeddah Municipality", "sector": "Tourism", "region": "Jeddah", "value_sar": 420000000, "deadline": "2026-04-30", "status": "Open", "source": "Etimad", "source_url": "https://tenders.etimad.sa", "description": "Comprehensive redesign and construction of 12km waterfront promenade with F&B outlets, marina, and public art installations."},
        
        # Education
        {"id": "ETM-2026-070", "title": "KAUST Research Campus Expansion", "entity": "KAUST", "sector": "Education", "region": "Jeddah", "value_sar": 750000000, "deadline": "2026-06-20", "status": "Open", "source": "Direct", "source_url": "https://www.kaust.edu.sa", "description": "New research laboratories, innovation hub, and faculty housing at King Abdullah University of Science and Technology."},
        {"id": "ETM-2026-071", "title": "Smart Classroom Technology - 500 Schools", "entity": "Ministry of Education", "sector": "Education", "region": "Multiple", "value_sar": 195000000, "deadline": "2026-03-28", "status": "Open", "source": "Etimad", "source_url": "https://tenders.etimad.sa", "description": "Supply and installation of interactive displays, digital learning platforms, and networking for 500 public schools."},
        
        # Water & Environment
        {"id": "ETM-2026-080", "title": "Jubail 4 Desalination Plant", "entity": "SWCC", "sector": "Water", "region": "Eastern Province", "value_sar": 4500000000, "deadline": "2026-09-01", "status": "Open", "source": "Etimad", "source_url": "https://tenders.etimad.sa", "description": "Design, build, and operate 600,000 m³/day reverse osmosis desalination plant with solar energy integration."},
        {"id": "ETM-2026-081", "title": "Riyadh Stormwater Management System", "entity": "National Water Company", "sector": "Water", "region": "Riyadh", "value_sar": 310000000, "deadline": "2026-05-15", "status": "Open", "source": "Etimad", "source_url": "https://tenders.etimad.sa", "description": "Construction of 45km stormwater drainage network with smart monitoring and flood prevention systems."},
        
        # Recently Awarded (for pipeline tracking)
        {"id": "ETM-2025-090", "title": "NEOM The Line - Foundation Package Alpha", "entity": "NEOM Company", "sector": "Construction", "region": "Tabuk", "value_sar": 3800000000, "deadline": "2025-12-01", "status": "Awarded", "source": "MEED", "source_url": "https://www.meed.com/projects", "description": "Major foundation and substructure package for the first section of The Line vertical city."},
        {"id": "ETM-2025-091", "title": "Riyadh Season 2026 Tech Infrastructure", "entity": "General Entertainment Authority", "sector": "Entertainment", "region": "Riyadh", "value_sar": 220000000, "deadline": "2025-11-15", "status": "Awarded", "source": "Etimad", "source_url": "https://tenders.etimad.sa", "description": "AV systems, lighting, staging, and digital ticketing infrastructure for Riyadh Season 2026 events."},
        {"id": "ETM-2025-092", "title": "Ministry of Interior - CCTV Analytics Platform", "entity": "Ministry of Interior", "sector": "Defense", "region": "Multiple", "value_sar": 340000000, "deadline": "2025-10-20", "status": "Awarded", "source": "Etimad", "source_url": "https://tenders.etimad.sa", "description": "AI-powered video analytics platform integrated with national CCTV network for public safety."},
    ]
    
    df = pd.DataFrame(tenders)
    df["deadline"] = pd.to_datetime(df["deadline"])
    df["value_sar"] = df["value_sar"].astype(float)
    
    # Calculate days until deadline
    today = pd.Timestamp.now().normalize()
    df["days_left"] = (df["deadline"] - today).dt.days
    
    # Update status based on deadline proximity
    for idx, row in df.iterrows():
        if row["status"] not in ["Awarded", "Closed"]:
            if row["days_left"] < 0:
                df.at[idx, "status"] = "Closed"
            elif row["days_left"] <= 14:
                df.at[idx, "status"] = "Closing Soon"
    
    return df


def get_tenders_summary(df: pd.DataFrame) -> dict:
    """Generate tender statistics."""
    active = df[df["status"].isin(["Open", "Closing Soon"])]
    return {
        "total_tenders": len(df),
        "open_tenders": len(df[df["status"] == "Open"]),
        "closing_soon": len(df[df["status"] == "Closing Soon"]),
        "awarded": len(df[df["status"] == "Awarded"]),
        "total_value": active["value_sar"].sum(),
        "avg_value": active["value_sar"].mean(),
        "by_sector": active.groupby("sector")["value_sar"].sum().sort_values(ascending=False).to_dict(),
        "by_region": active.groupby("region")["value_sar"].sum().sort_values(ascending=False).to_dict(),
        "by_status": df.groupby("status").size().to_dict(),
    }
