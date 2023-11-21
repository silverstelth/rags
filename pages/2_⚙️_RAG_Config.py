"""Streamlit page showing builder config."""
import streamlit as st
import openai
from streamlit_pills import pills
from typing import cast

from agent_utils import (
    RAGParams,
    RAGAgentBuilder,
)


####################
#### STREAMLIT #####
####################



st.set_page_config(page_title="RAG Pipeline Config", page_icon="🦙", layout="centered", initial_sidebar_state="auto", menu_items=None)
st.title("RAG Pipeline Config")
st.info(
    "This is generated by the builder in the above section.", icon="ℹ️"
)

if "agent_builder" in st.session_state.keys():
    agent_builder = cast(RAGAgentBuilder, st.session_state.agent_builder)
    if agent_builder.cache.system_prompt is None:
        system_prompt = ""
    else:
        system_prompt = agent_builder.cache.system_prompt
    sys_prompt_st = st.text_area("System Prompt", value=system_prompt)

    rag_params = cast(RAGParams, agent_builder.cache.rag_params)
    file_paths = st.text_input(
        "File/URL paths (not editable)", 
        value=",".join(agent_builder.cache.file_paths),
        disabled=True
    )
    include_summarization_st = st.checkbox("Include Summarization", value=rag_params.include_summarization)
    top_k_st = st.number_input("Top K", value=rag_params.top_k)
    chunk_size_st = st.number_input("Chunk Size", value=rag_params.chunk_size)
    embed_model_st = st.text_input("Embed Model", value=rag_params.embed_model)
    llm_st = st.text_input("LLM", value=rag_params.llm)
    if agent_builder.cache.agent is not None:
        if st.button("Update Agent"):
            # update the agent
            agent_builder.cache.system_prompt = sys_prompt_st
            # get agent_builder
            # We call set_rag_params and create_agent, which will
            # update the cache
            agent_builder = cast(RAGAgentBuilder, st.session_state.agent_builder)

            # TODO: decouple functions from tool functions exposed to the agent
            agent_builder.set_rag_params(
                include_summarization=include_summarization_st,
                top_k=top_k_st,
                chunk_size=chunk_size_st,
                embed_model=embed_model_st,
                llm=llm_st,
            )
            # this will update the agent in the cache
            agent_builder.create_agent()
    else:
        # show text saying "agent not created"
        st.info("Agent not created. Please create an agent in the above section.")
else:
    st.info("agent builder not created yet. Please describe your task in the above section.")
