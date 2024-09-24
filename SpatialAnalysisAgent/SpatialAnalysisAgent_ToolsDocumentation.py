import os
import tomllib


current_script_dir = os.path.dirname(os.path.abspath(__file__))
Tools_Documentation_dir = os.path.join(current_script_dir, 'Tools_Documentation')

def tool_documentation_collection(tool_ID, tool_dir=Tools_Documentation_dir):
    # Initialize the tool file path variable
    tool_file = None

    # Walk through all subdirectories and files in the Tools_Documentation folder
    for root, dirs, files in os.walk(tool_dir):
        # Check if the tool file exists in any subdirectory
        for file in files:
            if file ==f'{tool_ID}.toml':
                tool_file = os.path.join(root, file)
                break # Stop once the file is found

        if tool_file:  # Exit the loop early if the file was found
            break

    # tool_file = os.path.join(tool_dir, f'{tool_ID}.toml')

    ## If the file is not found, return an empty string
    if not tool_file:
        return ""
    # #Check if the file exists
    # if not os.path.exists(tool_file):
    #     return ""

    with open(tool_file, "rb") as f:
        tool = tomllib.load(f)
    tool_parameter_str = tool['parameters']
    tool_total_str = str(tool)
    tool_total_str_lines = tool_total_str.strip().split('\n')
    # numbered_tool_total_str = ''
    # for idx, line in enumerate(tool_total_str_lines):
    #     line = line.strip(' ')
    #     numbered_tool_total_str += f"{idx + 1}. {line}\n"
    # Dynamically print each section's name and content
    output = ''
    for section, content in tool.items():
        # Automatically print section names in title case with content below it
        output += f"{section.replace('_', ' ').title()}:\n"
        output += f"{content.strip()}\n\n" if isinstance(content, str) else f"{content}\n\n"

    return output
    # return tool_total_str_lines


#***********************************************************************
# import sqlite3
#
# # Connect to the SQLite database
# def connect_to_database(db_path):
#     try:
#         conn = sqlite3.connect(db_path)
#         return conn
#     except sqlite3.Error as e:
#         print(f"Error connecting to database: {e}")
#         return None
#
#
# # Fetch all documentation records
# def fetch_all_documentation(conn):
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM documentation")
#
#     rows = cursor.fetchall()
#
#     for row in rows:
#         print(f"ID: {row[0]}, Tool Name: {row[1]}, Tool ID: {row[2]}")
#         print(f"Brief Description: {row[3]}")
#         print(f"Parameters: {row[4]}")
#         print(f"Code Example: {row[5]}")
#         print(f"Last Modified: {row[6]}")
#         print("-" * 50)
#
# # Close the connection
# def close_connection(conn):
#     if conn:
#         conn.close()
#
#
# # Main logic
# db_path = 'path_to_your_database.db'
# conn = connect_to_database(db_path)
#
# if conn:
#     fetch_all_documentation(conn)
#     close_connection(conn)