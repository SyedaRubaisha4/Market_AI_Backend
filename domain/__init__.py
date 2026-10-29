from importlib import import_module

__all__ = [
    'BaseModel',
    'Brand',
    'GeneratedContent',
    'Lookup',
    'Notification',
    'Product',
    'ProductImage',
 #   'ScheduledPost',
  #  'ScheduledPostTarget',
    'SocialConnect',
    'User',
    'UserToken',
    'SocialConnect',
]


def __getattr__(name):
    if name not in __all__:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    models = import_module('.models', __name__)
    return getattr(models, name)