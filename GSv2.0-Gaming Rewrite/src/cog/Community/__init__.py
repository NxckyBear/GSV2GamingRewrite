import pkgutil

CEXTENSIONS = [e.name for e in pkgutil.iter_modules(__path__, f"{__package__}.")]