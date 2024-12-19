import json
import os
from typing import List, Optional

import dotenv
import pandas as pd
from llama_index.core import PromptTemplate
from llama_index.core.output_parsers import PydanticOutputParser
from llama_index.core.query_pipeline import QueryPipeline
from llama_index.llms.ollama import Ollama
from pydantic import BaseModel, Field, ValidationError
from tqdm import tqdm

from instructions.tasks import get_tasks

# TODO: Need to include a JSON instruction guide thing after the task.
# This is to include all the prompting for outputting proper JSON.
# Ugh this JSON stuff is such a pain. Maybe I should have done someting else?
template = """###ROLE\n\n{role}\n\n\n----------------------\n\n### GENERAL CONTEXT\n\n{gen_context}\n\n\n----------------------\n\n### PATIENT NOTE\n\n{patient_note}\n\n\n----------------------\n\n### TASK\n\n{task}{uncertain}\n\n\n----------------------\n\n### OUTPUT FORMATTING\n\n{json_guide}"""

# Uncomment one of the below lines to choose whether the model is allowed to be uncertain.
uncertain = ""
# uncertain = "\nIf you are uncertain, answer -1"

role = """You are an experienced surgeon who has been asked to review an operative note for a patient who underwent surgery. You are tasked with answering a question based on information from the operative note. This information is crucial for a research project that could help many people. Please read carefully the general surgical context, the operative note, and the task instructions that follow. Please then answer the question based on the information in the prompt."""

with open("data/context.md") as f:
    gen_context = f.read()

json_guide = """
                - It is incredibly important that your answer be in properly formatted JSON
                - Once you are finished, check the JSON formatting once again to ensure that it is one line of syntactically vanilla and perfect JSON.
                - Don't forget the ending "}"
                - Do not include in the answer body quote marks or other symbols that could interfere with the JSON formatting.
"""


class Task(BaseModel):
    """Object representing the answers to a single task."""

    answer: int = Field(..., description="The answer to the task.")
    explanation: str = Field(..., description="Explanation for the answer.")
    # answer: Optional[int] = ""
    # explanation: Optional[str] = ""


# def extract_and_validate_json(output, output_parser):
#     if isinstance(output, dict):
#         # If the output is already a dictionary, use it directly
#         return output_parser.parse_obj(output)
#     elif isinstance(output, str):
#         try:
#             # Parse the JSON string
#             parsed_output = json.loads(output)
#             # Validate using Pydantic
#             validated_output = output_parser.parse_obj(parsed_output)
#             return validated_output
#         except json.JSONDecodeError as e:
#             print("JSON Decode Error:", e)
#             raise
#         except ValidationError as e:
#             print("Validation Error:", e)
#             raise
#         except Exception as e:
#             print("General Error:", e)
#             raise
#     else:
#         raise TypeError("Output must be a str or dict")
#
#
# def process_query_with_retries(
#     prompt_tmpl, output_parser, prompt_template, llm, max_retries=3
# ):
#     for attempt in range(max_retries):
#         p = QueryPipeline(chain=[prompt_tmpl, llm, output_parser], verbose=True)
#         output = p.run()
#         try:
#             validated_output = extract_and_validate_json(output, output_parser)
#             return validated_output
#         except (ValueError, json.JSONDecodeError, ValidationError):
#             print(f"Attempt {attempt + 1} failed, retrying...")
#     raise RuntimeError("Failed to get a valid response after maximum retries")


def apply_extractions(row, llm, tasks):
    patient_note = row["Text_desc"]

    # Create a dictionary and add key-value pairs for each task
    return_dict = {}
    # Append the row index with row["ID"]
    return_dict["op_note_id"] = row["ID"]

    for task in tasks:
        print(f"{row['ID']} : {task['task_name']}")
        task_name = task["task_name"]
        task_desc = task["content"]
        prompt_tmpl = template
        output_parser = PydanticOutputParser(Task)
        prompt_tmpl = output_parser.format(prompt_tmpl)
        prompt_tmpl = PromptTemplate(
            prompt_tmpl,
            role=role,
            gen_context=gen_context,
            patient_note=patient_note,
            task=task_desc,
            uncertain=uncertain,
            json_guide=json_guide,
        )
        # print the final prompt_tmpl
        # print(prompt_tmpl)
        p = QueryPipeline(chain=[prompt_tmpl, llm, output_parser], verbose=True)
        # p = QueryPipeline(chain=[prompt_tmpl, llm], verbose=True)
        # INFO: If you get a "ValueError" on the p.run() line, it is likely because the model did not output valid JSON, even though it was asked to do so.
        # Consider more aggressive prompting for it to output valid JSON.
        # Sometimes it doesn't work but you can just have it try again lol.
        # Hopefully less of a problem with Llama3:70b.

        for attempt in range(10):
            try:
                output = p.run()
                break
            except (ValueError, json.JSONDecodeError, ValidationError, TypeError) as e:
                print(f"Attempt {attempt + 1} failed, retrying... Error: {e}")
        # output = p.run()
        # try:
        #     output = process_query_with_retries(
        #         prompt_tmpl, output_parser, prompt_tmpl, llm
        #     )
        # Parse out the content from a ChatResponse datatype
        print("output is below:")
        print(output)
        print(output.answer)
        # print(output["answer"])
        # Append the result and explanation to the dictionary
        return_dict[f"{task_name}"] = output.answer
        return_dict[f"{task_name}_explanation"] = output.explanation
        # except RuntimeError as e:
        #     print(e)

    return return_dict


def main():
    print("Starting main")
    dotenv.load_dotenv()
    data_file = os.getenv("EXLAP_DATA_FILE")
    df = pd.read_csv(data_file)
    with open("data/context.md") as f:
        gen_context = f.read()
    # The LLAMA_VERSION environment variable is so it's easier to use Llama3:70b on HPG
    model_name = os.getenv("LLAMA_VERSION")
    # I increased the timeout to allow for sluggish HPG initial model loading
    # On HPG sbatch, this required 186 seconds to start an `ollama run llama3:70b` call
    llm = Ollama(model=model_name, request_timeout=1200.0, json_mode=True)
    # TODO: Add tasks
    tasks = get_tasks()

    results = []
    with tqdm(
        total=df.shape[0], desc="Processing rows", leave=True, dynamic_ncols=True
    ) as pbar:
        for index, row in df.iterrows():
            # for index, row in df.head(3).iterrows():  # for testing
            result = apply_extractions(row=row, llm=llm, tasks=tasks)
            results.append(result)
            pbar.update(1)

    # Create a DataFrame
    results_df = pd.DataFrame(results)
    # get name of output file using os module from dotenv environment variable
    # TODO: Add the EXLAP_OUTPUT_FILE environment variable to the .env file
    output_file_name = os.getenv("EXLAP_OUTPUT_FILE")
    # Save the DataFrame to a CSV file
    results_df.to_csv(output_file_name, index=False)


if __name__ == "__main__":
    main()
