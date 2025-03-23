import warnings

# Filter out SWIG deprecation warnings
warnings.filterwarnings(
    "ignore", category=DeprecationWarning, module="importlib._bootstrap")
