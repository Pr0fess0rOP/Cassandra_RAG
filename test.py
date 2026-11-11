from requests import session
from app import generate_embedding


def query_rag(text):
     text_embeddings = generate_embedding(text)
     select_query = """
        SELECT content_chunk,similarity_cosine(content_vector, ?) FROM embeddings.document_vectors
        ORDER BY content_vector ANN OF ?
        LIMIT 3
        """
     prepared_stmt = session.prepare(select_query)
     result_rows = session.execute(prepared_stmt, [
            text_embeddings,
            text_embeddings 
        ])
     for row in result_rows:
         print(row[0], row[1])


query_rag('Tell about my Bangkok experiences')