import traceback

try:
    1/0
except Exception:
    traceback.print_exc()