from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains.llm import LLMChain
from langchain.chains import MapReduceDocumentsChain, ReduceDocumentsChain, StuffDocumentsChain
from textwrap import fill

llm = ChatOpenAI(
    temperature=0.1,
    model_name="gemma2:latest",
    api_key="ollama",
    base_url="http://localhost:11434/v1",
)
user_query = "Суммаризируй книгу"
# Map part: Appplied to each page
map_template = """Ниже представлен набор из книги
{book}
На основе этого списка определите информацию, которая наиболее релевантна следующему запросу:
{user_query} 
Если документ не релевантен, напишите «не релевантен».
Полезный ответ:"""
map_prompt = PromptTemplate.from_template(map_template)
map_prompt = map_prompt.partial(user_query=user_query)
map_chain = LLMChain(llm=llm, prompt=map_prompt)
# Reduce part: Applied to the list of results
reduce_template = """Ниже приведен набор частичных ответов на запрос пользователя:
{book}
Возьмите их и скомпонуйте в окончательный, консолидированный ответ на следующий запрос:
{user_query} 
Полный ответ:"""
reduce_prompt = PromptTemplate.from_template(reduce_template)
reduce_prompt = reduce_prompt.partial(user_query=user_query)
# Full chain


reduce_chain = LLMChain(llm=llm, prompt=reduce_prompt)

# Takes a list of documents, combines them into a single string, and passes this to an LLMChain
combine_documents_chain = StuffDocumentsChain(
    llm_chain=reduce_chain, document_variable_name="book"
)

# Combines and iteratively reduces the mapped documents
reduce_documents_chain = ReduceDocumentsChain(
    # This is final chain that is called.
    combine_documents_chain=combine_documents_chain,
    # If documents exceed context for `StuffDocumentsChain`
    collapse_documents_chain=combine_documents_chain,
    # The maximum number of tokens to group documents into.
    token_max=4000,
)
# Combining documents by mapping a chain over them, then combining results
map_reduce_chain = MapReduceDocumentsChain(
    # Map chain
    llm_chain=map_chain,
    # Reduce chain
    reduce_documents_chain=reduce_documents_chain,
    # The variable name in the llm_chain to put the documents in
    document_variable_name="book",
    # Return the results of the map steps in the output
    return_intermediate_steps=False,
)
def main(file_path = "harry.pdf"):
    loader = PyPDFLoader(file_path)
    book = loader.load()
    result = map_reduce_chain.invoke(book)
    return(fill(result["output_text"]))
