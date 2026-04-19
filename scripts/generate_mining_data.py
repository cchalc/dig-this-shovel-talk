"""
Generate synthetic mining data simulating ShovelSense XRF measurements and truck diversions.

Based on the ShovelSense ROI dialectical analysis, this generates data for a
heterogeneous copper porphyry deposit with the following characteristics:

Deposit Parameters (from Round 1 Context Briefing):
- Mineralogy: ~80% chalcopyrite (CuFeS₂), ~20% bornite (Cu₅FeS₄)
- Cutoff grade: 0.32% Cu
- Average head grade: 0.45% Cu
- Grade range: Waste to 2.1% Cu
- Monthly throughput: 800,000 tonnes

Geological Zonation:
- BORNITE_CORE: High-grade bornite-rich center (higher Cu, lower Fe)
- CHALCOPYRITE_ZONE: Main ore zone with 80% chalcopyrite
- PYRITE_HALO: Outer zone with elevated pyrite, lower Cu
- SUPERGENE: Secondary enrichment zone
- LEACHED_CAP: Near-surface oxidized zone
- WASTE_ZONE: Sub-economic material

XRF Sensor Characteristics (from Round 1):
- Detection limits: <10 ppm for Cu
- Penetration depth: Surface only (micrometers)
- Classification accuracy: 75-93% depending on zone
- Matrix effects: Fe absorbs Cu X-rays (chalcopyrite has 30.5% Fe)

The data simulates the ~11% diversion rate claimed in the ShovelSense white paper,
split into:
- Ore from Waste: ~6.4% (403/6270 trucks)
- Waste from Ore: ~4.7% (294/6270 trucks)
"""
import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Tuple

# =============================================================================
# CONFIGURATION - Based on Dialectical Analysis Parameters
# =============================================================================
CATALOG = os.environ.get("CATALOG", "cjc_aws_workspace_catalog")
SCHEMA = os.environ.get("SCHEMA", "shovelsense")
VOLUME_PATH = f"/Volumes/{CATALOG}/{SCHEMA}/raw_data"

# Data generation parameters
SEED = 42
N_DAYS = 80  # Match the case study period
N_SHOVELS = 3
N_TRUCKS = 15
BUCKETS_PER_TRUCK = 5  # Average buckets to fill a truck
TRUCKS_PER_DAY_PER_SHOVEL = 80  # ~80 trucks/day/shovel

# =============================================================================
# ECONOMIC PARAMETERS (from Round 3, Direction C)
# =============================================================================
MONTHLY_THROUGHPUT_TONNES = 800_000
COPPER_PRICE_PER_LB = 4.00
COPPER_PRICE_PER_TONNE = 8820  # $4/lb * 2205 lb/tonne
METALLURGICAL_RECOVERY = 0.85  # 85% recovery
SHOVELSENSE_MONTHLY_COST = 200_000  # $200K/month

# =============================================================================
# GRADE PARAMETERS (from Round 1 Context Briefing)
# Heterogeneous copper porphyry deposit
# =============================================================================
CU_CUTOFF = 0.32  # Cu% cutoff for ore vs waste (changed from 0.20%)
CU_MEAN_HEAD_GRADE = 0.45  # Target average head grade
CU_MAX_GRADE = 2.1  # Maximum observed grade

# Mineralogy breakdown
CHALCOPYRITE_PCT = 0.80  # 80% chalcopyrite (CuFeS₂: 34.5% Cu, 30.5% Fe)
BORNITE_PCT = 0.20  # 20% bornite (Cu₅FeS₄: 63% Cu, lower Fe)

# Diversion rates (based on white paper claims)
TARGET_DIVERSION_RATE = 0.11  # ~11% of trucks diverted
ORE_FROM_WASTE_RATE = 0.064  # 6.4% of trucks (403/6270)
WASTE_FROM_ORE_RATE = 0.047  # 4.7% of trucks (294/6270)

# Date range - last 80 days to match case study
END_DATE = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
START_DATE = END_DATE - timedelta(days=N_DAYS)

# =============================================================================
# GEOLOGICAL DOMAIN CONFIGURATION
# Reflecting zonation pattern: Bornite core → Chalcopyrite → Pyrite halo
# =============================================================================
GEOLOGICAL_DOMAINS = {
    'BORNITE_CORE': {
        'cu_mean': 0.85,  # High grade bornite-rich
        'cu_std': 0.25,
        'fe_mean': 4.5,   # Lower Fe (bornite has less Fe than chalcopyrite)
        'chalcopyrite_ratio': 0.30,  # More bornite here
        'bornite_ratio': 0.70,
        'surface_volume_correlation': 0.75,  # Higher correlation (more disseminated)
        'probability': 0.10
    },
    'CHALCOPYRITE_ZONE': {
        'cu_mean': 0.55,
        'cu_std': 0.20,
        'fe_mean': 6.5,   # Higher Fe due to chalcopyrite (30.5% Fe)
        'chalcopyrite_ratio': 0.85,
        'bornite_ratio': 0.15,
        'surface_volume_correlation': 0.60,  # Moderate correlation
        'probability': 0.30
    },
    'PYRITE_HALO': {
        'cu_mean': 0.25,
        'cu_std': 0.15,
        'fe_mean': 8.0,   # High Fe from pyrite
        'chalcopyrite_ratio': 0.90,
        'bornite_ratio': 0.10,
        'surface_volume_correlation': 0.50,  # Lower correlation (vein-controlled)
        'probability': 0.20
    },
    'SUPERGENE': {
        'cu_mean': 0.65,  # Secondary enrichment
        'cu_std': 0.30,
        'fe_mean': 5.0,
        'chalcopyrite_ratio': 0.60,
        'bornite_ratio': 0.40,
        'surface_volume_correlation': 0.55,
        'probability': 0.15
    },
    'LEACHED_CAP': {
        'cu_mean': 0.18,  # Near-surface oxidized
        'cu_std': 0.12,
        'fe_mean': 7.0,
        'chalcopyrite_ratio': 0.50,
        'bornite_ratio': 0.50,
        'surface_volume_correlation': 0.45,
        'probability': 0.10
    },
    'WASTE_ZONE': {
        'cu_mean': 0.08,
        'cu_std': 0.05,
        'fe_mean': 4.0,
        'chalcopyrite_ratio': 0.80,
        'bornite_ratio': 0.20,
        'surface_volume_correlation': 0.70,  # More homogeneous
        'probability': 0.15
    }
}


# =============================================================================
# GENERATION FUNCTIONS
# =============================================================================
def generate_block_model(n_blocks: int = 500) -> pd.DataFrame:
    """
    Generate a geological block model reflecting copper porphyry zonation.

    From Round 2, Direction D (Optimal Sensor Architecture):
    - Multi-scale grade variability (mm to deposit scale)
    - Gradational ore/waste boundaries
    - Within-bucket coefficient of variation: 40-80%
    """
    np.random.seed(SEED)

    # Extract domain names and probabilities
    domain_names = list(GEOLOGICAL_DOMAINS.keys())
    domain_probs = [GEOLOGICAL_DOMAINS[d]['probability'] for d in domain_names]

    blocks = []
    for i in range(n_blocks):
        # Random location in pit
        easting = np.random.uniform(500000, 501000)
        northing = np.random.uniform(6000000, 6001000)
        bench = np.random.choice([1, 2, 3, 4, 5], p=[0.15, 0.25, 0.30, 0.20, 0.10])
        elevation = 3500 - (bench * 15)  # 15m bench height

        # Geological domain with radial zonation tendency
        # Bornite core more likely at center of deposit
        distance_from_center = np.sqrt((easting - 500500)**2 + (northing - 6000500)**2)

        # Adjust probabilities based on distance (bornite core at center)
        adjusted_probs = domain_probs.copy()
        if distance_from_center < 200:  # Near center
            adjusted_probs[0] *= 2.5  # Boost BORNITE_CORE
            adjusted_probs[1] *= 1.5  # Boost CHALCOPYRITE_ZONE
        elif distance_from_center > 400:  # Outer zones
            adjusted_probs[2] *= 2.0  # Boost PYRITE_HALO
            adjusted_probs[5] *= 1.5  # Boost WASTE_ZONE

        # Normalize
        adjusted_probs = np.array(adjusted_probs) / sum(adjusted_probs)
        domain = np.random.choice(domain_names, p=adjusted_probs)
        domain_config = GEOLOGICAL_DOMAINS[domain]

        # Is this a barren dyke? (causes ore-to-waste diversions)
        # From Round 1: Dyke intrusions are a known source of misclassification
        is_dyke = np.random.random() < 0.05  # 5% of blocks are dyke intrusions

        # Grade based on domain (log-normal distribution)
        if is_dyke:
            cu_grade = np.random.normal(0.02, 0.01)  # Very low grade
        else:
            cu_grade = np.random.lognormal(
                np.log(domain_config['cu_mean']),
                domain_config['cu_std'] / domain_config['cu_mean']
            )

        cu_grade = max(0, min(cu_grade, CU_MAX_GRADE))  # Clamp to realistic range

        # Fe grade (affected by mineralogy - chalcopyrite has 30.5% Fe)
        fe_grade = np.random.lognormal(np.log(domain_config['fe_mean']), 0.3)

        # Mineralogy percentages for this block
        chalcopyrite_pct = domain_config['chalcopyrite_ratio'] * 100 + np.random.normal(0, 5)
        bornite_pct = 100 - chalcopyrite_pct
        chalcopyrite_pct = max(0, min(100, chalcopyrite_pct))
        bornite_pct = max(0, min(100, bornite_pct))

        # Blast movement (causes misclassification)
        # From AusIMM 2008: Blast movement is a major source of grade control error
        blast_movement = np.random.exponential(2.0)  # Average 2m movement

        # Surface-volume correlation estimate for this block
        # From Round 1: This is the critical unknown that determines XRF value
        surface_volume_corr = domain_config['surface_volume_correlation'] + np.random.normal(0, 0.1)
        surface_volume_corr = max(0.2, min(0.95, surface_volume_corr))

        # Planned classification based on cutoff
        planned_class = 'ORE' if cu_grade >= CU_CUTOFF else 'WASTE'

        blocks.append({
            'block_id': f'BLK-{i:05d}',
            'bench': bench,
            'easting': round(easting, 2),
            'northing': round(northing, 2),
            'elevation': round(elevation, 2),
            'planned_cu_grade': round(cu_grade, 4),
            'planned_fe_grade': round(fe_grade, 2),
            'planned_classification': planned_class,
            'geological_domain': domain,
            'is_dyke': is_dyke,
            'blast_movement_m': round(blast_movement, 2),
            # New fields from dialectical analysis
            'chalcopyrite_pct': round(chalcopyrite_pct, 1),
            'bornite_pct': round(bornite_pct, 1),
            'surface_volume_correlation': round(surface_volume_corr, 3),
            'nugget_effect_variance': round(np.random.uniform(0.3, 0.8), 2),  # From geostatistics
            'vein_density_class': np.random.choice(['LOW', 'MEDIUM', 'HIGH'], p=[0.3, 0.5, 0.2])
        })

    return pd.DataFrame(blocks)


def generate_fleet() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Generate shovel and truck fleet data."""
    np.random.seed(SEED + 1)

    # Shovels with ShovelSense equipment
    shovels = []
    shovel_types = ['ELECTRIC_ROPE', 'HYDRAULIC', 'FRONT_END_LOADER']
    for i in range(N_SHOVELS):
        shovels.append({
            'shovel_id': f'SHV-{i+1:02d}',
            'shovel_type': shovel_types[i % len(shovel_types)],
            'bucket_capacity_m3': np.random.choice([40, 50, 60]),
            'minesense_equipped': True,
            'sensor_heads': np.random.choice([2, 3, 4]),
            'commissioned_date': (START_DATE - timedelta(days=np.random.randint(30, 365))).strftime('%Y-%m-%d'),
            # XRF sensor specifications
            'xrf_detector_type': 'SDD',  # Silicon Drift Detector
            'detection_limit_ppm': 10,   # From Round 1: <10 ppm for Cu
            'penetration_depth_mm': 0.1  # Surface only (micrometers)
        })

    # Trucks
    trucks = []
    for i in range(N_TRUCKS):
        trucks.append({
            'truck_id': f'TRK-{i+1:03d}',
            'truck_model': np.random.choice(['CAT 797F', 'KOMATSU 980E', 'LIEBHERR T284']),
            'payload_capacity_tonnes': np.random.choice([320, 360, 400]),
            'fms_system': 'MODULAR_DISPATCH'
        })

    return pd.DataFrame(shovels), pd.DataFrame(trucks)


def generate_bucket_measurements(
    block_model: pd.DataFrame,
    shovels: pd.DataFrame,
    trucks: pd.DataFrame
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Generate XRF bucket measurements and truck load aggregations.

    This simulates what ShovelSense would produce, incorporating:
    - Surface-only XRF measurement (from Round 1: penetration depth <1mm)
    - Matrix effects (Fe absorbing Cu X-rays in chalcopyrite)
    - Heterogeneity error (surface may not represent volume)
    - Measurement noise and sensor failures
    """
    np.random.seed(SEED + 2)

    bucket_data = []
    truck_data = []

    shovel_ids = shovels['shovel_id'].tolist()
    truck_ids = trucks['truck_id'].tolist()
    block_ids = block_model['block_id'].tolist()

    # Create lookup for block properties
    block_lookup = block_model.set_index('block_id').to_dict('index')

    measurement_id = 0
    load_id = 0

    for day_offset in range(N_DAYS):
        current_date = START_DATE + timedelta(days=day_offset)

        # Reduced activity on weekends
        daily_multiplier = 0.7 if current_date.weekday() >= 5 else 1.0

        for shovel_id in shovel_ids:
            n_trucks_today = int(TRUCKS_PER_DAY_PER_SHOVEL * daily_multiplier * np.random.normal(1, 0.1))

            for truck_num in range(n_trucks_today):
                truck_id = np.random.choice(truck_ids)

                # Select block being mined (with some spatial continuity)
                block_id = np.random.choice(block_ids)
                block = block_lookup[block_id]

                # Generate bucket measurements for this truck load
                n_buckets = np.random.randint(4, 7)  # 4-6 buckets per truck
                bucket_grades = []

                for bucket_num in range(n_buckets):
                    # Base grade from block model
                    base_cu = block['planned_cu_grade']
                    surface_corr = block['surface_volume_correlation']

                    # Simulate the surface-volume correlation problem
                    # From Round 1: "The relationship between multi-surface XRF readings
                    # and true volumetric grade of a heterogeneous bucket load is
                    # NOT well-characterized"

                    # The actual grade in the bucket (what we're trying to measure)
                    if block['is_dyke']:
                        actual_cu = np.random.normal(0.02, 0.01)
                    elif block['blast_movement_m'] > 2:
                        # Blast movement causes material mixing
                        shift_magnitude = block['blast_movement_m'] / 5.0
                        if block['planned_classification'] == 'ORE':
                            bias = -0.08  # Tend to dilute ore
                        else:
                            bias = 0.08   # Tend to enrich waste
                        actual_cu = base_cu + bias + np.random.normal(0, 0.15 * shift_magnitude)
                    elif np.random.random() < 0.15:
                        # ~15% of buckets have significant grade variance from model
                        # This drives the ~11% truck diversion rate
                        if block['planned_classification'] == 'ORE':
                            actual_cu = np.random.normal(CU_CUTOFF - 0.15, 0.08)
                        else:
                            actual_cu = np.random.normal(CU_CUTOFF + 0.25, 0.10)
                    else:
                        actual_cu = base_cu + np.random.normal(0, 0.05)

                    actual_cu = max(0, actual_cu)

                    # XRF surface measurement
                    # From Round 1: "XRF penetration depth: <1mm in copper sulfide ore"
                    # The surface sample may not represent the volume

                    # Heterogeneity error: deviation based on surface-volume correlation
                    heterogeneity_error = np.random.normal(0, (1 - surface_corr) * 0.1)

                    # Matrix effect: Fe absorbs Cu X-rays
                    # Chalcopyrite (30.5% Fe) causes more absorption than bornite
                    fe_absorption_factor = 1 - (block['chalcopyrite_pct'] / 100 * 0.03)

                    # XRF measurement with all error sources
                    xrf_noise = np.random.normal(0, 0.02)  # ~2% measurement error
                    measured_cu = (actual_cu + heterogeneity_error) * fe_absorption_factor + xrf_noise
                    measured_cu = max(0, measured_cu)

                    # XRF confidence based on measurement conditions
                    # Lower confidence in high-Fe (chalcopyrite) zones due to matrix effects
                    base_confidence = 0.92
                    fe_penalty = (block['chalcopyrite_pct'] - 50) / 100 * 0.05
                    vein_penalty = 0.03 if block['vein_density_class'] == 'HIGH' else 0
                    xrf_confidence = base_confidence - fe_penalty - vein_penalty + np.random.normal(0, 0.02)
                    xrf_confidence = max(0.70, min(0.99, xrf_confidence))

                    # Generate timestamp within shift
                    shift_hour = np.random.choice([7, 8, 9, 10, 11, 14, 15, 16, 17, 18])
                    timestamp = current_date.replace(
                        hour=shift_hour,
                        minute=np.random.randint(0, 60),
                        second=np.random.randint(0, 60)
                    )

                    bucket_data.append({
                        'measurement_id': f'XRF-{measurement_id:08d}',
                        'timestamp': timestamp.isoformat(),
                        'shovel_id': shovel_id,
                        'bucket_number': bucket_num + 1,
                        'truck_id': truck_id,
                        'block_id': block_id,
                        'cu_grade_pct': round(measured_cu, 4),
                        'fe_grade_pct': round(np.random.lognormal(np.log(block['planned_fe_grade']), 0.15), 2),
                        'zn_grade_ppm': round(np.random.lognormal(np.log(100), 0.5), 1),
                        'as_grade_ppm': round(np.random.lognormal(np.log(50), 0.6), 1),
                        'laser_fill_level_pct': round(np.random.uniform(85, 100), 1),
                        'xrf_confidence': round(xrf_confidence, 3),
                        'sensor_head_1_active': True,
                        'sensor_head_2_active': np.random.random() > 0.05,  # 5% sensor failure
                        # New fields from dialectical analysis
                        'matrix_effect_factor': round(fe_absorption_factor, 3),
                        'heterogeneity_error_est': round(abs(heterogeneity_error), 4),
                        'geological_domain': block['geological_domain']
                    })

                    bucket_grades.append(measured_cu)
                    measurement_id += 1

                # Aggregate to truck load
                avg_cu = np.mean(bucket_grades)

                # Classification logic using the 0.32% Cu cutoff
                planned_class = block['planned_classification']
                ss_class = 'ORE' if avg_cu >= CU_CUTOFF else 'WASTE'

                # Determine diversion type
                if planned_class == ss_class:
                    diversion_type = 'ALIGNED'
                    destination = 'CRUSHER' if ss_class == 'ORE' else 'WASTE_DUMP'
                elif planned_class == 'WASTE' and ss_class == 'ORE':
                    diversion_type = 'ORE_FROM_WASTE'
                    destination = 'CRUSHER'  # Diverted to crusher
                else:
                    diversion_type = 'WASTE_FROM_ORE'
                    destination = 'WASTE_DUMP'  # Diverted to waste

                # Payload with realistic variation
                payload = np.random.uniform(300, 380)

                # Estimated copper content
                estimated_cu_tonnes = payload * avg_cu / 100

                truck_data.append({
                    'load_id': f'LOAD-{load_id:07d}',
                    'timestamp': timestamp.isoformat(),
                    'truck_id': truck_id,
                    'shovel_id': shovel_id,
                    'block_id': block_id,
                    'n_buckets': n_buckets,
                    'avg_cu_grade_pct': round(avg_cu, 4),
                    'avg_fe_grade_pct': round(np.mean([b['fe_grade_pct'] for b in bucket_data[-n_buckets:]]), 2),
                    'planned_classification': planned_class,
                    'shovelsense_classification': ss_class,
                    'diversion_type': diversion_type,
                    'destination': destination,
                    'payload_tonnes': round(payload, 1),
                    'cycle_time_minutes': round(np.random.exponential(25) + 15, 1),
                    # New fields
                    'estimated_cu_tonnes': round(estimated_cu_tonnes, 4),
                    'geological_domain': block['geological_domain'],
                    'surface_volume_correlation': round(block['surface_volume_correlation'], 3),
                    'avg_xrf_confidence': round(np.mean([b['xrf_confidence'] for b in bucket_data[-n_buckets:]]), 3)
                })

                load_id += 1

    return pd.DataFrame(bucket_data), pd.DataFrame(truck_data)


def generate_shift_summaries(truck_loads: pd.DataFrame) -> pd.DataFrame:
    """Generate shift-level summary statistics."""
    truck_loads['date'] = pd.to_datetime(truck_loads['timestamp']).dt.date
    truck_loads['shift'] = pd.to_datetime(truck_loads['timestamp']).dt.hour.apply(
        lambda h: 'DAY' if 6 <= h < 18 else 'NIGHT'
    )

    summaries = truck_loads.groupby(['date', 'shift', 'shovel_id']).agg({
        'load_id': 'count',
        'avg_cu_grade_pct': 'mean',
        'payload_tonnes': 'sum',
        'estimated_cu_tonnes': 'sum',
        'diversion_type': lambda x: (x != 'ALIGNED').sum(),
        'surface_volume_correlation': 'mean',
        'avg_xrf_confidence': 'mean'
    }).reset_index()

    summaries.columns = ['date', 'shift', 'shovel_id', 'n_trucks', 'avg_cu_grade',
                         'total_tonnes', 'total_cu_tonnes', 'n_diversions',
                         'avg_surface_volume_corr', 'avg_xrf_confidence']
    summaries['diversion_rate'] = summaries['n_diversions'] / summaries['n_trucks']

    # Calculate F1-related metrics
    # From Round 1: F1 factor is the ratio of actual to planned performance
    summaries['f1_factor_estimate'] = 1.0 - summaries['diversion_rate'] * 0.5  # Simplified

    return summaries


# =============================================================================
# MAIN EXECUTION
# =============================================================================
def main():
    """Generate all synthetic data and save locally."""
    print("=" * 70)
    print("ShovelSense Synthetic Data Generation")
    print("Based on Dialectical ROI Analysis Parameters")
    print("=" * 70)
    print(f"\nDeposit Parameters:")
    print(f"  Cutoff Grade: {CU_CUTOFF}% Cu")
    print(f"  Target Head Grade: {CU_MEAN_HEAD_GRADE}% Cu")
    print(f"  Mineralogy: {CHALCOPYRITE_PCT*100:.0f}% chalcopyrite, {BORNITE_PCT*100:.0f}% bornite")
    print(f"  Monthly Throughput: {MONTHLY_THROUGHPUT_TONNES:,} tonnes")
    print(f"  Metallurgical Recovery: {METALLURGICAL_RECOVERY*100:.0f}%")
    print(f"\nData Range: {START_DATE.date()} to {END_DATE.date()} ({N_DAYS} days)")
    print(f"Catalog: {CATALOG}")
    print(f"Schema: {SCHEMA}")
    print()

    # Generate data
    print("1. Generating block model with zonation pattern...")
    print("   (Bornite core → Chalcopyrite zone → Pyrite halo)")
    block_model = generate_block_model(n_blocks=500)
    print(f"   Generated {len(block_model)} blocks")

    # Validate block model distribution
    domain_dist = block_model['geological_domain'].value_counts(normalize=True)
    print(f"\n   Domain distribution:")
    for domain, pct in domain_dist.items():
        print(f"     {domain}: {pct*100:.1f}%")

    print("\n2. Generating fleet data...")
    shovels, trucks = generate_fleet()
    print(f"   Generated {len(shovels)} shovels (XRF-equipped), {len(trucks)} trucks")

    print("\n3. Generating XRF measurements and truck loads...")
    bucket_measurements, truck_loads = generate_bucket_measurements(block_model, shovels, trucks)
    print(f"   Generated {len(bucket_measurements):,} bucket measurements")
    print(f"   Generated {len(truck_loads):,} truck loads")

    print("\n4. Generating shift summaries...")
    shift_summaries = generate_shift_summaries(truck_loads.copy())
    print(f"   Generated {len(shift_summaries)} shift summaries")

    # Calculate statistics
    print("\n" + "=" * 70)
    print("DATA VALIDATION")
    print("=" * 70)

    diversion_counts = truck_loads['diversion_type'].value_counts()
    total_trucks = len(truck_loads)

    print(f"\nClassification Results:")
    print(f"  Total trucks: {total_trucks:,}")
    for dtype, count in diversion_counts.items():
        pct = count / total_trucks * 100
        print(f"  {dtype}: {count:,} ({pct:.2f}%)")

    ore_from_waste = diversion_counts.get('ORE_FROM_WASTE', 0)
    waste_from_ore = diversion_counts.get('WASTE_FROM_ORE', 0)
    total_diversions = ore_from_waste + waste_from_ore
    diversion_rate = total_diversions / total_trucks * 100

    print(f"\n  Overall diversion rate: {diversion_rate:.2f}%")
    print(f"  Ore from Waste rate: {ore_from_waste/total_trucks*100:.2f}% (target: 6.4%)")
    print(f"  Waste from Ore rate: {waste_from_ore/total_trucks*100:.2f}% (target: 4.7%)")
    print(f"  (Target from white paper: ~11%)")

    # Grade statistics
    print(f"\nGrade Statistics:")
    print(f"  Block model mean Cu: {block_model['planned_cu_grade'].mean():.3f}%")
    print(f"  Truck load mean Cu: {truck_loads['avg_cu_grade_pct'].mean():.3f}%")
    print(f"  Target head grade: {CU_MEAN_HEAD_GRADE}%")

    # XRF confidence by domain
    print(f"\nXRF Confidence by Geological Domain:")
    conf_by_domain = bucket_measurements.groupby('geological_domain')['xrf_confidence'].mean()
    for domain, conf in conf_by_domain.sort_values(ascending=False).items():
        print(f"  {domain}: {conf:.3f}")

    # Save to local parquet files
    output_dir = "data/generated"
    os.makedirs(output_dir, exist_ok=True)

    print(f"\n5. Saving to local parquet files in {output_dir}/...")
    block_model.to_parquet(f"{output_dir}/block_model.parquet", index=False)
    shovels.to_parquet(f"{output_dir}/shovels.parquet", index=False)
    trucks.to_parquet(f"{output_dir}/trucks.parquet", index=False)
    bucket_measurements.to_parquet(f"{output_dir}/bucket_measurements.parquet", index=False)
    truck_loads.to_parquet(f"{output_dir}/truck_loads.parquet", index=False)
    shift_summaries.to_parquet(f"{output_dir}/shift_summaries.parquet", index=False)

    print("\n" + "=" * 70)
    print("GENERATION COMPLETE")
    print("=" * 70)
    print(f"Data saved to: {output_dir}/")
    print("\nGenerated files:")
    print("  - block_model.parquet (geological reference with zonation)")
    print("  - shovels.parquet (XRF-equipped fleet)")
    print("  - trucks.parquet (haul fleet)")
    print("  - bucket_measurements.parquet (XRF sensor data with matrix effects)")
    print("  - truck_loads.parquet (aggregated loads with diversions)")
    print("  - shift_summaries.parquet (operational summaries)")
    print()
    print("To upload to Databricks, run: just upload-data")


if __name__ == "__main__":
    main()
