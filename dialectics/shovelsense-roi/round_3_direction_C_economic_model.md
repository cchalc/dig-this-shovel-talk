# Round 3, Direction C: Five-Year Total Cost of Ownership and ROI Analysis

**Question:** What's the true 5-year total cost of ownership for each technology path, and what ROI does each need to break even?

---

## Economic Baseline Assumptions

| Parameter | Value | Source |
|-----------|-------|--------|
| Monthly ore throughput | 800,000 tonnes | Given |
| Average head grade | 0.45% Cu | Given |
| Cutoff grade | 0.32% Cu | Given |
| Copper price | $4.00/lb ($8,820/tonne) | Given |
| Metallurgical recovery | 85% | Given |
| Mineralogy | 80% chalcopyrite / 20% bornite | Given |

**Monthly copper production (theoretical):**
- 800,000 t x 0.45% Cu x 85% recovery = **3,060 tonnes Cu/month**
- Annual value: 3,060 x 12 x $8,820 = **$323.8M/year**

**Value per 0.01% grade improvement:**
- 800,000 t x 0.0001 x 85% x $8,820 x 12 = **$7.2M/year**

---

## Technology TCO Analysis

### 1. ShovelSense (XRF)

**Cost Structure:**
| Item | Cost | Notes |
|------|------|-------|
| Operating lease | $200K/month | All-inclusive (equipment, maintenance, support, calibration) |
| 5-year lease total | $12.0M | 60 months x $200K |
| Multi-shovel discount | Likely 10-15% | Not publicly confirmed; assumed for 3+ units |
| Installation/mobilization | ~$50K | One-time per shovel |
| Internal staff training | ~$25K | One-time |

**5-Year TCO: $12.0-12.5M**

**Contract structure (industry standard for mining tech leases):**
- Typical minimum term: 24-36 months
- Exit clauses: Usually require notice period (3-6 months) with equipment return obligations
- Performance guarantees: Rarely binding; typically "best efforts" language

**What's included:**
- Hardware (XRF sensors, mounting, computing)
- Ongoing calibration and maintenance
- Technical support
- Software updates
- Typically includes a pilot/trial period (3-6 months) at reduced rate

### 2. PGNAA Belt Analyzer

**Cost Structure:**
| Item | Cost | Notes |
|------|------|-------|
| Capital purchase | $800K-1.2M | Thermo Fisher CB Omni or equivalent |
| Installation | $150-300K | Conveyor integration, radiation shielding, infrastructure |
| Annual maintenance | $80-120K | 10-15% of capital; service contracts, neutron source replacement |
| Annual calibration | $15-25K | Site-specific calibration, lab sample correlation |
| Spare parts/consumables | $10-20K/year | X-ray tubes, detectors, etc. |
| Expected equipment life | 15-20 years | Well-established technology |

**5-Year TCO Calculation:**
| Component | Year 0-1 | Years 2-5 | Total |
|-----------|----------|-----------|-------|
| Capital + installation | $1.1M | - | $1.1M |
| Annual maintenance | $100K | $400K | $500K |
| Calibration | $20K | $80K | $100K |
| Consumables | $15K | $60K | $75K |
| **Total** | **$1.235M** | **$540K** | **$1.775M** |

**5-Year TCO: ~$1.8M**

### 3. MRT (NextOre)

**Cost Structure (estimated from industry sources):**

NextOre pricing is not publicly disclosed. Based on comparable bulk ore sorting technology economics and the [RFC Ambrian analysis](http://www.rfcambrian.com/nextore-breakthrough-ore-sorting-technology/):

| Item | Estimate | Notes |
|------|----------|-------|
| Capital system | $1.5-3.0M | Conveyor-mounted MR analyzer + infrastructure |
| Installation | $200-400K | Material handling, diverters, integration |
| Annual maintenance | $100-150K | Specialized RF equipment |
| Lease alternative | Unknown | NextOre may offer lease/performance-based models |

**5-Year TCO Estimate:**
| Model | Calculation | Total |
|-------|-------------|-------|
| Capital purchase | $2.5M + $200K install + 5 x $125K maintenance | **$3.3M** |
| High estimate | $3.5M + $400K install + 5 x $150K maintenance | **$4.7M** |

**5-Year TCO: $3.3-4.7M** (midpoint ~$4.0M)

### 4. Blast Hole Optimization

**Cost Structure:**
| Item | Cost | Notes |
|------|------|-------|
| Geostatistics consulting | $50-100K | Initial variography, sampling protocol design |
| Blast movement monitoring (Hexagon BMM) | $100-150K/year | Annual license + monitors (~cents per tonne) |
| Additional RC drilling | $100-200K/year | Infill drilling for tighter grade control |
| Lab upgrades/turnaround | $50-75K | Faster assay capability |
| Training and protocol changes | $25-50K | One-time |

**5-Year TCO Calculation:**
| Component | Year 1 | Years 2-5 | Total |
|-----------|--------|-----------|-------|
| Consulting | $75K | - | $75K |
| BMM system | $125K | $500K | $625K |
| Additional drilling | $150K | $600K | $750K |
| Lab upgrades | $75K | - | $75K |
| Training | $50K | - | $50K |
| **Total** | **$475K** | **$1.1M** | **$1.575M** |

**5-Year TCO: ~$1.6M**

---

## Summary: 5-Year TCO Comparison

| Technology | 5-Year TCO | Annual Equivalent | Cost per Tonne |
|------------|------------|-------------------|----------------|
| **ShovelSense** | $12.0-12.5M | $2.4M/year | $0.25/t |
| **PGNAA** | ~$1.8M | $0.36M/year | $0.04/t |
| **MRT (NextOre)** | $3.3-4.7M | $0.8M/year | $0.08/t |
| **Blast Hole Optimization** | ~$1.6M | $0.32M/year | $0.03/t |

**ShovelSense costs 6-7x more than any alternative over 5 years.**

---

## Required Grade Improvement for Breakeven

Given:
- Monthly ore: 800,000 tonnes
- Average grade: 0.45% Cu
- Recovery: 85%
- Copper price: $8,820/tonne Cu

**Value creation formula:**
- Value = Throughput x Grade Improvement x Recovery x Cu Price x 12 months

**Breakeven calculation:**

| Technology | 5-Year TCO | Annual Value Needed | Required Grade Improvement |
|------------|------------|---------------------|----------------------------|
| **ShovelSense** | $12.0M | $2.4M/year | 0.033% Cu (7.3% of head grade) |
| **PGNAA** | $1.8M | $0.36M/year | 0.005% Cu (1.1% of head grade) |
| **MRT** | $4.0M | $0.80M/year | 0.011% Cu (2.4% of head grade) |
| **Blast Hole** | $1.6M | $0.32M/year | 0.0044% Cu (1.0% of head grade) |

**Interpretation:**
- ShovelSense needs to improve delivered grade by **0.033% Cu absolute** (from 0.450% to 0.483%) to break even
- This is equivalent to **7.3%** relative improvement in head grade
- PGNAA needs only **1.1%** relative improvement
- Blast hole optimization needs only **1.0%** relative improvement

---

## Risk-Adjusted Expected Value

### Probability Estimates

Based on validation evidence assessed in Rounds 1-2:

| Technology | P(Achieves Breakeven) | Evidence Basis |
|------------|----------------------|----------------|
| **ShovelSense** | 35% | No independent validation; surface-volume correlation unknown; vendor claims only |
| **PGNAA** | 75% | Extensive industrial validation; proven technology; volumetric measurement |
| **MRT** | 65% | Peer-reviewed Kansanshi trial; operational at multiple sites; newer technology |
| **Blast Hole** | 60% | Academic literature support; depends on current baseline quality |

### Expected Value Calculation

Assume realistic improvement scenarios (not maximum vendor claims):

| Technology | Realistic Improvement | Annual Value | 5-Year Gross Value | 5-Year TCO | Net Value | P(Success) | Expected Value |
|------------|----------------------|--------------|-------------------|------------|-----------|------------|----------------|
| **ShovelSense** | 0.04% Cu | $2.9M | $14.4M | $12.0M | $2.4M | 35% | **$0.8M** |
| **PGNAA** | 0.02% Cu | $1.4M | $7.2M | $1.8M | $5.4M | 75% | **$4.1M** |
| **MRT** | 0.03% Cu | $2.2M | $10.8M | $4.0M | $6.8M | 65% | **$4.4M** |
| **Blast Hole** | 0.015% Cu | $1.1M | $5.4M | $1.6M | $3.8M | 60% | **$2.3M** |

**Risk-Adjusted 5-Year Expected Value:**
1. **MRT (NextOre):** $4.4M
2. **PGNAA:** $4.1M
3. **Blast Hole Optimization:** $2.3M
4. **ShovelSense:** $0.8M

---

## Final Ranking: Risk-Adjusted ROI

| Rank | Technology | 5-Year TCO | Required Breakeven | Risk-Adjusted EV | ROI Multiple |
|------|------------|------------|-------------------|------------------|--------------|
| **1** | MRT (NextOre) | $4.0M | 2.4% improvement | $4.4M | 1.1x |
| **2** | PGNAA | $1.8M | 1.1% improvement | $4.1M | 2.3x |
| **3** | Blast Hole | $1.6M | 1.0% improvement | $2.3M | 1.4x |
| **4** | ShovelSense | $12.0M | 7.3% improvement | $0.8M | 0.07x |

---

## Conclusions

1. **ShovelSense has the worst risk-adjusted ROI by a large margin.** It costs 6-7x more than alternatives, requires 7x the improvement to break even, and has the weakest validation evidence. Even optimistic scenarios yield poor expected value.

2. **PGNAA offers the best capital efficiency.** Lowest breakeven threshold (1.1%), highest success probability (75%), and proven technology. The 2.3x ROI multiple reflects both low cost and high confidence.

3. **MRT offers the highest absolute expected value** ($4.4M) but requires more capital commitment. The peer-reviewed validation at Kansanshi provides confidence, but the technology is newer than PGNAA.

4. **Blast hole optimization is the low-risk entry point.** Lowest cost, well-understood methodology, and creates the baseline assessment infrastructure needed to evaluate any sensor technology.

**Recommended sequence:**
1. **Blast hole optimization first** ($1.6M over 5 years) - establishes baseline, quick wins
2. **PGNAA or MRT second** - provides ground truth for any upstream sensor evaluation
3. **ShovelSense never, or last** - only if independent validation emerges and only after belt-based ground truth is available

The $12M saved by avoiding ShovelSense could fund PGNAA + MRT + blast hole optimization combined, with money left over.

---

## Sources

- [Thermo Fisher - PGNAA Technology](https://www.thermofisher.com/us/en/home/industrial/cement-coal-minerals/cement-coal-minerals-learning-center/cement-analysis-production-information/pgnaa-pftna-technology.html)
- [Hexagon - Blast Movement Monitoring](https://hexagon.com/products/hexagon-blast-movement-monitoring)
- [NextOre - Bulk Ore Sorting](https://www.nextore.com.au/)
- [International Mining - NextOre Kansanshi](https://im-mining.com/2022/05/24/nextore-first-quantum-fully-commission-worlds-largest-bulk-ore-sorting-system/)
- [RFC Ambrian - NextOre Analysis](http://www.rfcambrian.com/nextore-breakthrough-ore-sorting-technology/)
- [MineSense - ShovelSense](https://minesense.com/shovelsense/)
- [CIM Magazine - No Time for Waste](http://magazine.cim.org/en/technology/no-time-for-waste/)
- [XRF Analyzer Cost Guide](https://www.vrxrf.com/resource/guide/how-much-does-a-quality-xrf-analyzer-cost/)
