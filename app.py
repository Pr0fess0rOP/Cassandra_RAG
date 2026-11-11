from cassandra.cluster import Cluster
from cassandra.query import PreparedStatement, BoundStatement
import uuid
import datetime
import requests

cluster = Cluster(['127.0.0.1'],port=9042)
session = cluster.connect()

def generate_embedding(text):
    embedding_url = 'http://localhost:11434/api/embed'
    body = {
        "model": "nomic-embed-text",
        "input": text
    }

    response = requests.post(embedding_url, json = body)
    return response.json()['embeddings'][0] 

def insert_chunk(content, vector):
    id = uuid.uuid4()
    content_chunk = content
    content_vector = vector
    created_at = datetime.datetime.now()
    insert_query = """
        INSERT INTO embeddings.document_vectors (record_id, id, content_chunk, content_vector, created_at)
        VALUES (now(), ?, ?, ?, ?)
        """
    prepared_stmt = session.prepare(insert_query)
    session.execute(prepared_stmt, [
        id, 
        content_chunk, 
        content_vector, 
        created_at
    ])

def insert_sample_data_in_cassandra():
  sentences = [
    "The aroma of freshly baked bread wafted through the quaint bakery nestled in the cobblestone streets of Paris, making Varun feel like time stood still.",
    "Sipping a spicy masala chai in a bustling tea stall in Mumbai, Varun felt he was tasting the very soul of the city.",
    "The sushi in a small Tokyo diner was so fresh, it felt like Varun was on a culinary journey to the sea itself.",
    "Under the starry desert sky in Morocco, Varun enjoyed a lamb tagine that tasted like a dream cooked slowly over a fire.",
    "The cozy Italian trattoria served the creamiest risotto, perfectly capturing the heart of Tuscany on a plate, which Varun savored with delight.",
    "Enjoying fish tacos on a sunny beach in Mexico, with the waves crashing nearby, made the flavors unforgettable for Varun.",
    "The crispy waffles drizzled with syrup at a Belgian café were worth every minute of waiting, as Varun indulged in the decadent treat.",
    "A bowl of warm pho in a roadside eatery in Hanoi felt like comfort wrapped in a broth of herbs and spices, giving Varun a sense of warmth.",
    "Sampling chocolate truffles in a Swiss chocolate shop, Varun found himself in a moment of pure bliss amidst snow-capped mountains.",
    "The street food stalls in Bangkok served fiery pad Thai that left Varun with a tangy memory of the city’s vibrant energy."
    ]
  for sentence in sentences:
     vector = generate_embedding(sentence)
     insert_chunk(sentence, vector)

insert_sample_data_in_cassandra()