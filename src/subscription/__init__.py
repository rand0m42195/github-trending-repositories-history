"""
Subscription functionality for GitHub Trending Assistant.
"""

from .manager import SubscriptionManager
from .api import SubscriptionAPI
from .processor import process_subscription_issues

__all__ = ['SubscriptionManager', 'SubscriptionAPI', 'process_subscription_issues'] 