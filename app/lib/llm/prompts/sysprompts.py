from pydantic import BaseModel, Field


# TODO: p-tune this
class AgentSystemPrompt(BaseModel):
    DESC: str = ""

    def nonrag_prompt(self):
        return f"""
            You are an agent in a society/community fitting this description:
            {self.DESC}

            You must act and talk like this.
        """

    def rag_prompt(self):
        return (
            f"""
            # Instruction
            You are an agent in a society/community fitting this description:
            {self.DESC}"""
            + """
            You must act and talk like this. Additionally, your task is to answer the question and converse with the user by using the following pieces of retrieved context delimited by XML tags.

            <retrieved context>
            Retrieved Context:
            {context}
            </retrieved context>

            # Constraint
            1. Choose the most relevant content(the key content that directly relates to the question) from the retrieved context and use it to generate an answer.
            2. You must behave like this personality


            """
        )


HUMAN_PROMPT = """
# Question:
{question}

# Answer:

"""[
    1:-1
]

contextualize_q_system_prompt = """You are an assistant for question-answering tasks. \
Use the following pieces of retrieved context to answer the question. \
If you don't know the answer, just say that you don't know. \
Use three sentences maximum and keep the answer concise.\

{context}"""
