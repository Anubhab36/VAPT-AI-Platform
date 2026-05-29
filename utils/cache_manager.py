cache_store = {}


def set_cache(

    key,

    value
):

    cache_store[key] = value


def get_cache(key):

    return cache_store.get(key)


def cache_exists(key):

    return key in cache_store