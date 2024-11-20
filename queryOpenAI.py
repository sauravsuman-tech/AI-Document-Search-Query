import time
from llama_index import GPTSimpleVectorIndex
import os
from llama_index import GPTSimpleVectorIndex, LLMPredictor, PromptHelper,ServiceContext
from langchain.chat_models import ChatOpenAI
from llama_index.embeddings.openai import OpenAIEmbedding


os.environ['OPENAI_API_KEY'] = 'open api key'
llm = ChatOpenAI(model_name="gpt-3.5-turbo")
llm_predictor = LLMPredictor(llm=llm)
prompt_helper = PromptHelper(max_input_size=3000, num_output=20, max_chunk_overlap=20, chunk_size_limit=1000)
service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor, prompt_helper=prompt_helper,embed_model=OpenAIEmbedding(embed_batch_size=1))

index = GPTSimpleVectorIndex.load_from_disk(
'index.json',
service_context=service_context
)

def GetResult(query):
    start_time = time.time()
    response = index.query(query,mode="embedding",response_mode="default")

    end_time = time.time()
    time_taken = end_time - start_time
    print(f"Time taken: {time_taken:.2f} seconds")
    return response.response
