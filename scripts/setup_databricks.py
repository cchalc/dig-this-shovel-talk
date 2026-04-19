"""
Set up Databricks infrastructure and upload data.

Creates:
- Schema: ai_dev_kit.shovelsense
- Volume: ai_dev_kit.shovelsense.raw_data
- Uploads parquet files from data/generated/
"""
import os
import sys
from pathlib import Path

from databricks.sdk import WorkspaceClient
from databricks.sdk.service.catalog import VolumeType

# Configuration
CATALOG = os.environ.get("CATALOG", "cjc_aws_workspace_catalog")
SCHEMA = os.environ.get("SCHEMA", "shovelsense")
VOLUME = "raw_data"
VOLUME_PATH = f"/Volumes/{CATALOG}/{SCHEMA}/{VOLUME}"
DATA_DIR = Path("data/generated")


def main():
    print("=" * 60)
    print("Databricks Infrastructure Setup")
    print("=" * 60)
    print(f"Catalog: {CATALOG}")
    print(f"Schema: {SCHEMA}")
    print(f"Volume: {VOLUME}")
    print()

    # Connect to Databricks
    print("Connecting to Databricks...")
    profile = os.environ.get("DATABRICKS_CONFIG_PROFILE", "fevm-cjc")
    w = WorkspaceClient(profile=profile)
    print(f"  Connected to: {w.config.host}")

    # Create schema (catalog should already exist)
    print(f"\n1. Creating schema {CATALOG}.{SCHEMA}...")
    try:
        w.schemas.create(name=SCHEMA, catalog_name=CATALOG)
        print("   Schema created!")
    except Exception as e:
        if "already exists" in str(e).lower():
            print("   Schema already exists, skipping.")
        else:
            print(f"   Warning: {e}")

    # Create volume
    print(f"\n2. Creating volume {CATALOG}.{SCHEMA}.{VOLUME}...")
    try:
        w.volumes.create(
            catalog_name=CATALOG,
            schema_name=SCHEMA,
            name=VOLUME,
            volume_type=VolumeType.MANAGED
        )
        print("   Volume created!")
    except Exception as e:
        if "already exists" in str(e).lower():
            print("   Volume already exists, skipping.")
        else:
            print(f"   Warning: {e}")

    # Upload data files
    print(f"\n3. Uploading data files to {VOLUME_PATH}/...")

    if not DATA_DIR.exists():
        print(f"   ERROR: Data directory {DATA_DIR} not found!")
        print("   Run 'just generate-data' first.")
        sys.exit(1)

    parquet_files = list(DATA_DIR.glob("*.parquet"))
    if not parquet_files:
        print(f"   ERROR: No parquet files found in {DATA_DIR}")
        sys.exit(1)

    for filepath in parquet_files:
        remote_path = f"{VOLUME_PATH}/{filepath.name}"
        print(f"   Uploading {filepath.name}...")
        try:
            with open(filepath, 'rb') as f:
                w.files.upload(remote_path, f, overwrite=True)
            print(f"      -> {remote_path}")
        except Exception as e:
            print(f"      ERROR: {e}")

    # Verify upload
    print(f"\n4. Verifying uploaded files...")
    try:
        files = list(w.files.list_directory_contents(VOLUME_PATH))
        print(f"   Found {len(files)} files in volume:")
        for f in files:
            print(f"      - {f.name}")
    except Exception as e:
        print(f"   Warning: Could not list files: {e}")

    print("\n" + "=" * 60)
    print("SETUP COMPLETE")
    print("=" * 60)
    print(f"\nData available at: {VOLUME_PATH}/")
    print("\nNext steps:")
    print("  1. Deploy the pipeline: just deploy")
    print("  2. Run data quality check in Databricks")


if __name__ == "__main__":
    main()
