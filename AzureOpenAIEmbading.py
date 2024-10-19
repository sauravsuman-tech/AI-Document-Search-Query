import os
import openai
from dotenv import load_dotenv
from llama_index import GPTSimpleVectorIndex, SimpleDirectoryReader, LLMPredictor, PromptHelper,ServiceContext
from langchain.llms import AzureOpenAI
from langchain.embeddings import OpenAIEmbeddings
from llama_index import LangchainEmbedding
from llama_index.node_parser import SimpleNodeParser
from llama_index.embeddings.openai import OpenAIEmbedding
import time


resourcename="saurav"
ST=time.time()
openai.api_type = "azure"
openai.api_version = "2022-12-01"
openai.api_base = "https://saurav.openai.azure.com/"
os.environ['OPENAI_API_KEY']="67bfdc8b80324eb385349ca8a1459f14"
deployment_name = "text-embedding-ada-002"
max_input_size = 100
num_output = 20
chunk_size_limit =50  # token window size per document
max_chunk_overlap = 0 # overlap for each token fragment
llm = AzureOpenAI(deployment_name=deployment_name)
llm_predictor = LLMPredictor(llm=llm)
embedding_llm = LangchainEmbedding(OpenAIEmbeddings())
prompt_helper = PromptHelper(max_input_size=max_input_size, num_output=num_output, max_chunk_overlap=max_chunk_overlap, chunk_size_limit=chunk_size_limit)
service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor, prompt_helper=prompt_helper,embed_model=OpenAIEmbedding(embed_batch_size=1))
# Read txt files from data directory
directory_path="data"
DirList=subdirs = [x[0] for x in os.walk(directory_path)]
print(DirList)
documentList=[]
for dir in DirList:
    print(dir)
    file_metadata = lambda x: {"filename": x}
    document = SimpleDirectoryReader(dir,file_metadata=file_metadata).load_data()
    print(type(documentList),type(document))
    documentList=documentList+document

parser = SimpleNodeParser()
nodes = parser.get_nodes_from_documents(documentList)

index = GPTSimpleVectorIndex(
    nodes, service_context=service_context
)

index.save_to_disk('index.json')
ET=time.time()
print("Total Time Consumed : ",ET-ST)
