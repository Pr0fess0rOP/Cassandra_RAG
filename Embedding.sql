CREATE KEYSPACE IF NOT EXISTS embeddings
   WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : '1' };

USE embeddings;

CREATE TABLE IF NOT EXISTS embeddings.document_vectors (
  record_id timeuuid,
  id uuid,
  content_chunk text,
  content_vector VECTOR <FLOAT, 768>,
  created_at timestamp,
  PRIMARY KEY (id, created_at)
)
WITH CLUSTERING ORDER BY (created_at DESC);

CREATE INDEX IF NOT EXISTS edv_ann_index
  ON embeddings.document_vectors(content_vector) USING 'sai';