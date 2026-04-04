import os 
import logging 
from llama_index.core import SimpleDirectoryReader, Document

logger = logging.getLogger(__name__)

def load_documents(directory_path : str) -> list[Document]:
    if not os.path.isdir(directory_path):
        raise FileNotFoundError(f"Directory not found: {directory_path}")
    
    reader = SimpleDirectoryReader(
        input_dir = directory_path,
        required_exts = [".pdf", ".txt"],
        recursive = False,
        filename_as_id = True
    )

    documents = reader.load_data()

    if not documents:
        raise ValueError(f"No documents found in: {directory_path}")
    
    logger.info(f"Loaded {len(documents)} document(s) from {directory_path}")
    return documents