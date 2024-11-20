import os
import openai
from dotenv import load_dotenv
from llama_index import GPTSimpleVectorIndex, SimpleDirectoryReader, LLMPredictor, PromptHelper,ServiceContext
from langchain.llms import AzureOpenAI
from langchain.embeddings import OpenAIEmbeddings
from llama_index import LangchainEmbedding
from llama_index.node_parser import SimpleNodeParser
from llama_index.embeddings.openai import OpenAIEmbedding
from datetime import datetime
import openpyxl
import time

openai.api_type = "azure"
openai.api_version = "2022-12-01"
openai.api_base = "https://{resourcename}.openai.azure.com/"
os.environ['OPENAI_API_KEY']="Azure Open AI Key"
deployment_name = "gpt-35-turbo" #model name
llm = AzureOpenAI(deployment_name=deployment_name)
llm_predictor = LLMPredictor(llm=llm)
prompt_helper = PromptHelper(max_input_size=100, num_output=20, max_chunk_overlap=20, chunk_size_limit=100)
service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor, prompt_helper=prompt_helper,embed_model=OpenAIEmbedding(embed_batch_size=1))

index = GPTSimpleVectorIndex.load_from_disk(
'index.json',
service_context=service_context
)

Row=4
# workbook = xlsxwriter.Workbook("Result/logs.xlsx")
# worksheet = workbook.add_worksheet()
def writeToExcel(d,query,response,filename,QuationType,QuationBoundry,score):
    global Row
    wb = openpyxl.load_workbook('Result/logs.xlsx')
    ws = wb.get_sheet_by_name('Sheet1')
    ws.append([str(d),str(query),str(response),str(score),str(filename),str(QuationType),str(QuationBoundry)])
    wb.save('Result/logs.xlsx')
    wb.close()
    # worksheet.write("B"+str(Row),str(d))
    # worksheet.write("C"+str(Row),str(query))
    # worksheet.write("D"+str(Row),str(response))
    # worksheet.write("E"+str(Row),str(score))
    # worksheet.write("F"+str(Row),str(filename))
    # worksheet.write("G"+str(Row),str(QuationType))
    # worksheet.write("H"+str(Row),str(QuationBoundry))
    # Row=Row+1


def GetResult(query,QuationType,QuationBoundry):
    response = index.query(query,mode="embedding",response_mode="default")

    print(response.source_nodes[0].score)
    print("Query : ",query,"\n")
    print("Answer :",response.response)
    # print(response.source_nodes[0].node.extra_info)
    # writeToExcel(datetime.now(),query,response.response,response.source_nodes[0].node.extra_info,QuationType,QuationBoundry,response.source_nodes[0].score)


QUESTION=[
    "Amazon Elasticsearch Service ",
  "Amazon Kinesis Data Firehose",
  "How Does AWS Lake Form?",
  "what is  EventBridge",
  "tell me about amazon email service",
  "who is the founder of Microsoft",
  "what are the corporate acquisitions of Microsoft",
  "why Microsofr has been criticized?",
  "tell me about Microsoft Corporation",
  "Who replaced Gates and when in Microsoft",
  "tell me about Yashwant Kumar",
  "How many year of expreance yashwant has ",
  "contact info yashwant kumar ",
  "what are the skilss of yashwant kumar",
  "did yashwant has any presonal project?",
  "Who had composed the original Ramayana?",
  "Lakshmana is considered to be the incarnation of whom?",
  "What was the name of Lord Rama's father?",
  "where does rama styed during exile?",
  "did Lord Rama is considered to be the incarnation of Lord Vishnu?",
  "tell me about google",
  "who kills ravan?",
  "who is Hanuman?",
  "who created Shree Jagannath Temple?",
  "when did firstsource Founded?"
]

# for query in QUESTION:
#     GetResult(query)

while(True):
    query=input("enter your Query\n")
    # QuationType=input("Your Question is Contextual?(Yes/No)\n")
    # QuationBoundry=input("Your Questions is within conrpus (Yes/No)\n")
    ST=time.time()
    GetResult(query,"Yes","Yes")
    ET=time.time()
    print("Total Time Consumed : ",ET-ST)



