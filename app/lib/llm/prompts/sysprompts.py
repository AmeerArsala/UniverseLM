from pydantic import BaseModel, Field


# TODO: p-tune this
class AgentSystemPrompt(BaseModel):
    NAME: str = ""
    DESC: str = ""

    recipient: str = ""

    def recipient_prompt(self, rag: bool) -> str:
        if len(self.recipient) == 0:
            return ""
        else:
            if rag:
                return f". The identity of the user you are currently speaking with is {self.recipient}, so respond to the user like you would to {self.recipient}, because that's who they are"
            else:
                return f" Also, you are currently speaking to {self.recipient}, so keep that in mind with your response."

    def nonrag_prompt(self):
        return f"""
            You are an agent in a society/community. You fit this description:
            {self.DESC}

            You must act and talk like that. You are known as {self.NAME}. Always stay in character and behave like the description says.{self.recipient_prompt(rag=False)}
        """

    def rag_prompt(self):
        return (
            f"""
            # Instruction
            You are an agent in a society/community. You fit this description:
            {self.DESC}
            You must act and talk like that. You are known as {self.NAME}{self.recipient_prompt(rag=True)}."""
            + """
            As you behave in character, your task is to answer the question and converse with the user while staying in character by using the following pieces of retrieved context delimited by XML tags.
            
            <retrieved context>
            Retrieved Context:
            {context}
            </retrieved context>

            # Constraint
            1. Choose the most relevant content(the key content that directly relates to the question) from the retrieved context and use it to generate an answer.
            2. You must behave like this personality and always stay in character


            """
        )


HUMAN_PROMPT = """
# Question:
{question}

# Answer:

"""[
    1:-1
]
