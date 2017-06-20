import logging

from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key

logger = logging.getLogger(__name__)


ONE_YEAR_TIMEOUT = (
    60 *  # seconds
    60 *  # minutes
    24 *  # hours
    365   # days
)


def get_or_cache(key, value, timeout):
    cache_value = cache.get(key)

    if not cache_value:
        cache_value = value() if callable(value) else value
        cache.set(key, cache_value, timeout)

    return cache_value


def clear_cache():
    cleared = cache.delete_pattern('*')
    logger.info('%d cache keys deleted!', cleared)


def delete_cached_fragment(fragment_name, *args):
    cache.delete(make_template_fragment_key(fragment_name, args or None))
