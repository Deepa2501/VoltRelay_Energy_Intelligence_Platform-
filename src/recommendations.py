"""
VoltRelay Energy - Evidence-Backed Priority Actions Engine
Translates analytical findings into prioritized, quantified management interventions.
"""

import pandas as pd

def get_actionable_recommendations():
    """Returns structured executive recommendations."""
    return [
        {
            'Category': 'Operations & Capacity',
            'Title': 'Emergency Battery Rebalancing & Rapid Charger Deployment to Jaipur & Delhi NCR',
            'Priority': 'P0 - IMMEDIATE (Next 14 Days)',
            'Problem': 'Jaipur (7.16% failure rate) and Delhi NCR (6.83% failure rate) Launch stations suffer severe evening battery stock-outs with queue times exceeding 32 minutes.',
            'Evidence': '57% higher failure rate than network baseline; 94,000+ failed swaps concentrated in 48 Launch stations during 17:00–21:00 peak.',
            'Target Segment': 'Top 20 worst bottleneck stations (e.g., STN-DEL-037, STN-DEL-048, STN-JAI-137, STN-JAI-142).',
            'Recommended Action': 'Reallocate 350 healthy Cellora/Amptek battery packs from under-utilized Mumbai & Pune Wave-2 stations to Jaipur & Delhi hubs; upgrade charger generation from Gen-1 to Gen-2.',
            'Expected Impact': 'Estimated reduction of failure rate from 7.16% to <4.2% across Delhi & Jaipur; recovery of ₹6.2M in annual lost swap revenue.'
        },
        {
            'Category': 'Procurement & Vendor Governance',
            'Title': 'Halt Kyron Procurement & Enforce Comprehensive Warranty Clawback',
            'Priority': 'P0 - IMMEDIATE',
            'Problem': 'Kyron battery packs suffer catastrophic degradation (mean SOH 63.7%), leading to 87.8% (1,438 units) premature retirement within 12 months.',
            'Evidence': '1,438 of 1,638 Kyron packs retired vs 0 retirements in 4,862 Cellora and Amptek packs across the exact same operating duration.',
            'Target Segment': 'All remaining 200 active Kyron packs and historical procurement invoices.',
            'Recommended Action': 'Immediately quarantine remaining active Kyron packs to avoid thermal events; file formal commercial warranty claim against Kyron for ₹4.45 Cr capital replacement cost.',
            'Expected Impact': 'Direct recovery of up to ₹4.45 Cr in vendor warranty credits; elimination of 60%+ of network-wide "no charged battery" failure events.'
        },
        {
            'Category': 'Commercial & Fleet Partnerships',
            'Title': 'Renegotiate ZipDrop (FP-03) Contract Terms to Reinstate Peak Economics',
            'Priority': 'P1 - HIGH (Next 30 Days)',
            'Problem': '2024-11-01 contract amendment raised discount from 12% to 28% and waived peak surcharges, reducing net revenue per swap by 24% (from ₹57.1 to ₹43.3–₹46.7).',
            'Evidence': 'While swap volume grew +70%, net margin per swap turned negative during high grid-tariff hours, failing to cover battery wear and station opex.',
            'Target Segment': 'Fleet Partner FP-03 (ZipDrop) — 2,381 riders.',
            'Recommended Action': 'Introduce a tiered discount structure requiring minimum monthly completed swap commitments and reinstate peak-hour surcharge of ₹10/swap during 18:00–21:00.',
            'Expected Impact': 'Margin improvement of ₹8.4M annually without causing volume churn due to high driver reliance on VoltRelay network.'
        },
        {
            'Category': 'Customer Experience & Churn Prevention',
            'Title': 'Automated "Zero-Friction" Credit Trigger for Poor Onboarding Experience',
            'Priority': 'P1 - HIGH',
            'Problem': 'Riders experiencing even one failure in their first 3 swaps have a 42% higher 30-day churn hazard.',
            'Evidence': '4,200+ churned riders had an early failed swap or >20 minute queue wait during their first week of onboarding.',
            'Target Segment': 'New signups in their first 14 days of tenure across all cities.',
            'Recommended Action': 'Deploy automated webhook: if a new rider experiences a failed swap or >15 min queue wait, automatically credit ₹100 wallet balance with an apology SMS and priority slot reservation.',
            'Expected Impact': 'Projected 4.8 percentage point uplift in 30-day cohort retention, saving ~960 active riders and generating ₹3.8M in lifetime gross margin.'
        },
        {
            'Category': 'Dynamic Pricing & Network Load Balancing',
            'Title': 'Expand Off-Peak Discount Incentives to Shift Peak Traffic to Wave 1/2 Stations',
            'Priority': 'P2 - MEDIUM (Next 60 Days)',
            'Problem': 'Launch stations operate at near 100% capacity during evening peaks, while Wave 1 and Wave 2 stations operate at <40% utilization.',
            'Evidence': 'Pilot in Bengaluru and Pune demonstrated price sensitivity among independent riders.',
            'Target Segment': 'Independent and pay-as-you-go riders (7,600+ riders).',
            'Recommended Action': 'Introduce ₹15 off-peak discount (11:00–16:00 and 22:00–06:00) and implement in-app station navigation steering riders to nearby Wave-1/2 stations within 1.5km.',
            'Expected Impact': '15–20% peak load shifting away from bottleneck stations, reducing average peak queue wait by 8.5 minutes.'
        }
    ]
