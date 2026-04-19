# Monk A: The XRF Believer

## The Ontology of Decision-Point Measurement

The fundamental error in evaluating ShovelSense is asking "how accurate is XRF?" when the question that matters is "does this measurement reduce decision error at the decision point?" These are not the same question. The first treats accuracy as an abstract property of measurement systems. The second treats measurement as a tool for improving outcomes under uncertainty.

A truck leaves a shovel carrying 100 tonnes of material. That material will either go to the crusher or the waste dump. This decision will be made. The only question is: what information will inform it? Today, that decision rests on blast hole samples taken days or weeks earlier, interpolated across a block model that treats the bucket's contents as a statistical abstraction. ShovelSense offers something different: a measurement taken at the moment of the decision, on the actual material being routed.

The ontological claim is this: **location in the decision process matters more than absolute precision.** A measurement that's 80% correlated with true grade, applied at the point where routing decisions are made, delivers more value than a measurement that's 95% correlated but applied after the truck has already committed to a destination. The belt analyzers using neutron activation achieve superior bulk measurement, but they measure ore that has already been routed. The information arrives too late. ShovelSense measures at the only point in the process where truck-by-truck diversion is physically possible.

This is the proper way to think about real-time grade measurement: not as a replacement for perfect information, but as a reduction in decision error compared to the counterfactual of blast hole data alone.

---

## The Skeptic's Strongest Case

The skeptic's argument deserves its full weight. It runs as follows:

XRF penetrates only micrometers into rock surfaces, essentially measuring a film of material rather than the bulk volume. A bucket of heterogeneous copper porphyry ore contains a grade distribution, not a grade value. That distribution varies at millimeter scale (individual veins), centimeter scale (vein density), and meter scale (alteration zonation). The surface that happens to face the XRF sensor during loading bears no systematic relationship to the volumetric average of the entire bucket load.

The skeptic points to the industry's own revealed preference: major conveyor belt analyzers use PGNAA/PFTNA (neutron activation), not XRF, specifically because neutron techniques provide penetrative bulk measurement. Thermo Fisher states explicitly that surface analysis technologies "measure limited depths and surface areas that may not be representative of the entire amount of material on the belt." When billion-dollar processing plants need to know copper grade, they don't trust XRF. Why should a mine operator trust it at the shovel?

Furthermore, the skeptic notes the absence of independent validation. MineSense's accuracy claims originate from MineSense-commissioned studies and partner announcements. No peer-reviewed study specifically validates ShovelSense's claimed performance. The Whittle Consulting economic assessment was commissioned by MineSense. The CIM Magazine articles cite MineSense-provided data. This is not scientific evidence; it is marketing.

The matrix effects compound the problem. In this deposit, 80% of copper occurs as chalcopyrite (CuFeS2), which contains 30.5% iron. Iron absorbs copper K-alpha X-rays. Spatial variability in the chalcopyrite-to-bornite ratio across a bucket creates systematic measurement variations that cannot be calibrated out without knowing the ratio you're trying to measure.

I acknowledge the force of these arguments. The skeptic is not wrong about the physics. XRF does measure surfaces. Porphyry deposits are heterogeneous. Independent validation is lacking. These are facts.

---

## Why the Skeptic's Framing Is Wrong

The skeptic compares XRF to perfect information and finds XRF wanting. But perfect information is not the counterfactual. The counterfactual is blast hole sampling.

Blast hole sampling has, as the AusIMM documented in 2008, "acquired an extremely bad reputation for the last 50 years." The errors are systematic and well-documented: delimitation biases from single assays representing entire hole lengths, extraction biases from loss of fines to voids and cracks, weighting biases from pile segregation and operator-dependent sampling. One case study found bias amounting to 70% of total observable grade variability. Research from a large copper open pit mine in Chile documents $134 million lost over 10 years due to suboptimal blast hole-based grade control. Up to 50% of valuable ore can be lost or diluted due to poor sampling resolution or delays in decision-making.

The skeptic treats "heterogeneity error" as fatal to XRF. But heterogeneity error affects all sampling methods, including blast holes. The question is not whether XRF eliminates uncertainty but whether XRF combined with blast holes reduces uncertainty compared to blast holes alone. This is a question about information gain, not absolute accuracy.

The skeptic frames surface measurement as categorically incapable of representing volume. But if this were true, all surface sampling in mineral exploration would be worthless, exploration drill core assays would be meaningless, and the entire edifice of resource estimation would collapse. It doesn't. The relationship between surface and volume is a question of correlation, not identity. Statistical averaging of multiple measurements is established methodology for addressing heterogeneity, and ongoing research continues to refine adaptive averaging algorithms for inhomogeneous materials.

ShovelSense does not take one measurement. It takes multiple measurements across multiple surfaces during the loading process, then applies site-specific calibration against reconciled mill feed. The relevant question is whether this multi-measurement approach, calibrated to actual recovery data, correlates with volumetric grade. The published academic literature reports R-squared values of 0.84 and classification accuracies of 75-93% depending on cutoff grade. These are not perfect correlations. They are useful correlations.

---

## Information Value Theory

Consider a simplified decision problem. A truck carrying material with true grade 0.4% Cu (above the 0.32% cutoff) should go to the crusher. Under blast hole data alone, suppose there's a 15% probability of misclassifying this load as waste. Under ShovelSense plus blast holes, suppose misclassification drops to 8%. The value of ShovelSense is not measured by its absolute accuracy but by this 7-percentage-point reduction in decision error.

Information value theory quantifies this precisely. The expected value of information depends on:
1. The prior probability distribution of grade
2. The decision rules applied to measurements
3. The conditional probability that measurement X indicates true grade Y
4. The economic consequences of correct and incorrect decisions

A measurement that's 80% correlated with true grade, applied at the decision point, beats a measurement that's 95% correlated but applied after the decision is irreversible. Belt analyzers achieve the 95% correlation, but they cannot reroute trucks. ShovelSense achieves the 80% correlation (or whatever the actual figure is post-calibration), and it can reroute trucks.

The skeptic asks "is XRF accurate?" The correct question is "does XRF reduce decision error compared to the counterfactual?" If blast hole sampling introduces 30-50% precision error (documented), and XRF at the shovel provides an independent measurement with even 60-70% correlation to volumetric grade, the combined information is strictly better than blast holes alone. This is basic information theory. Two imperfect signals, when independent, can be fused to produce a more reliable estimate than either alone.

---

## Pushing to the Extreme

If surface measurement truly cannot represent volumetric grade, then exploration geology is pseudoscience. Every exploration drill core assayed in a lab represents surface measurement of a tiny volume. Every resource estimate built on assay data is built on the assumption that measured surfaces correlate with unmeasured volumes. The entire mining industry operates on this assumption.

The skeptic cannot have it both ways. Either surface measurements can be statistically representative of volumes—in which case XRF at the shovel is at least potentially useful—or they cannot, in which case the $134 million Chilean copper mine lost to poor grade control is not an aberration but an inevitability, and all grade control is theater.

The skeptic retreats to "yes, but XRF is surface-only in a different way than drill core." This is true but irrelevant. The question remains: what is the correlation between measured surfaces and volumetric grade? For drill core, we accept correlations in the 0.8-0.9 range as sufficient for resource estimation. Published XRF classification accuracies of 75-93% sit in exactly this range.

At 0.32% Cu cutoff with grades ranging to 2.1%, the signal-to-noise ratio favors detection. The grade differential between ore (>0.32% Cu) and waste (<0.32% Cu) is significant. Even surface-biased measurement provides actionable signal when the contrast is this large. The difficult cases are near-cutoff loads where true grade hovers around 0.32%. But these are precisely the loads where blast hole interpolation is also most uncertain. The question is whether ShovelSense plus blast holes better resolves these marginal cases than blast holes alone.

Recent sensor-based sorting case studies demonstrate clear economic value. A pilot-scale trial of magnetic resonance sensors achieved 0.028% copper precision following a year-long calibration period. Field trials at copper operations show revenue increases of 12% with identical product quality. Multi-sensor integration using both MR and PGNAA shows enhanced Net Smelter Return compared to single-sensor approaches. The industry is moving toward sensor fusion, not sensor skepticism.

---

## Economic Calculation

The economics are straightforward. At $200,000/month, the technology must deliver $400,000/month at 2x ROI or $800,000/month at 4x ROI.

Assume the mine moves 10 million tonnes per year (approximately 833,000 tonnes per month). At 0.32% Cu cutoff and $4/lb copper, a tonne of ore contains roughly $28 of copper value (0.0032 x 2,205 lbs x $4). The difference between routing correctly versus incorrectly is this $28/tonne, minus processing costs if sent to crusher, plus haulage cost differential.

To achieve $400,000/month benefit at $28/tonne marginal value, you need to correctly reroute approximately 14,000 tonnes per month that would otherwise be misclassified. At 833,000 tonnes/month, this is a 1.7% improvement in classification accuracy.

Is 1.7% improvement plausible? MineSense reports truck reclassification rates of 5.9% ore-to-waste and 7.2% waste-to-ore across nine copper mines. Even if half of these reclassifications are false positives that don't improve outcomes, the net improvement would exceed the 1.7% threshold for 2x ROI.

To achieve $800,000/month (4x ROI), you need to correctly reroute approximately 28,000 tonnes per month, a 3.4% improvement. The MineSense data suggests this is achievable at high coverage rates.

The skeptic will note that MineSense data is not independently verified. This is true. But the required improvement for positive ROI is modest. A 2% net improvement in classification accuracy pays for the system at 2x. Given documented blast hole errors of 30-50%, and XRF classification accuracies of 75-93% in academic studies, a 2% net improvement is not merely plausible but conservative.

The deeper point: the risk is asymmetric. If ShovelSense works as claimed, the mine gains $400,000-$800,000/month. If it fails to deliver, the mine loses $200,000/month. A 6-month trial with exit clause costs $1.2M maximum downside against $2.4-$4.8M potential annualized upside. The expected value calculation favors deployment even under uncertainty about exact performance.

---

## Conclusion

ShovelSense will deliver positive ROI for this customer's copper porphyry mine. Not because XRF is as accurate as neutron-based bulk measurement (it isn't). Not because surface measurement equals volumetric grade (it doesn't). Not because MineSense's claims are independently verified (they aren't).

ShovelSense will deliver because it measures at the decision point. Because even imperfect real-time measurement combined with blast hole data beats blast hole data alone. Because 75-93% classification accuracy, applied to every truck, exceeds the precision of 30-50% error-prone blast hole sampling interpolated across a block model. Because the 0.32% Cu cutoff against grades ranging to 2.1% creates sufficient signal-to-noise ratio for actionable decisions.

The skeptic demands certainty before action. But mining is a business of managing uncertainty, not eliminating it. Blast hole sampling is uncertain. Block model interpolation is uncertain. Mill recovery is uncertain. The question is not whether ShovelSense introduces uncertainty but whether it reduces net decision error. On the physics, on the information theory, on the economics, the answer is yes.

Deploy the system. Calibrate to site conditions. Reconcile against mill feed. Measure the actual improvement. The technology is sound. The ROI will follow.
