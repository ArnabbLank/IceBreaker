from langchain_core.prompts import PromptTemplate
from langchain_ollama import OllamaLLM

from outputparser.summaryOutput import summary_parser
from scraping.linkedin import lookup
from third_parties.linkedln import scrape_linkedin_profile


def ice_breaker_linkedin(name:str):
    try:
        linkedin_username = lookup(name=name)
    except Exception as e:
        print(e)
        linkedin_username = "arnab sen"
    linkedin_data = scrape_linkedin_profile(
        linkedin_profile_url=linkedin_username, mock=True
    )

    summary_template = """
    given the information about a person from linkedin {information}, I want you to create:
    1. A short summary
    2. two interesting facts about them 

    Use both information from twitter and Linkedin
    \n{format_instructions}
    """
    summary_prompt_template = PromptTemplate(
        input_variables=["information", "twitter_posts"],
        template=summary_template,
        partial_variables={
            "format_instructions": summary_parser.get_format_instructions()
        },
    )

    llm = OllamaLLM(model="llama3")

    chain = summary_prompt_template | llm | summary_parser

    res = chain.invoke(input={"information": linkedin_data})

    return res, linkedin_data.get("profile_pic_url")

if __name__ == "__main__":
    print("Hello langchain")

    print(ice_breaker_linkedin("Arnab Sen"))