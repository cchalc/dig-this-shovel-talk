# Phase 6: Validation of S+G Combined Candidate

## The Candidate Under Test

**Core claim:** Before committing to $2.4M/year for ShovelSense, the mine should run a $50-90K stratified measurement study that:
1. Measures XRF surface-to-volume correlation by zone (chalcopyrite vs bornite)
2. Uses decision rules: R² > 0.6 = deploy, R² 0.4-0.6 = partial, R² < 0.4 = reject
3. If bornite zones show better correlation (lower Fe interference), consider partial deployment in those zones only

---

## Hostile Auditor's Attack

### Attack 1: The Paired Sample Problem is Fatal

The synthesis assumes you can get "paired XRF/assay samples from the same bucket loads." This is operationally naive.

XRF measures the **surface** of rocks in a truck bed. Assay measures a **pulverized composite** from the mill feed. These are fundamentally different sampling universes. To get a true paired sample, you would need to:

1. Halt the truck at the XRF scanner
2. Take a physical sample from the exact surface area the XRF measured
3. Send that specific sample to assay
4. Repeat hundreds of times per zone

This is not a $50-90K study. This is a multi-month operational disruption requiring dedicated sampling crews, chain-of-custody protocols, and statistical design expertise. The cost estimate appears to be fabricated without reference to actual mining sampling costs. A proper surface-to-volume correlation study at an operating copper mine would likely cost $200-400K minimum and require 6-12 months of data collection.

**Status: VALID ATTACK — cost estimate needs revision**

### Attack 2: The R² Thresholds Are Arbitrary

The synthesis claims R² > 0.6 = deploy, R² 0.4-0.6 = partial, R² < 0.4 = reject. Where do these numbers come from?

There is no citation. No reference to similar validation studies. No sensitivity analysis showing what happens at R² = 0.59 vs 0.61.

Worse: **R² is the wrong metric entirely.** What matters for truck diversion is **prediction accuracy at the decision boundary** (the cutoff grade). A model could have R² = 0.7 overall but catastrophically fail at the 0.3% Cu threshold where diversion decisions happen.

**Status: VALID ATTACK — metric needs refinement**

### Attack 3: Mineralogical Stratification Doesn't Exist at Bucket Scale

The synthesis claims bornite zones might show better XRF correlation due to lower Fe interference. This reveals a fundamental misunderstanding of porphyry copper deposits.

Chalcopyrite and bornite do not occur in cleanly separated "zones" at the 100-ton truck scale. They occur as **disseminated grains intermixed within the same rock mass**, often within the same hand sample. The supergene enrichment that produces bornite creates a vertical transition, not horizontal zones you can selectively mine.

A bucket of ore will contain both minerals. You cannot "deploy in bornite zones only" because there are no pure bornite zones at the operational scale.

**Status: PARTIALLY VALID — stratification concept needs geological refinement, but Fe content variation by zone is still real**

### Attack 4: "Partial Deployment" is Economically Incoherent

If XRF only works reliably in 20-30% of the deposit, what does "partial deployment" mean? MineSense's business model requires capital investment in scanning infrastructure. You cannot install 20% of a scanner. The fixed costs remain, but the value capture drops to a fraction.

The synthesis never addresses whether MineSense would even offer a partial deployment contract.

**Status: VALID ATTACK — needs MineSense pricing model clarification**

### Attack 5: Analysis Paralysis Accusation

Strip away the technical language and this synthesis says: "Don't decide yet. Do a study first."

That is not a resolution of the contradiction between the monks. It is a deferral.

**Status: REJECTED — the measurement study IS a decision; spending $75-400K to avoid a $1.2M mistake is rational, not paralysis**

### Attack 6: Reversibility Failure

The "zone-specific guidance based on mineralogical physics" claim cannot be traced to either monk's atomic decomposition. Neither monk discussed mineralogical stratification.

**Status: PARTIALLY VALID — the zone concept came from Ground (G) candidate material, which was derived from the briefing's 80/20 chalcopyrite/bornite split. Reversibility to briefing facts holds, but not to monk arguments directly.**

---

## Validation Monk's Assessment

### Verdict: Genuine Aufhebung, Not Compromise

**From Monk A's position (Believer):** The synthesis preserves and elevates the core insight. It says: "You're right that XRF *could* add value, but let's find out *where and how much* before committing $2.4M." The insight about information value is preserved; what's canceled is naivety about assuming vendor correlation studies transfer to this specific ore body.

**From Monk B's position (Skeptic):** The synthesis preserves and elevates the core insight. It operationalizes skepticism into a structured measurement protocol. What's canceled is the implicit assumption that skepticism means rejection. The decision rules encode the demand for evidence into executable criteria.

**One-Sidedness Check:** Passes. The synthesis doesn't secretly favor either position. If R² < 0.4 everywhere, Monk B "wins." If R² > 0.6 in all zones, Monk A "wins." But neither monk *actually* wins—the synthesis wins because both outcomes follow from its framework.

**Closure Test:** The synthesis can be stated without hedging: "We will deploy XRF exactly where empirical measurement proves it adds decision value, and nowhere else, with thresholds established before measurement to prevent motivated reasoning."

---

## Surviving Issues Requiring Refinement

1. **Cost estimate**: $50-90K is likely too low. Realistic range may be $150-300K for proper paired sampling protocol.

2. **Metric refinement**: Replace R² with **classification accuracy at cutoff grade** (0.32% Cu). The question isn't "how well does XRF predict grade overall?" but "how often does XRF correctly classify ore vs. waste near the cutoff?"

3. **Stratification reframe**: Instead of "bornite zones vs. chalcopyrite zones" (which may not exist at operational scale), stratify by:
   - Grade range (near-cutoff vs. clearly ore vs. clearly waste)
   - Depth/supergene zone (where Fe content actually varies)
   - Rock type/alteration facies

4. **Partial deployment clarification**: Before study, get MineSense's actual pricing model for partial vs. full deployment. If partial isn't economically viable, the decision simplifies to all-or-nothing.

---

## Refined Candidate S+G

**After incorporating valid attacks:**

The mine should run a measurement study (~$150-300K, 3-6 months) before committing to $2.4M/year:

1. **Metric**: Classification accuracy at 0.32% Cu cutoff, not R²
2. **Decision rules**:
   - Accuracy > 80% at cutoff → full deployment justified
   - Accuracy 70-80% → economic analysis required (does marginal improvement justify cost?)
   - Accuracy < 70% → reject (XRF not adding value over blast holes)
3. **Stratification**: By grade range and depth/alteration zone, not by mineral species
4. **Prerequisite**: Confirm MineSense's pricing model before study design

**The refined synthesis preserves the core insight:** measure before committing, with pre-established decision rules to prevent motivated reasoning. The attacks improved the operational realism without changing the fundamental recommendation.

---

## Internal Standard Check (Post-Validation)

- ✓ Cancels both monks' unjustified assumptions (automatic fusion / categorical rejection)
- ✓ Preserves both monks' valid insights (counterfactual framing / demand for verification)
- ✓ Elevates to measurable unknown with operationally realistic protocol
- ✓ Zone stratification refined to match geological reality
- ✓ Cost estimate revised upward to realistic range
- ✓ Metric refined from R² to classification accuracy at cutoff
