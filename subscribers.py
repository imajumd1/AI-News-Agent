"""Email subscription management for AI News Agent."""

import csv
import os
import hashlib
import secrets
from datetime import datetime
from typing import Optional, List, Dict, Tuple
import re

# Subscribers file path
SUBSCRIBERS_FILE = os.getenv("SUBSCRIBERS_FILE", "data/subscribers.csv")

def ensure_subscribers_file():
    """Ensure subscribers.csv exists with headers."""
    os.makedirs(os.path.dirname(SUBSCRIBERS_FILE) or ".", exist_ok=True)
    
    if not os.path.exists(SUBSCRIBERS_FILE):
        with open(SUBSCRIBERS_FILE, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'email', 'token', 'subscribed_at', 'confirmed', 'categories', 'unsubscribed_at'
            ])
            writer.writeheader()

def validate_email(email: str) -> bool:
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def email_exists(email: str) -> bool:
    """Check if email is already subscribed."""
    ensure_subscribers_file()
    try:
        with open(SUBSCRIBERS_FILE, 'r', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['email'].lower() == email.lower() and not row.get('unsubscribed_at'):
                    return True
    except (FileNotFoundError, ValueError):
        pass
    return False

def generate_confirmation_token() -> str:
    """Generate a secure confirmation token."""
    return secrets.token_urlsafe(32)

def add_subscriber(email: str, categories: Optional[List[str]] = None) -> Tuple[bool, str, str]:
    """
    Add a new subscriber.
    
    Args:
        email: Email address to subscribe
        categories: Optional list of categories to subscribe to
        
    Returns:
        Tuple of (success, message, token)
    """
    # Validate email
    email = email.strip().lower()
    if not validate_email(email):
        return False, "Invalid email format", ""
    
    # Check if already subscribed
    if email_exists(email):
        return False, "Email already subscribed", ""
    
    ensure_subscribers_file()
    
    token = generate_confirmation_token()
    categories_str = ",".join(categories) if categories else "all"
    
    try:
        with open(SUBSCRIBERS_FILE, 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'email', 'token', 'subscribed_at', 'confirmed', 'categories', 'unsubscribed_at'
            ])
            writer.writerow({
                'email': email,
                'token': token,
                'subscribed_at': datetime.now().isoformat(),
                'confirmed': 'false',
                'categories': categories_str,
                'unsubscribed_at': ''
            })
        return True, "Subscription pending confirmation. Check your email!", token
    except Exception as e:
        return False, f"Error saving subscription: {str(e)}", ""

def confirm_subscription(email: str, token: str) -> Tuple[bool, str]:
    """
    Confirm a subscription with a token.
    
    Args:
        email: Email address to confirm
        token: Confirmation token
        
    Returns:
        Tuple of (success, message)
    """
    email = email.strip().lower()
    ensure_subscribers_file()
    
    try:
        rows = []
        found = False
        
        with open(SUBSCRIBERS_FILE, 'r', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['email'].lower() == email and row['token'] == token:
                    if row.get('confirmed') == 'true':
                        return False, "Already confirmed"
                    row['confirmed'] = 'true'
                    found = True
                rows.append(row)
        
        if not found:
            return False, "Invalid email or token"
        
        # Write back updated rows
        with open(SUBSCRIBERS_FILE, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'email', 'token', 'subscribed_at', 'confirmed', 'categories', 'unsubscribed_at'
            ])
            writer.writeheader()
            writer.writerows(rows)
        
        return True, "Subscription confirmed! You'll now receive AI news updates."
    except Exception as e:
        return False, f"Error confirming subscription: {str(e)}"

def unsubscribe(email: str, token: Optional[str] = None) -> Tuple[bool, str]:
    """
    Unsubscribe an email address.
    
    Args:
        email: Email address to unsubscribe
        token: Optional token for verification
        
    Returns:
        Tuple of (success, message)
    """
    email = email.strip().lower()
    ensure_subscribers_file()
    
    try:
        rows = []
        found = False
        
        with open(SUBSCRIBERS_FILE, 'r', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['email'].lower() == email:
                    if token and row['token'] != token:
                        continue  # Token mismatch, skip
                    if row.get('unsubscribed_at'):
                        continue  # Already unsubscribed
                    row['unsubscribed_at'] = datetime.now().isoformat()
                    found = True
                rows.append(row)
        
        if not found:
            return False, "Email not found or already unsubscribed"
        
        # Write back updated rows
        with open(SUBSCRIBERS_FILE, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'email', 'token', 'subscribed_at', 'confirmed', 'categories', 'unsubscribed_at'
            ])
            writer.writeheader()
            writer.writerows(rows)
        
        return True, "You have been unsubscribed from AI News Agent."
    except Exception as e:
        return False, f"Error unsubscribing: {str(e)}"

def get_confirmed_subscribers() -> List[Dict[str, str]]:
    """Get all confirmed subscribers."""
    ensure_subscribers_file()
    subscribers = []
    
    try:
        with open(SUBSCRIBERS_FILE, 'r', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get('confirmed') == 'true' and not row.get('unsubscribed_at'):
                    subscribers.append(row)
    except (FileNotFoundError, ValueError):
        pass
    
    return subscribers

def get_subscriber_count() -> int:
    """Get total count of confirmed subscribers."""
    return len(get_confirmed_subscribers())

