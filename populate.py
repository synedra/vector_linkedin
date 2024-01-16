import json
import os
from openai import OpenAI
import cassio
from langchain.vectorstores import Cassandra
from langchain.schema import Document
from dotenv import load_dotenv
load_dotenv()

cassio.init(
    token=os.environ["ASTRA_DB_APPLICATION_TOKEN"],
    database_id=os.environ["ASTRA_DB_ID"],
)

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
from langchain.embeddings import OpenAIEmbeddings
myEmbedding = OpenAIEmbeddings()
completion_model_name = "gpt-3.5-turbo"

vector_store = Cassandra(
    embedding=myEmbedding, # <-- meaning: use the OpenAI Embeddings loaded above
    table_name="shakespeare_act5",
    session=None,  # <-- meaning: use the global defaults from cassio.init()
    keyspace="linkedin_vector",  
)

def populate_database():
    input_lines = json.load(open("./romeo_astra_act5.json"))

    input_documents = []
    current_quote = ""
    # Create documents from the quotes
    
    for input_line in input_lines:
        if (input_line["ActSceneLine"] != ""):
            (act, scene, line) = input_line["ActSceneLine"].split(".")
            location = "Act {}, Scene {}, Line {}".format(act, scene, line)
            if (scene != "3"):
                continue
            metadata = {"act": act, "scene": scene, "line": line}
        else:
            location = ""
            metadata = {}
 
        if '.' not in input_line["PlayerLine"]:
            current_quote += " " + input_line["PlayerLine"]
            continue

        quote_input = "{} : {} ".format(location, current_quote)
        current_quote = ""
        print(quote_input + "\n")

        input_document = Document(page_content=quote_input)
        input_documents.append(input_document)

    retriever = vector_store.as_retriever(search_kwargs={"k": 5})

    # Add documents to the vector store
    print(f"Adding {len(input_documents)} documents ... ", end="")
    vector_store.add_documents(documents=input_documents, batch_size=50)
    print("Done.")

generation_prompt_template = """"
Create a summary from the documents.  Answer the question using the examples in 20-50 words

REFERENCE TOPIC: {topic}

ACTUAL EXAMPLES:
{examples}
"""

def generate_quote(topic, n=10, author=None, tags=None):
    retriever = vector_store.as_retriever(search_kwargs={"k": n})
    quotes = retriever.get_relevant_documents('How did Astra die?')
    
    if quotes:
        examples = ""
        for doc in quotes:
            examples += "<line> " + doc.page_content + "</line>\n"
        

        print ("\n".join(doc.page_content for doc in quotes))
        
        system_prompt = "You will be provided with a series of sections from a Shakespearean play, delimited with xml tags. " + \
                        "Summarize the plot using the entirety of the data provided, using the act, scene and line to order the sections." 

        # Generate the answer using the prompt
        prompt = generation_prompt_template.format(
            topic=topic,
            wordcount=50,
            examples = examples
        )
        response = client.chat.completions.create(model=completion_model_name,
        messages=[{"role": "user", "content": prompt},
                  {"role": "system", "content":system_prompt}],
        temperature=0,
        max_tokens=1000)
        return response.choices[0].message.content.replace('"', '').strip()
    else:
        print("** no quotes found.")
        return None

#populate_database()

q_topic = generate_quote("How did Astra die?")
print("\nAn answer to the question:")
print(q_topic)

# Sample answer:
# Astra dies in Act 5, Scene 3. 
# She is found dead alongside Stargate. 
# It is revealed that Astra took a sleeping potion to fake her death, 
# but Stargate was not aware of this plan. 
# Astra's death causes great grief and tragedy for those involved.
