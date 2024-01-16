# Shakespeare sample application for DataStax Python driver

1. Let the environment finish running the pip install command.
2. Using astra cli or manually grabbing from the Astra UI, populate a .env file with the following items.

   ```
   OPENAI_API_KEY=<key>
   ASTRA_DB_APPLICATION_TOKEN=<token>
   ASTRA_DB_ID=<id>
   ```

   - Get an Astra account/database at https://astra.datastax.com
   - The DB ID can be found on the main page
   - You can get an application token from the database details page

3. `python -m pip -i requirements.txt`
4. Run the population command with `python populate.py` - this will take a while as it populates the database, then it will give you the response
