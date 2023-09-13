from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import json
import os
from getpass import getpass
import openai
from uuid import uuid4

ASTRA_DB_SECURE_BUNDLE_PATH = os.environ["ASTRA_DB_SECURE_BUNDLE_PATH"] 

ASTRA_DB_APPLICATION_TOKEN = os.environ["ASTRA_DB_APPLICATION_TOKEN"]
ASTRA_DB_KEYSPACE = "vector"

# this
cluster = Cluster(
    cloud={
        "secure_connect_bundle": ASTRA_DB_SECURE_BUNDLE_PATH,
    },
    auth_provider=PlainTextAuthProvider(
        "token",
        ASTRA_DB_APPLICATION_TOKEN,
    ),
)
session = cluster.connect()
keyspace = ASTRA_DB_KEYSPACE 

openai.api_key="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"

embedding_model_name = "text-embedding-ada-002"

def find_quote_and_author(query_quote, n):
    query_vector = openai.Embedding.create(
        input=[query_quote],
        engine=embedding_model_name,
    ).data[0].embedding
    
    search_statement = f"""SELECT playerline, player FROM vector.shakespeare_cql
            ORDER BY embedding_vector ANN OF %s
            LIMIT %s;
        """
    # For best performance, one should keep a cache of prepared statements (see the insertion code above)
    # for the various possible statements used here.
    # (We'll leave it as an exercise to the reader to avoid making this code too long.
    # Remember: to prepare a statement you use '?' instead of '%s'.)
    query_values = tuple([query_vector] + [n])
    result_rows = session.execute(search_statement, query_values)

    return [
        (result_row.playerline, result_row.player)
        for result_row in result_rows
    ]

completion_model_name = "gpt-3.5-turbo"

generation_prompt_template = """"Generate an answer to a question. Use only the information in the provided documents. 
Answer with 50-100 words.  If you don't know, just say you don't know, don't try to make up an answer.  Be as truthful as possible.

REFERENCE TOPIC: "{topic}"

ACTUAL EXAMPLES:
{examples}
"""

def generate_quote(topic, n=100, author=None, tags=None):
    quotes = find_quote_and_author(query_quote=topic, n=n)
    if quotes:
        prompt = generation_prompt_template.format(
            topic=topic,
            examples="\n".join(f"  - {quote[0]}" for quote in quotes),
        )
        # a little logging:
        print("** quotes found:")
        for q, a in quotes:
            print(f"**    - {q} ({a})")
        print("** end of logging")
        #
        response = openai.ChatCompletion.create(
            model=completion_model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=320,
        )
        return response.choices[0].message.content.replace('"', '').strip()
    else:
        print("** no quotes found.")
        return None

q_topic = generate_quote("How did Juliet die?")
print("\nAn answer to the question:")
print(q_topic)