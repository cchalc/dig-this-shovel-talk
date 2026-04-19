# Candidate G: Ground Condition — XRF Accuracy is Zone-Dependent

The debate between these monks proceeds as if "XRF accuracy at this deposit" is a single number—either good enough to justify deployment or not. This framing is false. The deposit's mineralogy, which both monks cite, guarantees that XRF accuracy varies systematically by ore type and spatial zone. The question is not "does XRF work?" but "where does XRF work?"

## The Physics of Variable Accuracy

The deposit's hypogene mineralization is 80% chalcopyrite (CuFeS₂) and 20% bornite (Cu₅FeS₄). These are not just different copper grades—they represent fundamentally different measurement environments for X-ray fluorescence.

Chalcopyrite contains 34.5% copper and 30.5% iron. Bornite contains approximately 63% copper with substantially lower iron content. This matters because iron creates a well-documented matrix effect: iron atoms absorb copper's characteristic X-rays before they reach the detector, causing systematic underestimation of copper grade. The effect is not random noise—it is a predictable bias proportional to iron concentration.

In a chalcopyrite-dominant zone, XRF will systematically under-read copper. In a bornite-rich zone, with less iron interference, XRF readings will more accurately reflect true copper content. The same instrument, same operator, same measurement protocol will produce different accuracy profiles depending on which ore type dominates the local geology.

This is not speculation. It is physics. Both monks had access to this mineralogical data. Neither applied it to the evaluation question.

## Why This Dissolves the Debate

Monk A argues that XRF reduces error versus blast-hole sampling alone, citing the ShovelSense literature. But the vendor's accuracy claims are aggregate statistics. If chalcopyrite zones show ±0.25% Cu error while bornite zones show ±0.08% Cu error, a "±0.15% average" obscures the operational reality. The shovel does not dig average ore—it digs specific zones.

Monk B argues that surface measurement cannot represent volumetric grade and that no independent validation exists. Both points may be true on average while false in specific contexts. A bornite zone with lower matrix interference and more homogeneous grade distribution might show strong surface-to-volume correlation. A chalcopyrite zone with high iron interference and supergene overprinting might show poor correlation. "The deposit" does not have a single validation status.

Both monks treated the deposit as a uniform measurement environment. The mineralogy they cited proves it is not. They debated at the wrong level of abstraction.

## The Practical Implication: Stratified Pilot Design

The correct experimental design stratifies by ore type:

**Phase 1:** Deploy XRF in bornite-dominant zones only. These represent 20% of the deposit but likely offer the best XRF accuracy due to lower iron interference. Run parallel validation against assay for 30 days. Establish zone-specific accuracy metrics.

**Phase 2:** Use chalcopyrite-dominant zones as controls, running conventional blast-hole sampling without XRF augmentation. Compare misallocation rates between XRF-guided and non-XRF zones.

**Phase 3:** If bornite-zone results justify the method, develop zone-specific calibration curves for chalcopyrite areas. Test whether iron-corrected measurements achieve acceptable accuracy.

This design answers the actual operational question: not "is XRF accurate?" but "where is XRF accurate enough to improve decisions?"

## Partial-Deployment ROI

If XRF works only in bornite zones, does 20% coverage justify $200K/month?

Assume the mine moves roughly 800,000 tonnes of ore monthly. At 20% bornite coverage, XRF-guided decisions would affect approximately 160,000 tonnes per month. Using the monks' misallocation baseline of 5-10% and assuming XRF halves this rate in bornite zones only:

- Monthly ore affected: 160,000 tonnes
- Misallocation reduction: 2.5-5% of affected volume = 4,000-8,000 tonnes/month
- At 0.32% Cu, $4/lb copper, ~70% recovery: ~$16-20/tonne marginal value for correct allocation
- Conservative monthly value recovery: $64K-$160K

At the floor estimate, partial deployment in favorable zones approaches break-even. At the higher estimate, it exceeds 2x ROI on an allocated-cost basis.

The ROI question is not "does $200K/month pencil out for the whole deposit?" It is "which zones generate positive ROI, and how do we sequence deployment?"

## Conclusion

The monks' debate assumed a uniform answer to a non-uniform question. XRF accuracy at this deposit is not a single number—it is a spatial function of mineralogy. The bornite zones offer favorable physics for measurement accuracy. The chalcopyrite zones present known interference challenges. A pilot study that ignores this heterogeneity will produce ambiguous results. A stratified pilot will produce actionable zone-specific guidance.

The ground truth is in the mineralogy. Neither monk looked closely enough to see it.

---

## Internal Standard Check

- ✓ Identifies a concrete fact that changes the frame (80/20 chalcopyrite/bornite split → different matrix effects)
- ✓ Level-shift is orthogonal to both monks (deposit-wide → zone-specific)
- ✓ Practical implication follows (stratified pilot by ore type)
