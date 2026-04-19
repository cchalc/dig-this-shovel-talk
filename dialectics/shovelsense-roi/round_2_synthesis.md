# Round 2 Synthesis: Four Directions Converge

## The Four Directions

| Direction | Core Question | Key Finding |
|-----------|---------------|-------------|
| **A: Technology Comparison** | Which sensing tech offers best ROI? | MRT (NextOre) has peer-reviewed validation; ShovelSense has none |
| **B: Baseline Assessment** | How bad is current grade control? | 15-25% misclassification typical; best-in-class achieves 8-15% |
| **C: Validation Gap** | Why no independent validation? | Abnormal for tech class; 35% posterior on claimed ROI |
| **D: Hybrid Architecture** | What's the optimal sensor stack? | Belt analyzer first (ground truth), then pilot XRF with calibration |

---

## The Convergent Insight

All four directions point to the same conclusion: **ShovelSense should not be evaluated first, and possibly not at all.**

### Why the convergence?

**Direction A** found that MRT has peer-reviewed validation at an actual copper mine (Kansanshi), while ShovelSense has zero independent validation. If you're going to spend money on sensing technology, start with the one that has evidence.

**Direction B** found that you can't evaluate ANY technology without knowing your baseline. If your F1 factor is already above 0.92, the ROI case for any sensor collapses. If it's below 0.85, even expensive sensors pay off quickly. The first step is assessment, not purchase.

**Direction C** found that the validation gap is a red flag, not industry norm. Comparable technologies (PGNAA, Tomra, MRT) have academic validation trails. MineSense's 10-year silence suggests results are inconsistent enough that independent analysis would be unflattering.

**Direction D** found that you need ground truth before you can calibrate any upstream sensor. A belt analyzer provides standalone value AND creates the measurement infrastructure to empirically validate whether XRF adds value at your specific deposit.

---

## The Reframed Decision

The original question was: "Should I buy ShovelSense at $200K/month?"

Round 1 reframed it to: "Measure the surface-volume correlation before committing."

Round 2 reframes it further: **"You're asking the wrong question about the wrong technology in the wrong order."**

### The Right Order

1. **Assess your baseline** (Direction B)
   - Pull 24 months of reconciliation data
   - Calculate your F1 factor and misclassification rate
   - Cost: Internal labor only (~$10-20K opportunity cost)
   - Timeline: 2-4 weeks

2. **If baseline is poor (F1 < 0.90, misclassification > 15%), deploy a belt analyzer first** (Direction D)
   - PGNAA or MRT on conveyor
   - Provides ground truth for ALL upstream decisions
   - Enables empirical validation of any shovel-mounted sensor
   - Cost: ~$800K capital or lease equivalent
   - Timeline: 6-12 months to deploy and calibrate

3. **With belt data in hand, pilot XRF IF AND ONLY IF:**
   - Belt data shows recoverable misclassification at truck-loading stage
   - Surface-volume correlation can be measured against belt ground truth
   - The $200K/month cost is justified by marginal improvement over belt-only
   - Cost: $600K/year for 2-3 shovel pilot
   - Timeline: 12-18 months after belt deployment

4. **Consider MRT or improved blast holes instead of XRF** (Direction A)
   - MRT has independent validation ShovelSense lacks
   - Improved blast hole protocols may close the gap at lower cost
   - NextOre should be contacted for trial feasibility

---

## What Changed from Round 1

| Round 1 | Round 2 |
|---------|---------|
| Measure surface-volume correlation before committing | Measure your BASELINE before evaluating any technology |
| ShovelSense might work in some zones | ShovelSense has the weakest evidence of any option |
| $150-300K measurement study | Deploy belt analyzer (~$800K) for ground truth FIRST |
| Binary: deploy or reject ShovelSense | Sequence: baseline → belt → pilot XRF (maybe) |
| Surface-volume correlation is the key unknown | Your current misclassification rate is the key unknown |

---

## The Bottom Line

**Don't buy ShovelSense.**

Not because it doesn't work — it might work at some deposits. But because:

1. **You don't know your baseline.** If current grade control is already 90% accurate, no sensor technology delivers ROI at $200K/month.

2. **Better-validated alternatives exist.** MRT has peer-reviewed validation at a copper mine. ShovelSense has zero independent validation after 10+ years.

3. **You need ground truth first.** A belt analyzer provides the measurement infrastructure to validate whether ANY shovel-mounted sensor adds value at your specific deposit.

4. **The validation gap is a red flag.** When comparable technologies have academic validation trails and your target technology doesn't, that's information.

If you must evaluate ShovelSense, do it AFTER deploying a belt analyzer that can provide ground truth. Then you'll have empirical data on whether XRF surface measurements correlate with bulk grade at YOUR deposit, measured against independent verification.

---

## Recommended Next Steps

| Step | Action | Cost | Timeline |
|------|--------|------|----------|
| 1 | Internal baseline assessment (F1 factor, misclassification rate) | ~$15K labor | 2-4 weeks |
| 2 | Contact NextOre for MRT trial feasibility | Free | 1-2 weeks |
| 3 | Request Thermo Fisher PGNAA specifications | Free | 1-2 weeks |
| 4 | Engage geostatistics consultant for blast hole optimization | ~$50K | 2-3 months |
| 5 | If baseline is poor AND belt analyzer is deployed: pilot XRF with belt calibration | ~$800K + $600K/yr | 18-24 months |

**Total to validate properly: ~$1.5M over 2 years**
**Cost of deploying ShovelSense without validation: $2.4M/year for uncertain ROI**

The slower path is the cheaper path if it prevents a bad decision.

---

## Internal Standard Check

Round 2 synthesis succeeds if:
- ✓ It integrates insights from all four directions (technology comparison, baseline, validation gap, hybrid architecture)
- ✓ It produces a more specific recommendation than Round 1
- ✓ It changes the decision frame, not just the answer
- ✓ It's actionable (specific steps with costs and timelines)
- ✓ It can be believed at full conviction (not a hedge)

The synthesis has closure: "Deploy belt analyzer first, assess your baseline, consider MRT before XRF, and only pilot ShovelSense with empirical ground truth" is a position that can be argued without hedging.
