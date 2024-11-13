from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from third_parties.linkedln import scrape_linkedin_profile

if __name__ == "__main__":
    print("Hello langchain")

    summary_template = """
    given the LinkedIn information {information} about as person I want you to create:
    1. a short summary
    2. two interesting facts about them"""

    summary_prompt_template = PromptTemplate(
        input_variables=["information"], template=summary_template)

    llm = ChatOpenAI(model_name="gpt-3.5-turbo")

    chain = summary_prompt_template | llm

    data = scrape_linkedin_profile("https://www.linkedin.com/in/arnab-sen-7020b8200/", mock=True)

    res = chain.invoke(input={"information": data})

    print(res)