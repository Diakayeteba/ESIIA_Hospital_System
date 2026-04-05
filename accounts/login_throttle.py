from django.conf import settings
from django.core.cache import cache


def _fail_key(username: str) -> str:
    return f'ehs:login_fail:{username}'


def _lock_key(username: str) -> str:
    return f'ehs:login_lock:{username}'


def is_username_locked(username: str) -> bool:
    if not username:
        return False
    return cache.get(_lock_key(username)) is True


def register_failed_attempt(username: str) -> None:
    if not username:
        return
    max_attempts = getattr(settings, 'LOGIN_MAX_ATTEMPTS', 5)
    lock_seconds = getattr(settings, 'LOGIN_LOCKOUT_SECONDS', 900)
    k = _fail_key(username)
    n = cache.get(k, 0) + 1
    cache.set(k, n, timeout=lock_seconds)
    if n >= max_attempts:
        cache.set(_lock_key(username), True, timeout=lock_seconds)
        cache.delete(k)


def clear_login_throttle(username: str) -> None:
    if not username:
        return
    cache.delete(_fail_key(username))
    cache.delete(_lock_key(username))
