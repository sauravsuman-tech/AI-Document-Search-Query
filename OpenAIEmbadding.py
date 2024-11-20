from ssl import Purpose
from llama_index import GPTSimpleVectorIndex,SimpleDirectoryReader,LLMPredictor,PromptHelper,ServiceContext
from langchain.chat_models import ChatOpenAI
from llama_index.node_parser import SimpleNodeParser
from langchain import OpenAI
import os

os.environ['OPENAI_API_KEY'] = 'your open api key'
llm_predictor = LLMPredictor(llm=OpenAI(temperature=0, model_name="text-moderation-007"))
directory_path="data"
file_metadata = lambda x: {"filename": x}
documents = SimpleDirectoryReader(directory_path,file_metadata=file_metadata).load_data()

parser = SimpleNodeParser()
nodes = parser.get_nodes_from_documents(documents)

max_input_size = 4096
num_output = 100
max_chunk_overlap = 20
prompt_helper = PromptHelper(max_input_size, num_output, max_chunk_overlap)
service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor, prompt_helper=prompt_helper)
index = GPTSimpleVectorIndex(
    nodes, service_context=service_context
)

index.save_to_disk('index.json')
