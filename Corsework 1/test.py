print(f"Loading corpus from: {CORPUS}")

try:
    with open(CORPUS, 'r', encoding='utf-8') as f:
        all_lines = f.readlines()

    corpus_documents = []
    current_document = []

    # Updated regex pattern to capture titles of all levels (lines starting and ending with one or more '=')
    split_pattern = re.compile(r'^\s*=[\s=]*[^=\n]*[\s=]*=[\s=]*$')

    for line in all_lines:
        line_stripped = line.strip()

        # Skip empty lines or lines that are likely noise
        if not line_stripped or line_stripped.startswith('<') or len(line_stripped) < 3:
             continue

        # Check if the line is a section title
        if split_pattern.match(line):
            # If there's content in the current document, add it to the list
            if current_document:
                doc = ' '.join(current_document).strip()
                if doc:
                    corpus_documents.append(doc)
                current_document = []
            # Skip the title line itself
            continue

        # Otherwise, add the line to the current document
        current_document.append(line_stripped)

    # Add the last document if it exists
    if current_document:
        doc = ' '.join(current_document).strip()
        if doc:
            corpus_documents.append(doc)

    print(f"Successfully loaded and split corpus into {len(corpus_documents)} documents (sections).")

    # Check if the corpus was loaded successfully
    if len(corpus_documents) > 0:
        print("\n--- Corpus Head (First 3 lines) ---")
        for doc in corpus_documents[:3]:
            print(doc.strip())
        print("-----------------------------------")
    else:
        print("\n--- Corpus Head ---")
        print("Corpus is empty or failed to load properly.")
        print("-------------------")


except FileNotFoundError:
    print(f"Error: Corpus file not found at {CORPUS}")
    corpus_documents = []
except Exception as e:
    print(f"An unexpected error occurred: {e}")
    corpus_documents = []