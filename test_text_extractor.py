from memory.text_extractor import TextExtractor

extractor = TextExtractor("memory/text_memory.json")

file_id = "test-file-1"
file_path = "data/test.txt"

extractor.rebuild_text_memory(file_id, file_path)

print("Extracted memory:")
print(extractor.get_text_memory(file_id))
