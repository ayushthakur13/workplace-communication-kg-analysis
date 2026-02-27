"""
Data cleaning utilities for parsed email data.

Removes invalid/incomplete email records that lack critical fields
required for knowledge graph construction and NLP analysis.
"""

import pandas as pd


def clean_email_data(df_parsed: pd.DataFrame, verbose: bool = True) -> tuple[pd.DataFrame, dict]:
    """Remove rows with invalid sender, recipients, or body. Return (df_clean, stats)."""
    initial_count = len(df_parsed)
    
    invalid_mask = (
        (df_parsed['sender'] == 'UNKNOWN') |
        (df_parsed['sender'] == 'PARSE_ERROR') |
        (df_parsed['recipients'] == 'UNKNOWN') |
        (df_parsed['recipients'] == 'PARSE_ERROR') |
        (df_parsed['body'] == '') |
        (df_parsed['body'] == 'PARSE_ERROR')
    )
    
    df_clean = df_parsed[~invalid_mask].copy()
    df_clean.reset_index(drop=True, inplace=True)
    
    removed_count = initial_count - len(df_clean)
    retention_rate = 100 * len(df_clean) / initial_count if initial_count > 0 else 0
    
    stats = {
        'initial_count': initial_count,
        'removed_count': removed_count,
        'final_count': len(df_clean),
        'removal_pct': 100 * removed_count / initial_count if initial_count > 0 else 0,
        'retention_rate': retention_rate
    }
    
    if verbose:
        print("\n" + "=" * 80)
        print("DATA CLEANING REPORT")
        print("=" * 80)
        print(f"\nInitial dataset size:       {initial_count:,}")
        print(f"Rows removed:               {removed_count:,} ({stats['removal_pct']:.2f}%)")
        print(f"Cleaned dataset size:       {len(df_clean):,}")
        print(f"Retention rate:             {retention_rate:.2f}%")
        print(f"\nCleaning rules applied:")
        print(f"  - Remove sender = 'UNKNOWN' or 'PARSE_ERROR'")
        print(f"  - Remove recipients = 'UNKNOWN' or 'PARSE_ERROR'")
        print(f"  - Remove empty or error body")
        print("=" * 80)
    
    return df_clean, stats
