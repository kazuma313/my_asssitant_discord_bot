from src.domain.templates.prompt.bad_word_prompte_template import BAD_WORD_PROMPT
from src.domain.entities.agents.bad_word_entities import BadWordDetection
from langchain_classic.output_parsers import OutputFixingParser
from langchain_core.output_parsers import PydanticOutputParser
from src.infrastructure.AI.models.llm import get_llm_model
from langchain_core.prompts import PromptTemplate


llm = get_llm_model(temperature=0.1, model_name="gpt-3.5-turbo-0125")


output_parser = PydanticOutputParser(pydantic_object=BadWordDetection)
BAD_WORD_PROMPT_TEMPLATE = PromptTemplate(input_variables=["text_to_check"], 
                                          template=BAD_WORD_PROMPT,
                                          partial_variables={
                                              "output_parser_format": output_parser.get_format_instructions()
                                              },
                                          output_parser=output_parser
                                          )

fixing_parser = OutputFixingParser.from_llm(parser=output_parser, llm=llm)

KLASIFIKASI_BAD_WORD_PROMPT_CHAIN = (
    BAD_WORD_PROMPT_TEMPLATE | llm | fixing_parser
)