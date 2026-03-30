from openclaw.core.harness import Harness
from openclaw.providers.llama_cpp import LlamaCppProvider

def build_advisor():
    provider = LlamaCppProvider(model_path="models/model.gguf")
    return Harness(provider=provider)
