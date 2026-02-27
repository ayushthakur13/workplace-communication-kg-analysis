"""
Preprocessing module for Enron email corpus analysis.

Includes utilities for loading, parsing, cleaning, and analyzing email data.
"""

from .loader import load_raw_data
from .parser import parse_email_message, parse_all_emails
from .cleaner import clean_email_data
from .eda import compute_communication_statistics, extract_sender_email, extract_recipients

__all__ = [
    "load_raw_data",
    "parse_email_message",
    "parse_all_emails",
    "clean_email_data",
    "compute_communication_statistics",
    "extract_sender_email",
    "extract_recipients",
]
