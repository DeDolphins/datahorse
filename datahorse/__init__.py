

from datahorse.smart_dataframe import SmartDataframe
from datahorse.smart_datalake import SmartDatalake

from .agent import Agent
from .engine import set_pd_engine
from .helpers.cache import Cache
from .skills import skill


def clear_cache(filename: str = None):
    """Clear the cache"""
    cache = Cache(filename) if filename else Cache()

    cache.clear()


__all__ = [
    "Agent",
    "clear_cache",
    "skill",
    "set_pd_engine",
    "pandas",
    "SmartDataframe",
    "SmartDatalake",
]
