"""
Phase 1: Exploratory Data Analysis Pipeline

This script loads, parses, cleans, and analyzes the Enron email corpus.
It can be run directly from the command line or imported as a module.

Usage:
    python phase1_eda.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from preprocessing.loader import load_raw_data
from preprocessing.parser import parse_all_emails
from preprocessing.cleaner import clean_email_data
from preprocessing.eda import compute_communication_statistics, get_data_quality_report


def run_phase1_eda(verbose: bool = True) -> dict:
    """Load, parse, clean, and analyze emails. Return dict with all results."""
    print("\n" + "=" * 80)
    print("PHASE 1: EXPLORATORY DATA ANALYSIS")
    print("Enron Email Corpus - Knowledge Graph Analysis")
    print("=" * 80)
    
    print("\n[1/5] Loading raw dataset...")
    df_raw, data_path = load_raw_data()
    print(f"✓ Loaded {len(df_raw):,} emails from {data_path.name}")
    print(f"  Dataset size: {df_raw.memory_usage(deep=True).sum() / 1e9:.2f} GB")
    
    print("\n[2/5] Parsing email messages...")
    df_parsed = parse_all_emails(df_raw)
    print(f"✓ Parsed {len(df_parsed):,} emails into structured fields")
    print(f"  Columns: {df_parsed.columns.tolist()}")
    
    print("\n[3/5] Assessing data quality...")
    quality_report = get_data_quality_report(df_parsed)
    if verbose:
        print(f"\n  Null values:")
        for col, count in quality_report['null_values'].items():
            print(f"    - {col}: {count}")
        print(f"\n  Issues detected:")
        print(f"    - Parse errors: {quality_report['parse_errors']}")
        print(f"    - Unknown senders: {quality_report['unknown_senders']}")
        print(f"    - Unknown recipients: {quality_report['unknown_recipients']}")
        print(f"    - Empty subjects: {quality_report['empty_subjects']}")
        print(f"    - Empty bodies: {quality_report['empty_bodies']}")
    
    print("\n[4/5] Cleaning invalid records...")
    df_clean, clean_stats = clean_email_data(df_parsed, verbose=verbose)
    
    print("\n[5/5] Computing communication statistics...")
    comm_stats = compute_communication_statistics(df_clean, verbose=verbose)
    
    print("\n" + "=" * 80)
    print("PHASE 1 COMPLETE - Summary")
    print("=" * 80)
    print(f"\n✓ Loaded:      {clean_stats['initial_count']:,} emails")
    print(f"✓ Cleaned:     {clean_stats['final_count']:,} emails")
    print(f"✓ Retention:   {clean_stats['retention_rate']:.2f}%")
    print(f"✓ Senders:     {comm_stats['unique_senders']:,} unique employees")
    print(f"✓ Recipients:  {comm_stats['unique_recipients']:,} unique addresses")
    print("\nDataset is now ready for Phase 2 (Feature Extraction & Graph Construction)")
    print("=" * 80 + "\n")
    
    return {
        'df_raw': df_raw,
        'df_parsed': df_parsed,
        'df_clean': df_clean,
        'parse_stats': {'parsed_count': len(df_parsed)},
        'clean_stats': clean_stats,
        'comm_stats': comm_stats,
        'quality_report': quality_report
    }


if __name__ == "__main__":
    results = run_phase1_eda(verbose=True)
    
    output_path = Path(__file__).parent.parent.parent / "data" / "processed" / "enron_cleaned.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    results['df_clean'].to_csv(output_path, index=False)
    print(f"✓ Cleaned dataset saved to: {output_path}")
