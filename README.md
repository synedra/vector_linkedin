# Shakespeare sample application for DataStax Python driver

1. Using astra cli or manually grabbing from the Astra UI, populate a .env file with the following items:
   ```
   OPENAI_API_KEY=<key>
   ASTRA_DB_APPLICATION_TOKEN=<token>
   ASTRA_DB_ID=<id>
   ASTRA_DB_KEYSPACE="vector"
   ASTRA_DB_REGION="us-east1"
   ASTRA_DB_SECURE_BUNDLE_PATH=<path on your system>
   ```
2. Create a "vector" keyspace in your database using the Astra UI
3. `python -m pip -i requirements.txt`
4. Run the population command with `python populate.py` - this will take a while
5. Run the query with `python query.py <word_count> "<query>"
     Example: python query.py 50 "How did Juliet die?"
