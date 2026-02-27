"""
Exploratory Data Analysis (EDA) utilities.

Computes communication statistics, identifies key communication nodes,
and analyzes email characteristics.
"""

import pandas as pd
import re
from collections import Counter


def extract_sender_email(sender_str: str) -> str:
    """Extract email from 'Name <email@domain.com>' or return as-is."""
    match = re.search(r'<([^>]+)>', sender_str)
    if match:
        return match.group(1)
    return sender_str


def extract_recipients(recipient_str: str) -> list[str]:
    """Extract list of email addresses from comma/semicolon-separated field."""
    if pd.isna(recipient_str) or recipient_str == 'UNKNOWN':
        return []
    
    recipients = re.split(r'[,;]', recipient_str)
    emails = []
    
    for rec in recipients:
        email_match = re.search(r'<([^>]+)>', rec)
        if email_match:
            emails.append(email_match.group(1))
        elif '@' in rec:
            emails.append(rec.strip())
    
    return emails


def compute_communication_statistics(
    df_clean: pd.DataFrame,
    top_n: int = 10,
    verbose: bool = True
) -> dict:
    """Compute sender/recipient stats, email length, and return results dict."""
    df_clean['sender_email'] = df_clean['sender'].apply(extract_sender_email)
    unique_senders = df_clean['sender_email'].nunique()
    top_senders = df_clean['sender_email'].value_counts().head(top_n)
    
    df_clean['recipients_list'] = df_clean['recipients'].apply(extract_recipients)
    all_recipients = Counter()
    for recipients_list in df_clean['recipients_list']:
        all_recipients.update(recipients_list)
    top_recipients = all_recipients.most_common(top_n)
    
    avg_email_length = df_clean['body'].str.split().str.len().mean()
    avg_subject_length = df_clean['subject'].str.split().str.len().mean()
    
    results = {
        'unique_senders': unique_senders,
        'unique_recipients': len(all_recipients),
        'total_emails': len(df_clean),
        'top_senders': top_senders,
        'top_recipients': top_recipients,
        'all_recipients': all_recipients,
        'avg_email_length': avg_email_length,
        'avg_subject_length': avg_subject_length
    }
    
    if verbose:
        print("\n" + "=" * 80)
        print("COMMUNICATION STATISTICS")
        print("=" * 80)
        
        print(f"\nDataset Overview:")
        print(f"  Total emails:           {len(df_clean):,}")
        print(f"  Unique senders:         {unique_senders:,}")
        print(f"  Unique recipients:      {len(all_recipients):,}")
        print(f"  Avg. email length:      {avg_email_length:.1f} words")
        print(f"  Avg. subject length:    {avg_subject_length:.1f} words")
        
        print(f"\nTop {top_n} Senders (by email count):")
        for i, (sender, count) in enumerate(top_senders.items(), 1):
            pct = 100 * count / len(df_clean)
            print(f"  {i:2d}. {sender:40s} : {count:6,d} ({pct:5.2f}%)")
        
        print(f"\nTop {top_n} Recipients (by email count):")
        for i, (recipient, count) in enumerate(top_recipients, 1):
            pct = 100 * count / len(df_clean)
            print(f"  {i:2d}. {recipient:40s} : {count:6,d} ({pct:5.2f}%)")
        
        print("=" * 80)
    
    return results


def get_data_quality_report(df_parsed: pd.DataFrame) -> dict:
    """Return dict with null values, parse errors, and field-specific issues."""
    report = {
        'null_values': df_parsed.isnull().sum().to_dict(),
        'parse_errors': ((df_parsed['sender'] == 'PARSE_ERROR') | 
                         (df_parsed['recipients'] == 'PARSE_ERROR')).sum(),
        'unknown_senders': (df_parsed['sender'] == 'UNKNOWN').sum(),
        'unknown_recipients': (df_parsed['recipients'] == 'UNKNOWN').sum(),
        'empty_subjects': (df_parsed['subject'] == '').sum(),
        'empty_bodies': (df_parsed['body'] == '').sum(),
    }
    
    return report
