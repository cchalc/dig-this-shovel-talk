# Round 3 Synthesis: The Decision Crystallizes

## The Four Directions

| Direction | Core Finding |
|-----------|--------------|
| **A: MRT Deep-Dive** | MRT cannot detect bornite — your 20% bornite makes MRT unsuitable as standalone |
| **B: Blast Hole Optimization** | 10-20% improvement achievable at 1/6th the cost of sensors |
| **C: Economic Model** | ShovelSense costs 6-7x more than alternatives, requires 7x the improvement to break even |
| **D: Implementation Risk** | Six failure modes kill ROI regardless of technology choice |

---

## The Convergent Picture

Round 3 eliminates options and clarifies the path:

### What's Eliminated

1. **ShovelSense** — The economics don't work. $12M over 5 years, requiring 7.3% grade improvement to break even, with only 35% probability of achieving claimed ROI. Risk-adjusted expected value is near zero.

2. **MRT as standalone** — Despite superior validation, MRT cannot detect bornite. Your 20% bornite content would cause systematic 20% underreporting of copper grade, potentially misclassifying ore as waste.

### What Remains Viable

1. **Blast hole optimization** — Lowest risk, lowest cost, proven at multiple operations. 10-20% misclassification reduction at $400-700K + $300K/year. Should be implemented FIRST.

2. **PGNAA** — Detects total copper regardless of mineralogy (chalcopyrite + bornite). $1.8M over 5 years. Provides ground truth for all upstream decisions. Viable second step.

3. **MRT + PGNAA hybrid** — The academic literature suggests combining MRT (fast, high-throughput) with PGNAA (mineralogy-agnostic) for mixed sulfide ores. Complex but potentially optimal.

---

## The Final Recommendation

### Phase 1: Optimize What You Have (Months 1-12)

**Investment:** $400-700K capital + $300K/year operating
**Expected improvement:** 10-15% reduction in misclassification

| Action | Cost | Impact |
|--------|------|--------|
| Baseline assessment | ~$15K | Know your actual F1 factor and misclassification rate |
| Blast movement monitoring | ~$150-300K/yr | 5-7% misclassification reduction |
| Sampling protocol upgrade | ~$50K | 5-15% reduction in fundamental sampling error |
| Portable XRF screening | ~$50K | Faster decisions, >0.98 correlation with lab |
| GPS dig guidance | ~$200-400K | Eliminates execution error |
| Geostatistics consulting | ~$50-100K | ML-enhanced grade modeling |

### Phase 2: Ground Truth Measurement (Months 12-24)

**Investment:** ~$800K capital + installation
**Purpose:** Establish independent verification of grade at belt level

Deploy PGNAA belt analyzer:
- Measures total copper (chalcopyrite + bornite)
- Provides reconciliation data for blast hole calibration
- Enables empirical validation of any shovel-mounted sensor
- Creates feedback loop for continuous improvement

### Phase 3: Evaluate Shovel-Level Sensing — Maybe (Months 24-36)

**Only if:**
- Phase 1 + Phase 2 show residual misclassification worth capturing
- Belt data proves surface-volume correlation exists at your deposit
- Independent validation of ShovelSense emerges (currently none)
- OR: NextOre develops bornite-capable MRT

**Otherwise:** Stop at Phase 2. The problem may be solved without shovel-level sensing.

---

## What NOT To Do

1. **Don't buy ShovelSense now.** $12M over 5 years with 35% success probability and no independent validation. The risk-adjusted economics are negative.

2. **Don't assume MRT solves everything.** Bornite blindness is a hard constraint at your deposit.

3. **Don't skip the baseline.** If your current F1 > 0.92, no sensor technology delivers ROI.

4. **Don't deploy sensors without implementation discipline.** The six failure modes (operator bypass, calibration decay, set-and-forget, etc.) kill ROI regardless of technology.

---

## The Math

| Path | 5-Year Cost | Required Improvement | Success Probability | Risk-Adjusted EV |
|------|-------------|---------------------|---------------------|------------------|
| **ShovelSense** | $12.0M | 7.3% | 35% | $0.8M |
| **Blast Hole + PGNAA** | $3.4M | 1.5% | 70% | $5.0M |
| **Do Nothing** | $0 | 0% | 100% | $0 |

The **Blast Hole + PGNAA path** delivers **6x better risk-adjusted return** than ShovelSense.

---

## Implementation Checklist (From Direction D)

Before deploying ANY technology:

1. ☐ Measure baseline misclassification rate (F1 factor, ore/waste accuracy)
2. ☐ Define success metrics in contract with measurement protocol
3. ☐ Include performance-based exit clauses
4. ☐ Start in advisory mode for 6+ months before relying on sensor decisions
5. ☐ Assign a single calibration owner (person, not committee)
6. ☐ Define data hierarchy: which system is authoritative when they disagree?
7. ☐ Require workflow-focused training, not just display operation
8. ☐ Budget 15-20% of annual cost for ongoing calibration
9. ☐ Mandate quarterly performance reviews with independent measurement
10. ☐ Require independent validation before full commitment

---

## Answering the Original Question

**"If ShovelSense costs $200K/month, would there be a decent return on investment?"**

**No.**

- The technology has zero independent validation after 10+ years
- The economics require 7.3% grade improvement to break even — implausible without validation
- Better-validated alternatives exist at 1/6th the cost
- Your 20% bornite content eliminates the best-validated alternative (MRT), suggesting your deposit may be challenging for surface-based XRF as well
- Blast hole optimization can close most of the gap without any sensors

**The recommendation:** Invest $400-700K in blast hole optimization, then $800K in a PGNAA belt analyzer. This path costs $3.4M over 5 years (vs. $12M for ShovelSense) with higher probability of success.

If ShovelSense gets independent validation showing it works on mixed chalcopyrite-bornite porphyry deposits with quantified accuracy, revisit the decision. Until then, the answer is no.

---

## Dialectic Complete

Three rounds explored the question from every angle:

- **Round 1:** Established that surface-volume correlation is the key unknown; proposed measurement study
- **Round 2:** Discovered ShovelSense has no validation while alternatives do; reframed to "wrong technology, wrong order"
- **Round 3:** Quantified economics, found MRT bornite limitation, identified blast hole optimization as the best first step

The dialectic produced a clear recommendation that neither the Believer nor the Skeptic could have reached alone:

> Don't buy ShovelSense. Don't buy MRT alone. Optimize blast holes first, deploy PGNAA for ground truth, and only evaluate shovel-level sensing after you have empirical data from your own deposit.

This recommendation can be held at full conviction. It is not a hedge.
