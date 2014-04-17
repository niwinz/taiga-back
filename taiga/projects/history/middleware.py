from .services import clear_frozen_objects_storage


class HistoryMiddleware(object):
    """
    Middleware that manages memory management
    of frozen object storage.

    Usage of this middleware is recommended for
    avoid constant memory alocations without
    freeing it.
    """

    def process_response(self, request, response):
        clear_frozen_objects_storage()
