"""
Generate synthetic mining data simulating ShovelSense XRF measurements and truck diversions.

Based on the ShovelSense white paper analysis, this generates:
- XRF bucket measurements (Cu, Fe, Zn, As grades)
- Truck load aggregations
- Diversion events (ore-from-waste, waste-from-ore)
- Block model reference data
- Shovel and truck fleet data

The data is designed to test and validate claims made in the ShovelSense white paper,
including the ~11% diversion rate and various classification scenarios.
"""
import os
import sys
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
from dataclasses import dataclass

# Databricks SDK import removed - upload handled by justfile

# =============================================================================
# CONFIGURATION
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

# Grade parameters (copper-porphyry deposit, similar to white paper)
CU_CUTOFF = 0.20  # Cu% cutoff for ore vs waste
CU_MEAN_ORE = 0.45  # Mean Cu% in ore zones
CU_MEAN_WASTE = 0.08  # Mean Cu% in waste zones
CU_STD = 0.15  # Standard deviation

# Diversion rates (based on white paper claims)
TARGET_DIVERSION_RATE = 0.11  # ~11% of trucks diverted
ORE_FROM_WASTE_RATE = 0.064  # 6.4% of trucks (403/6270)
WASTE_FROM_ORE_RATE = 0.047  # 4.7% of trucks (294/6270)

# Date range - last 80 days to match case study
END_DATE = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
START_DATE = END_DATE - timedelta(days=N_DAYS)

# =============================================================================
# DATA CLASSES
# =============================================================================
@dataclass
class BlockModel:
    """Geological block model with planned grades."""
    block_id: str
    bench: int
    easting: float
    northing: float
    elevation: float
    planned_cu_grade: float
    planned_fe_grade: float
    planned_classification: str  # 'ORE' or 'WASTE'
    geological_domain: str
    is_dyke: bool  # Barren dyke intrusion (causes diversions)
    blast_movement_m: float  # Post-blast displacement


@dataclass
class BucketMeasurement:
    """Single XRF bucket measurement."""
    measurement_id: str
    timestamp: datetime
    shovel_id: str
    bucket_number: int
    truck_id: str
    block_id: str
    cu_grade: float
    fe_grade: float
    zn_grade: float
    as_grade: float
    laser_fill_level: float
    xrf_confidence: float
    sensor_head_1_active: bool
    sensor_head_2_active: bool


@dataclass
class TruckLoad:
    """Aggregated truck load from multiple buckets."""
    load_id: str
    timestamp: datetime
    truck_id: str
    shovel_id: str
    n_buckets: int
    avg_cu_grade: float
    avg_fe_grade: float
    planned_classification: str
    shovelsense_classification: str
    diversion_type: str  # 'ALIGNED', 'ORE_FROM_WASTE', 'WASTE_FROM_ORE'
    destination: str
    payload_tonnes: float


# =============================================================================
# GENERATION FUNCTIONS
# =============================================================================
def generate_block_model(n_blocks: int = 500) -> pd.DataFrame:
    """Generate a simplified geological block model."""
    np.random.seed(SEED)

    blocks = []
    for i in range(n_blocks):
        # Random location in pit
        easting = np.random.uniform(500000, 501000)
        northing = np.random.uniform(6000000, 6001000)
        bench = np.random.choice([1, 2, 3, 4, 5], p=[0.15, 0.25, 0.30, 0.20, 0.10])
        elevation = 3500 - (bench * 15)  # 15m bench height

        # Geological domain affects grade
        domain = np.random.choice(
            ['PORPHYRY_CORE', 'PORPHYRY_HALO', 'SUPERGENE', 'LEACHED_CAP', 'WASTE_ZONE'],
            p=[0.15, 0.25, 0.20, 0.15, 0.25]
        )

        # Is this a barren dyke? (causes ore-to-waste diversions)
        is_dyke = np.random.random() < 0.05  # 5% of blocks are dyke intrusions

        # Grade based on domain
        if is_dyke:
            cu_grade = np.random.normal(0.02, 0.01)  # Very low grade
        elif domain == 'PORPHYRY_CORE':
            cu_grade = np.random.lognormal(np.log(0.6), 0.3)
        elif domain == 'PORPHYRY_HALO':
            cu_grade = np.random.lognormal(np.log(0.35), 0.35)
        elif domain == 'SUPERGENE':
            cu_grade = np.random.lognormal(np.log(0.5), 0.4)
        elif domain == 'LEACHED_CAP':
            cu_grade = np.random.lognormal(np.log(0.15), 0.5)
        else:
            cu_grade = np.random.lognormal(np.log(0.05), 0.4)

        cu_grade = max(0, min(cu_grade, 3.0))  # Clamp to realistic range

        # Blast movement (causes misclassification)
        blast_movement = np.random.exponential(2.0)  # Average 2m movement

        # Planned classification based on cutoff
        planned_class = 'ORE' if cu_grade >= CU_CUTOFF else 'WASTE'

        blocks.append({
            'block_id': f'BLK-{i:05d}',
            'bench': bench,
            'easting': round(easting, 2),
            'northing': round(northing, 2),
            'elevation': round(elevation, 2),
            'planned_cu_grade': round(cu_grade, 4),
            'planned_fe_grade': round(np.random.lognormal(np.log(5), 0.3), 2),
            'planned_classification': planned_class,
            'geological_domain': domain,
            'is_dyke': is_dyke,
            'blast_movement_m': round(blast_movement, 2)
        })

    return pd.DataFrame(blocks)


def generate_fleet() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Generate shovel and truck fleet data."""
    np.random.seed(SEED + 1)

    # Shovels
    shovels = []
    shovel_types = ['ELECTRIC_ROPE', 'HYDRAULIC', 'FRONT_END_LOADER']
    for i in range(N_SHOVELS):
        shovels.append({
            'shovel_id': f'SHV-{i+1:02d}',
            'shovel_type': shovel_types[i % len(shovel_types)],
            'bucket_capacity_m3': np.random.choice([40, 50, 60]),
            'minesense_equipped': True,
            'sensor_heads': np.random.choice([2, 3, 4]),
            'commissioned_date': (START_DATE - timedelta(days=np.random.randint(30, 365))).strftime('%Y-%m-%d')
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

    This is the core data that simulates what ShovelSense would produce.
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

                    # Add measurement noise and variability
                    # Dykes, blast movement, and geological uncertainty cause diversions

                    # Simulate ~11% diversion rate as per white paper
                    # 6.4% ore-from-waste + 4.7% waste-from-ore

                    if block['is_dyke']:
                        # Dykes are always low grade (causes waste-from-ore)
                        actual_cu = np.random.normal(0.02, 0.01)
                    elif block['blast_movement_m'] > 2:
                        # Blast movement causes material mixing
                        # Can shift ore into waste zones or vice versa
                        shift_magnitude = block['blast_movement_m'] / 5.0
                        # Add directional bias based on planned classification
                        if block['planned_classification'] == 'ORE':
                            bias = -0.05  # Tend to dilute ore
                        else:
                            bias = 0.05   # Tend to enrich waste
                        actual_cu = base_cu + bias + np.random.normal(0, 0.15 * shift_magnitude)
                    elif np.random.random() < 0.15:
                        # ~15% of buckets have significant grade variance from model
                        # This simulates geological uncertainty not captured in block model
                        # Combined with dykes and blast movement, aims for ~11% truck diversion
                        if block['planned_classification'] == 'ORE':
                            # Some "ore" blocks are actually low grade (waste-from-ore)
                            actual_cu = np.random.normal(CU_CUTOFF - 0.12, 0.06)
                        else:
                            # Some "waste" blocks have ore pockets (ore-from-waste)
                            actual_cu = np.random.normal(CU_CUTOFF + 0.20, 0.08)
                    else:
                        actual_cu = base_cu + np.random.normal(0, 0.05)

                    actual_cu = max(0, actual_cu)

                    # XRF measurement with sensor noise
                    xrf_noise = np.random.normal(0, 0.02)  # ~2% measurement error
                    measured_cu = actual_cu + xrf_noise
                    measured_cu = max(0, measured_cu)

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
                        'fe_grade_pct': round(np.random.lognormal(np.log(5), 0.2), 2),
                        'zn_grade_ppm': round(np.random.lognormal(np.log(100), 0.5), 1),
                        'as_grade_ppm': round(np.random.lognormal(np.log(50), 0.6), 1),
                        'laser_fill_level_pct': round(np.random.uniform(85, 100), 1),
                        'xrf_confidence': round(np.random.uniform(0.85, 0.99), 3),
                        'sensor_head_1_active': True,
                        'sensor_head_2_active': np.random.random() > 0.05  # 5% sensor failure
                    })

                    bucket_grades.append(measured_cu)
                    measurement_id += 1

                # Aggregate to truck load
                avg_cu = np.mean(bucket_grades)

                # Classification logic
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
                    'payload_tonnes': round(np.random.uniform(300, 380), 1),
                    'cycle_time_minutes': round(np.random.exponential(25) + 15, 1)
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
        'diversion_type': lambda x: (x != 'ALIGNED').sum()
    }).reset_index()

    summaries.columns = ['date', 'shift', 'shovel_id', 'n_trucks', 'avg_cu_grade',
                         'total_tonnes', 'n_diversions']
    summaries['diversion_rate'] = summaries['n_diversions'] / summaries['n_trucks']

    return summaries


# =============================================================================
# MAIN EXECUTION
# =============================================================================
def main():
    """Generate all synthetic data and save locally."""
    print("=" * 60)
    print("ShovelSense Synthetic Data Generation")
    print("=" * 60)
    print(f"Catalog: {CATALOG}")
    print(f"Schema: {SCHEMA}")
    print(f"Date Range: {START_DATE.date()} to {END_DATE.date()} ({N_DAYS} days)")
    print()

    # Generate data
    print("1. Generating block model...")
    block_model = generate_block_model(n_blocks=500)
    print(f"   Generated {len(block_model)} blocks")

    print("\n2. Generating fleet data...")
    shovels, trucks = generate_fleet()
    print(f"   Generated {len(shovels)} shovels, {len(trucks)} trucks")

    print("\n3. Generating XRF measurements and truck loads...")
    bucket_measurements, truck_loads = generate_bucket_measurements(block_model, shovels, trucks)
    print(f"   Generated {len(bucket_measurements):,} bucket measurements")
    print(f"   Generated {len(truck_loads):,} truck loads")

    print("\n4. Generating shift summaries...")
    shift_summaries = generate_shift_summaries(truck_loads.copy())
    print(f"   Generated {len(shift_summaries)} shift summaries")

    # Calculate statistics
    print("\n" + "=" * 60)
    print("DATA VALIDATION")
    print("=" * 60)

    diversion_counts = truck_loads['diversion_type'].value_counts()
    total_trucks = len(truck_loads)

    print(f"\nTruck Load Statistics:")
    print(f"  Total trucks: {total_trucks:,}")
    for dtype, count in diversion_counts.items():
        pct = count / total_trucks * 100
        print(f"  {dtype}: {count:,} ({pct:.1f}%)")

    total_diversions = total_trucks - diversion_counts.get('ALIGNED', 0)
    diversion_rate = total_diversions/total_trucks*100
    print(f"\n  Overall diversion rate: {diversion_rate:.1f}%")
    print(f"  (Target from white paper: ~11%)")

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

    print("\n" + "=" * 60)
    print("GENERATION COMPLETE")
    print("=" * 60)
    print(f"Data saved to: {output_dir}/")
    print("\nGenerated files:")
    print("  - block_model.parquet (geological reference)")
    print("  - shovels.parquet (fleet master data)")
    print("  - trucks.parquet (fleet master data)")
    print("  - bucket_measurements.parquet (XRF sensor data)")
    print("  - truck_loads.parquet (aggregated loads with diversions)")
    print("  - shift_summaries.parquet (operational summaries)")
    print()
    print("To upload to Databricks, run: just upload-data")


if __name__ == "__main__":
    main()
