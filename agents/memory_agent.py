from memory.text_extractor import TextExtractor
from memory.file_memory_manager import FileMemoryManager


class MemoryAgent:
    """
    Coordinates all memory operations:
    - File memory (versions, hashes)
    - Text extraction
    - Semantic analysis (later)
    - Knowledge graph (later)
    - Indexing (later)
    """

    def __init__(self):
        # Load file memory manager
        self.file_memory = FileMemoryManager("memory/file_memory.json")

        # Load text extractor
        self.text_extractor = TextExtractor("memory/text_memory.json")

        # Later you will add:
        # self.semantic_analyzer = SemanticAnalyzer(...)
        # self.graph_builder = KnowledgeGraphBuilder(...)
        # self.index_manager = IndexManager(...)

    def ingest_file(self, path: str):
        """
        Main entry point for adding a file to the memory system.
        """

        # 1. Update file memory (get file_id, version info)
        file_id, is_new_version, old_version = self.file_memory.update_file_record(path)

        # 2. Extract text from the file
        self.text_extractor.rebuild_text_memory(file_id, path)

        # 3. Later steps (we will add these modules next):
        # self.semantic_analyzer.reanalyze(file_id)
        # self.graph_builder.update_graph_for_file(file_id)
        # self.index_manager.reindex_for_file(file_id)

        return file_id
