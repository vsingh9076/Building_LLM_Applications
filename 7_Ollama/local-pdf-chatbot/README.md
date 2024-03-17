# Chat with Multiple PDFs with Ollama and ChromaDB


## Quickstart

### RAG runs offline on local CPU

1. Clone the repository to your local machine.

2. Create a Virtual Environment:

```
python3 -m venv myenv
source myenv/bin/activate
```
   
3. Install the requirements: 

```
pip install -r requirements.txt
```

4. Install <a href="https://ollama.ai">Ollama</a> and pull LLM model specified in config.yml

5. Run the LLama2 model using Ollama

```
ollama pull llama2
ollama run llama2
```

6. Run the app.py file using the Streamlit CLI. Execute the following command:

```
streamlit run app.py
```