import asyncio
import os
import re
import sys
import tomllib
import tomli_w
from langchain_openai import ChatOpenAI



# Get the directory of the current script
current_script_dir = os.path.dirname(os.path.abspath(__file__))
# Add the directory to sys.path
if current_script_dir not in sys.path:
    sys.path.append(current_script_dir)

import  QGIS_tool_creation_Helper as Helper


# Tools_Documentation_dir = r"D:\Onedrive\OneDrive - The Pennsylvania State University\PhD Work\SpatialAnalysisAgent_Reasearch\Plugin\toml\TOML_10"
Tools_Documentation_dir = r"D:\Onedrive\OneDrive - The Pennsylvania State University\PhD Work\SpatialAnalysisAgent_Reasearch\Plugin\toml\TT"

def tool_documentation_collection(tool_ID, tool_dir=Tools_Documentation_dir):
    tool_file = os.path.join(tool_dir, f'{tool_ID}.toml')

    # Check if the file exists
    if not os.path.exists(tool_file):
        return ""

    with open(tool_file, "rb") as f:
        tool = tomllib.load(f)
    tool_parameter_str = tool['parameters']
    algorithm_id = tool['tool_ID']
    # algorithm_id = "qgis:buffer"

    tool_parameter_lines = tool_parameter_str.strip().split('\n')
    numbered_tool_parameter_str = ''
    for idx, line in enumerate(tool_parameter_lines):
        line = line.strip(' ')
        numbered_tool_parameter_str += f"{idx + 1}. {line}\n"

    return numbered_tool_parameter_str, algorithm_id



def append_code_to_toml(tool_ID, code_sample, tool_dir=Tools_Documentation_dir):
    tool_file = os.path.join(tool_dir, f'{tool_ID}.toml')

    # Check if the file exists
    if not os.path.exists(tool_file):
        print(f"TOML file for tool {tool_ID} does not exist.")
        return

    # Load the existing TOML file
    with open(tool_file, "rb") as f:
        tool_data = tomllib.load(f)

    # # Replace the sample code in the code_example section if it exists, otherwise add it
    # tool_data['code_example'] = code_sample

    # Append the sample code to the code_example section
    if 'code_example' in tool_data:
        tool_data['code_example'] += f"\n{code_sample}"
    else:
        tool_data['code_example'] = code_sample

    # Write the updated content back to the file using tomli_w
    with open(tool_file, "wb") as f:
        tomli_w.dump(tool_data, f)


def formatting_toml_file(tool_ID, tool_dir=Tools_Documentation_dir):
    #file_path = r"D:\Onedrive\OneDrive - The Pennsylvania State University\PhD Work\SpatialAnalysisAgent_Reasearch\Plugin\toml\toml\gdal_slope.toml"
    # Read the original file
    tool_file = os.path.join(tool_dir, f'{tool_ID}.toml')
    with open(tool_file, 'r', encoding = 'utf-8') as file:
        # tool = tomllib.load(f)
        # tool_parameter_str = tool['parameters']
        toml_content = file.read()

    # Function to replace single quotes with triple quotes for specific sections
    def replace_single_with_triple_quotes(section_name, content):
        # Pattern to match the section content that uses single quotes
        pattern = rf'({section_name}\s*=\s*)\"(.*?)\"'
        # Replace with triple quotes
        return re.sub(pattern, r'\1"""\2"""', content, flags=re.DOTALL)

    # Sections that need to be reformatted
    sections_to_format = ['brief_description', 'full_description', 'parameters', 'code_example']

    # Apply reformatting to each section
    for section in sections_to_format:
        toml_content = replace_single_with_triple_quotes(section, toml_content)


    # Replace occurrences of `n\` (escaped newline in TOML) with proper multiline format
    # Specifically, we will place strings in between triple double-quotes for basic multiline handling
    updated_code_example = toml_content.replace('\\n', '\n')

    # Write the updated content back into the file
    # updated_file_path = r'D:\Onedrive\OneDrive - The Pennsylvania State University\PhD Work\SpatialAnalysisAgent_Reasearch\Plugin\toml\toml\gdal_slope.toml'
    with open(tool_file, 'w', encoding='utf-8') as updated_file:
        updated_file.write(updated_code_example)

def process_toml_files_in_directory(directory):
    for file_name in os.listdir(directory):
        if file_name.endswith(".toml"):
            tool_file_name = file_name.split(".")[0]
            numbered_tool_parameter_str, algorithm_id = tool_documentation_collection(tool_ID = tool_file_name)
            Tooldoc_prompt_str = Helper.create_CodeSample_prompt(tool_doc=numbered_tool_parameter_str, algorithm_id=algorithm_id)
            
            # Generate code sample using OpenAI model
            OpenAI_key = Helper.get_OpenAI_key()

            model = ChatOpenAI(api_key=OpenAI_key, model="gpt-4o", temperature=1)
            CodeSample_prompt_str_chunks = asyncio.run(Helper.fetch_chunks(model, Tooldoc_prompt_str))
            LLM_reply_str = Helper.convert_chunks_to_str(chunks=CodeSample_prompt_str_chunks)

            # Extract Python code and clean it
            if 'python' in LLM_reply_str:
                sample_code = LLM_reply_str.split('python', 1)[1].strip()
            sample_code = sample_code.replace("\\n", "\n")

            # Append the sample code to the TOML file
            append_code_to_toml(tool_ID=tool_file_name, code_sample=sample_code)

            # Reformat the TOML file for multiline strings
            formatting_toml_file(tool_ID =tool_file_name)

            print(f"Processed file: {tool_file_name}.toml")

# Run the processing function for all TOML files in the directory
process_toml_files_in_directory(Tools_Documentation_dir)






