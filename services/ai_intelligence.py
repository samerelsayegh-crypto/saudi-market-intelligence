"""
AI-Powered Market Intelligence Service
Uses Google Gemini with Search grounding for real-time Saudi market analysis.
Falls back to curated intelligence when no API key is configured.
"""
import os
import json
from datetime import datetime
from typing import List, Optional

try:
    from google import genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False


# Curated fallback intelligence (used when no API key is configured)
CURATED_INTELLIGENCE = {
    "Construction": {
        "title": "Saudi Construction Sector Outlook — Q1 2026",
        "insights": [
            "The Saudi construction sector remains the fastest-growing in the GCC, with a project pipeline valued at over US$1.7 trillion.",
            "NEOM's The Line has begun vertical construction with 40 building cores planned at 500m height each, driving unprecedented demand for precast and structural steel.",
            "Red Sea Global's Shura Island has opened with 11 luxury hotels, with Phase 2 tenders worth $11.4B expected over the next 5 years.",
            "Riyadh Metro Phases 1-3 are now operational, with station fit-out and retail leasing contracts being awarded.",
            "Diriyah Gate's $63B development is entering its most intensive construction phase with 38 hotel builds active simultaneously.",
            "New Murabba's iconic 400m Mukaab cube structure has moved from design to foundation works, creating opportunities for specialty engineering firms.",
        ],
        "key_opportunities": ["Structural Steel Supply", "Precast Concrete", "MEP Systems", "Facade Engineering", "Smart Building Tech"],
        "risk_factors": ["Labor shortages in specialized trades", "Material cost inflation", "Project scope adjustments at giga-projects"],
    },
    "Technology": {
        "title": "Saudi Technology & Digital Transformation — Q1 2026",
        "insights": [
            "Saudi Arabia's digital economy has reached 19.2% of GDP, accelerated by Vision 2030's e-government initiatives.",
            "LEAP 2026 conference attracted 170,000+ attendees with $15.6B+ in announced tech deals and investments.",
            "The National Cybersecurity Authority is expanding its monitoring capabilities with AI-driven threat detection across critical infrastructure.",
            "NEOM's digital twin platform development is creating massive demand for 3D modeling, simulation, and real-time data analytics expertise.",
            "Cloud adoption is surging with Oracle, Google, and AWS all establishing Saudi data center regions to meet data sovereignty requirements.",
            "Fintech licensing by SAMA has accelerated, with 89 licensed fintechs operating in the Kingdom by Q1 2026.",
        ],
        "key_opportunities": ["Cloud Migration", "Cybersecurity", "AI/ML Solutions", "Digital Twins", "Fintech Platforms", "IoT Infrastructure"],
        "risk_factors": ["Data localization requirements", "Saudization quotas for tech roles", "Competition from international integrators"],
    },
    "Energy": {
        "title": "Saudi Energy Transition & Renewables — Q1 2026",
        "insights": [
            "Saudi Arabia is targeting 50% renewable energy by 2030, with 58.7 GW of solar and wind capacity planned.",
            "ACWA Power's NEOM green hydrogen plant expansion targets 600 tonnes/day production capacity.",
            "The EV charging network is expanding rapidly with SEC planning 2,000+ fast-charging stations by 2027.",
            "Aramco's downstream diversification continues with new petrochemical integration projects in Jubail and Yanbu.",
            "The Kingdom's first nuclear energy plant (BAPP) is progressing in the environmental impact assessment phase.",
            "Carbon capture and storage (CCS) investments have exceeded $5B, with Jubail CCS hub processing 44 MTPA by 2035.",
        ],
        "key_opportunities": ["Solar EPC", "Green Hydrogen", "EV Infrastructure", "CCUS Technology", "Wind Farm Development", "Energy Storage"],
        "risk_factors": ["Oil price volatility impact on transition funding", "Technology maturity for green hydrogen at scale"],
    },
    "Healthcare": {
        "title": "Saudi Healthcare Transformation — Q1 2026",
        "insights": [
            "Healthcare spending in Saudi Arabia is expected to reach SAR 186B by 2026, driven by population growth and ambitious reform programs.",
            "The Ministry of Health is digitizing 100% of patient records through the SEHA platform and national health information exchange.",
            "Privatization of hospital management continues, with 30+ government hospitals now under private operation.",
            "Medical tourism initiatives aim to attract 500,000 health tourists annually by 2030.",
            "NEOM is planning a fully AI-powered health district with predictive diagnostics and robotic surgery capabilities.",
            "Biotech clusters are emerging in Riyadh and KAEC, with the Saudi Authority for Life Sciences (SFDA) accelerating drug registration.",
        ],
        "key_opportunities": ["Hospital Construction", "Health IT Systems", "Telemedicine", "Medical Equipment", "Biotech R&D", "Health Insurance Tech"],
        "risk_factors": ["Regulatory complexity in healthcare IT", "Need for Arabic language compliance in health systems"],
    },
    "Tourism": {
        "title": "Saudi Tourism & Hospitality Boom — Q1 2026",
        "insights": [
            "Saudi Arabia welcomed 109 million visitors in 2025, closing in on its 150M target for 2030.",
            "The Kingdom needs 320,000+ new hotel rooms by 2030, making hospitality construction the single largest development subsector.",
            "AlUla's Sharaan Nature Reserve and Hegra UNESCO site are attracting premium international tourists at 85% occupancy.",
            "Riyadh Season 2025 attracted 15M+ visitors, and Boulevard City is transitioning into a permanent year-round entertainment district.",
            "Cruise tourism is growing with new terminals at King Abdullah Port and Red Sea marinas.",
            "The e-visa system has expanded to 66 nationalities, dramatically simplifying tourist entry.",
        ],
        "key_opportunities": ["Hotel Development", "Resort Operations", "Tourism Tech", "F&B Chains", "Event Management", "Travel Tech / OTA"],
        "risk_factors": ["Skilled hospitality labor shortage", "Seasonality management", "International brand competition"],
    },
    "Defense": {
        "title": "Saudi Defense & Security Industry — Q1 2026",
        "insights": [
            "Saudi Arabia is the world's 5th largest defense spender with a 2026 budget of $50.1B.",
            "GAMI (General Authority for Military Industries) is targeting 50% defense spending localization by 2030.",
            "SAMI (Saudi Arabian Military Industries) has signed multiple technology transfer agreements with international OEMs.",
            "The World Defense Show 2026 in Riyadh attracted 90,000+ visitors and $20B+ in defense contracts.",
            "Cybersecurity is increasingly integrated into national defense strategy with dedicated cyber defense units established.",
            "Drone technology (UAV/UAS) development is accelerating with SAMI and private sector partnerships.",
        ],
        "key_opportunities": ["Defense Electronics", "Unmanned Systems", "Cybersecurity", "Maintenance & Sustainment", "Ammunition Manufacturing", "Defense Training"],
        "risk_factors": ["Technology transfer requirements", "Security clearance requirements for foreign contractors"],
    },
    "Finance": {
        "title": "Saudi Financial Services Evolution — Q1 2026",
        "insights": [
            "Tadawul (Saudi stock exchange) market cap has exceeded $3 trillion, making it the 8th largest globally.",
            "Saudi Central Bank (SAMA) has licensed 89 fintech companies, up from 30 in 2023.",
            "The PIF's total assets under management have reached $950B, targeting $1T by 2025's end.",
            "ESG investing is gaining traction with multiple Saudi-listed companies publishing first sustainability reports.",
            "The Regional HQ Program has attracted 540+ multinationals to establish headquarters in Riyadh.",
            "Islamic banking assets in the Kingdom exceed $800B, representing 70% of total banking assets.",
        ],
        "key_opportunities": ["Fintech Development", "Payment Solutions", "RegTech", "Wealth Management", "Islamic Finance Tech", "Insurance Tech"],
        "risk_factors": ["Regulatory compliance complexity", "Open banking readiness", "Competition from international fintechs"],
    },
}


def get_ai_intelligence(sector: str = "Construction", custom_query: str = None) -> dict:
    """
    Get AI-powered market intelligence for a sector.
    Uses Gemini with search grounding if API key available, otherwise returns curated data.
    """
    api_key = os.environ.get("GEMINI_API_KEY", "")
    
    if api_key and GENAI_AVAILABLE:
        return _fetch_live_intelligence(api_key, sector, custom_query)
    else:
        return _get_curated_intelligence(sector)


def _fetch_live_intelligence(api_key: str, sector: str, custom_query: str = None) -> dict:
    """Fetch live intelligence using Gemini with Google Search grounding."""
    try:
        client = genai.Client(api_key=api_key)
        
        if custom_query:
            prompt = custom_query
        else:
            prompt = f"""You are a Saudi Arabia market intelligence analyst specializing in the {sector} sector.

Provide a comprehensive Q1 2026 market intelligence report covering:

1. **Market Overview**: Current state and recent developments in Saudi Arabia's {sector} sector
2. **Key Opportunities**: 5-6 specific business opportunities with estimated values where possible
3. **Active Tenders/RFPs**: Any known active procurement opportunities
4. **Policy Updates**: Relevant Vision 2030 policy changes or new regulations
5. **Risk Factors**: Key challenges and risks to be aware of
6. **Competitor Landscape**: Major international and local players

Format your response as JSON with these keys:
- "title": Report title
- "insights": Array of 6 insight strings
- "key_opportunities": Array of opportunity names
- "risk_factors": Array of risk strings
- "sources": Array of source URLs used

Focus specifically on actionable business intelligence for companies looking to enter or expand in the Saudi {sector} market."""

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            config={
                "tools": [{"google_search": {}}],
                "response_mime_type": "application/json",
            },
        )
        
        result = json.loads(response.text)
        
        # Extract grounding sources
        sources = []
        if hasattr(response, 'candidates') and response.candidates:
            candidate = response.candidates[0]
            if hasattr(candidate, 'grounding_metadata') and candidate.grounding_metadata:
                chunks = getattr(candidate.grounding_metadata, 'grounding_chunks', [])
                for chunk in chunks:
                    if hasattr(chunk, 'web') and chunk.web:
                        sources.append({
                            "title": getattr(chunk.web, 'title', 'Source'),
                            "uri": getattr(chunk.web, 'uri', ''),
                        })
        
        result["sources"] = sources
        result["powered_by"] = "Google Gemini + Live Search"
        result["fetched_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
        return result
        
    except Exception as e:
        # Fall back to curated intelligence on error
        result = _get_curated_intelligence(sector)
        result["error"] = f"AI service error: {str(e)[:100]}. Showing curated intelligence."
        return result


def _get_curated_intelligence(sector: str) -> dict:
    """Return curated intelligence for a given sector."""
    if sector in CURATED_INTELLIGENCE:
        result = CURATED_INTELLIGENCE[sector].copy()
    else:
        # Return general overview if sector not found
        result = {
            "title": f"Saudi {sector} Sector Overview — Q1 2026",
            "insights": [
                f"The Saudi {sector} sector is experiencing significant investment driven by Vision 2030 diversification.",
                "The Public Investment Fund (PIF) continues to be the primary catalyst for mega-project development.",
                "Foreign direct investment into Saudi Arabia reached $25.6B in 2025, with increasing focus on technology transfer.",
                "The Saudization program (Nitaqat) is creating demand for local talent development and training services.",
                "Regional HQ mandates are bringing 540+ international companies to establish presence in Riyadh.",
                "Digital transformation is accelerating across all sectors, creating cross-cutting technology opportunities.",
            ],
            "key_opportunities": ["Market Entry Advisory", "Joint Ventures", "Technology Transfer", "Workforce Development", "Digital Solutions"],
            "risk_factors": ["Regulatory navigation", "Local partnership requirements", "Currency and repatriation policies"],
        }
    
    result["powered_by"] = "Curated Intelligence Database"
    result["fetched_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    result["sources"] = [
        {"title": "Vision 2030", "uri": "https://vision2030.gov.sa"},
        {"title": "MEED Projects", "uri": "https://meed.com"},
        {"title": "Etimad Tenders", "uri": "https://etimad.sa"},
        {"title": "Saudi Gazette", "uri": "https://saudigazette.com.sa"},
    ]
    return result


def get_available_sectors() -> List[str]:
    """Return list of sectors with curated intelligence."""
    return list(CURATED_INTELLIGENCE.keys())
