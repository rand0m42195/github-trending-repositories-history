"""
Subscription functionality for Github Trending History.
"""

from .manager import SubscriptionManager
from .processor import process_subscription_issues

__all__ = ['SubscriptionManager', 'process_subscription_issues'] 