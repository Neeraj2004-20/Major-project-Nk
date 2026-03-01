#!/usr/bin/env python
"""Quick test of imports"""

print("Testing imports...")

try:
    from api_llm import router
    print("✓ api_llm router imported")
except Exception as e:
    print(f"✗ api_llm import error: {e}")
    import traceback
    traceback.print_exc()

try:
    from web_app_main import web_app_router
    print("✓ web_app_main router imported")
except Exception as e:
    print(f"✗ web_app_main import error: {e}")
    import traceback
    traceback.print_exc()

print("\nDone!")
