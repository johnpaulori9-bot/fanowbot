# main.py
# Advisor entry point

from originator import Originator

def main():
    originator = Originator()
    originator.run()

if __name__ == "__main__":
    main()
from openclaw.providers.llama_cpp import LlamaCppProvider
from advisor import EverythingAdvisor
from workflow import AdvisorWorkflow

def main():
    print("=== OpenClaw Everything Advisor v1.0 ===")
    print("Type 'exit' to quit.\n")

    provider = LlamaCppProvider(
        model_path="models/phi-3-mini.Q4_K_M.gguf",
        n_threads=12
    )

    advisor = EverythingAdvisor(provider)
    workflow = AdvisorWorkflow()

    while True:
        query = input("You: ").strip()
        if query.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        response = workflow.run(advisor, query)
        print("\nAssistant:", response, "\n")

if __name__ == "__main__":
    main()
