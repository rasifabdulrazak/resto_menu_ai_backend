import pkgutil
import importlib
from pathlib import Path

package_dir = Path(__file__).resolve().parent
package_name = __name__


def load_all_models():
    """
    Dynamically import all model modules so that
    SQLAlchemy registers them in Base.metadata
    """
    for module in pkgutil.walk_packages([str(package_dir)], package_name + "."):
        importlib.import_module(module.name)


print(load_all_models(),"=====================")
load_all_models()