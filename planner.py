def plan(query):
    # Detect create agent command
    if query.startswith("create agent "):
        parts = query.split()
        if len(parts) >= 3:
            name = parts[2]
            purpose = " ".join(parts[3:]) if len(parts) > 3 else "No purpose provided."
            return {
                "action": "create_agent",
                "input": {
                    "name": name,
                    "purpose": purpose
                }
            }
    """
    A simple planner that decides what to do based on the query.
    """

    # Tool: read file
    if query.startswith("read file "):
        return {"action": "read_file", "input": query.replace("read file ", "").strip()}

    # Tool: list directory
    if query.startswith("list directory "):
        return {"action": "list_directory", "input": query.replace("list directory ", "").strip()}

    # Tool: summarize
    if query.startswith("summarize "):
        return {"action": "summarize", "input": query.replace("summarize ", "").strip()}

    # Default: ask advisor
    return {"action": "advisor", "input": query}
