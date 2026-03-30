from agents.memory_agent import MemoryAgent

agent = MemoryAgent()

file_id = agent.ingest_file("data/test2.txt")

print("File ingested with file_id:", file_id)
