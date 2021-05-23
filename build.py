from typing import Any, Dict
from rejson import __version__

def build(setup_kwargs: Dict[str, Any]) -> None:
    setup_kwargs.update({
        "zip_safe": False,
        "version": __version__
    })
