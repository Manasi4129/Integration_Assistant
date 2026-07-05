"""Ask questions against the built index:

    python ask.py

Type a question and get a grounded, cited answer. Ctrl-C to quit.
"""

from dotenv import load_dotenv

load_dotenv()

from src.config import settings
from src.rag import answer
from src.vector_store import VectorStore


def main():
    try:
        store = VectorStore.load(settings.index_path)
    except FileNotFoundError:
        print(f"No index at {settings.index_path}. Run: python build_index.py")
        return

    print("Marketplace Catalog Integration Assistant — ask a question (Ctrl-C to quit).\n")
    while True:
        try:
            question = input("you  > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nbye")
            break
        if not question:
            continue
        result = answer(question, store)
        print(f"\nbot  > {result['answer']}")
        if result.get("sources"):
            print(f"       sources: {', '.join(result['sources'])}\n")


if __name__ == "__main__":
    main()
