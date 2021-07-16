"""Module for paginate pages"""

from flask import abort


def get_paginated_list(results: list, url: str, start: int, limit: int) -> dict:
    """Function for paginate pages"""
    start = int(start)
    limit = int(limit)
    count = len(results)
    if count < start or limit < 0:
        abort(404)
    obj = {'start': start, 'limit': limit, 'count': count}
    if start == 1:
        obj['previous'] = ''
    else:
        start_copy = max(1, start - limit)
        limit_copy = start - 1
        obj['previous'] = url + '?start=%d&limit=%d' % (start_copy, limit_copy)
    if start + limit > count:
        obj['next'] = ''
    else:
        start_copy = start + limit
        obj['next'] = url + '?start=%d&limit=%d' % (start_copy, limit)
    obj['results'] = results[(start - 1):(start - 1 + limit)]
    return obj
