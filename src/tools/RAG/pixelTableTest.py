import pixeltable as pxt
import pixeltable.functions as pxtf
from pixeltable.functions import openai, huggingface
from pixeltable.iterators import DocumentSplitter

# Manage your tables by directories
directory = "my_docs"
pxt.drop_dir(directory, if_not_exists="ignore", force=True)
pxt.create_dir("my_docs")

# Create a document table and add a PDF
docs = pxt.create_table(f'{directory}.docs', {'doc': pxt.Document})
docs.insert([{'doc': 'https://github.com/pixeltable/pixeltable/raw/release/docs/resources/rag-demo/Jefferson-Amazon.pdf'}])

# Create chunks view with sentence-based splitting
chunks = pxt.create_view(
    'doc_chunks',
    docs,
    iterator=DocumentSplitter.create(document=docs.doc, separators='sentence')
)

# Explicitly create the embedding function object
embed_model = huggingface.sentence_transformer.using(model_id='all-MiniLM-L6-v2')
# Add embedding index using the function object
chunks.add_embedding_index('text', string_embed=embed_model)

# Define query function for retrieval - Returns a DataFrame expression
@pxt.query
def get_relevant_context(query_text: str, limit: int = 3):
    sim = chunks.text.similarity(query_text)
    # Return a list of strings (text of relevant chunks)
    return chunks.order_by(sim, asc=False).limit(limit).select(chunks.text)

# Build a simple Q&A table
qa = pxt.create_table(f'{directory}.qa_system', {'prompt': pxt.String})

# 1. Add retrieved context (now a list of strings)
qa.add_computed_column(context=get_relevant_context(qa.prompt))

# 2. Format the prompt with context
qa.add_computed_column(
    final_prompt=pxtf.string.format(
        """
        PASSAGES:
        {0}

        QUESTION:
        {1}
        """,
        qa.context,
        qa.prompt
    )
)

# 4. Generate the answer using the well-formatted prompt column
qa.add_computed_column(
    answer=openai.chat_completions(
        model='gpt-4o-mini',
        messages=[{
            'role': 'user',
            'content': qa.final_prompt
        }]
    ).choices[0].message.content
)

# Ask a question and get the answer
qa.insert([{'prompt': 'What can you tell me about Amazon?'}])
print("--- Final Answer ---")
print(qa.select(qa.answer).collect())
