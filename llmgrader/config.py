"""
Configuration for LLM providers.
"""

# HuggingFace configuration
# Use the Hugging Face Router endpoint (recommended replacement for api-inference)
# {model} will be replaced with the chosen model id, e.g. "HuggingFaceH4/zephyr-7b-beta"
HF_API_URL = "https://router.huggingface.co/models/{model}"
# Use a stable, actively maintained model
HF_DEFAULT_MODEL = "meta-llama/Llama-3.1-8B-Instruct:novita"

# Request timeout settings
DEFAULT_TIMEOUT = 20  # seconds
ADDITIONAL_TIMEOUT_BUFFER = 5  # seconds
