"""
Email parsing utilities.

Parses RFC 2822 formatted email messages into structured fields:
sender, recipients, date, subject, body.
"""

import pandas as pd
from email.parser import Parser
from email import policy


def parse_email_message(raw_message: str) -> tuple[str, str, str, str, str]:
    """Parse RFC 2822 email to (sender, recipients, date, subject, body)."""
    try:
        parser = Parser(policy=policy.default)
        msg = parser.parsestr(raw_message)
        
        sender = msg.get('From', 'UNKNOWN').strip()
        recipients = msg.get('To', 'UNKNOWN').strip()
        date = msg.get('Date', 'UNKNOWN').strip()
        subject = msg.get('Subject', '').strip()
        body = msg.get_payload(decode=True)
        
        if isinstance(body, bytes):
            try:
                body = body.decode('utf-8', errors='ignore')
            except Exception:
                body = str(body)
        body = body.strip() if body else ''
        
        return sender, recipients, date, subject, body
        
    except Exception as e:
        return 'PARSE_ERROR', 'PARSE_ERROR', 'PARSE_ERROR', '', ''


def parse_all_emails(df: pd.DataFrame, message_col: str = 'message') -> pd.DataFrame:
    """Apply parse_email_message() to all rows in DataFrame."""
    parsed_data = df[message_col].apply(parse_email_message)
    
    df_parsed = pd.DataFrame({
        'sender': [x[0] for x in parsed_data],
        'recipients': [x[1] for x in parsed_data],
        'date': [x[2] for x in parsed_data],
        'subject': [x[3] for x in parsed_data],
        'body': [x[4] for x in parsed_data]
    })
    
    if 'file' in df.columns:
        df_parsed['file'] = df['file']
    
    return df_parsed
