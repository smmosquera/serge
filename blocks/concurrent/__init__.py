from pkgutil import extend_path
import sys

sys.modules['concurrent'] = sys.modules['serge.blocks.concurrent']

__path__ = extend_path(__path__, __name__)
