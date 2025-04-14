from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

import streamlit as st

import os
from dotenv import load_dotenv

load_dotenv()
os.environ["OPENAI_API_KEY"] =os.getenv("OPENAI_API_KEY")
## LangSmithtraking
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] =  os.getenv("LANGCHAIN_API_KEY")
## Prompt Template

if "question_history" not in st.session_state:
    st.session_state.question_history = []
   # print(st.session_state.question_history)

prompt=ChatPromptTemplate.from_messages(
    [
        ("system","You are a helpful assistant. Please respond to the user quaries"),
        ("user","Question:{question}"),
    ]
)
## streamlit framework
st.title("Langchain  with OPEN_AI")
input_text = st.text_input("Search th etopic u want")

#st.button("📝 Summarize All My Questions")
## openAI LLm
llm=ChatOpenAI(model="gpt-4o")
output_parser = StrOutputParser()
chain = prompt|llm|output_parser

#i=0
# 🧠 Summarize button
if st.button("📝 Summarize All My Questions"):
    if st.session_state.question_history:
        summary_prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant that summarizes all user questions."),
            ("user", "Here are all the questions I asked:\n\n{questions}\n\nSummarize them.")
        ])
        summary_chain = summary_prompt | llm | output_parser
        summary = summary_chain.invoke({
            "questions": "\n".join(st.session_state.question_history) ## converting list to string to give as input to user
        })
        st.subheader("Summary of Your Questions:")
        st.write(summary)
    else:
        st.info("You haven't asked any questions yet.")
# Question History

if st.button("Question History"):
    if st.session_state.question_history:
        for i,question in enumerate(st.session_state.question_history):
            st.write(i+1,question)
    else:
        st.write("No questions available yet!")
## Normal Question Answer
elif input_text:
    # i+=1
    # print("test",i)
    st.session_state.question_history.append(input_text)
    response = chain.invoke({"question": input_text})
    st.write(response)



# if input_text:
#     st.write(chain.invoke({"question":input_text}))


