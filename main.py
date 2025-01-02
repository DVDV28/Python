import os
from openai import OpenAI
from prompt import prompt_text

class R_Converter:
    def __init__(self, api_key, r_script_path, output_dir):
        """
        Initialise the R_Converter class.

        Args:
            api_key (str): API key for authenticating with the OpenAI service.
            r_script_path (str): Path to the R script to be converted.
            output_dir (str): Directory where the converted Python script will be saved.

        Raises:
            FileNotFoundError: If the R script does not exist at the specified path.
        """
        if not os.path.exists(r_script_path):
            raise FileNotFoundError(f"R script not found: {r_script_path}")
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok = True)
        
        self.api_key = api_key
        self.r_script_path = r_script_path
        self.output_dir = output_dir

    def read_r_script(self) -> str :
        """Read the R script from the input file.

        Returns:
            str: The contents of the R script file.
        """
        with open(self.r_script_path, 'r') as input_file:
            return input_file.read()
        
    def write(self, python_code):
        """Write the Python code to a file in the output directory.

        Args:
            python_code (str): The Python code to write to file.
        """
        file_name = os.path.basename(self.r_script_path)
        output_path = os.path.join(self.output_dir, file_name.replace('.R', '.py'))
        with open(output_path, 'w') as output_file:
            output_file.write(python_code)

    def convert(self):
        """Convert the imported R script to Python using the LLM."""

        input_r_script = self.read_r_script()

        client = OpenAI()

        response = client.chat.completions.create(
            model = "gpt-4o-mini",
            messages = [
                {"role": "system", "content": "You are a machine that converts R scripts to Python."},
                {"role": "user", "content": prompt_text.format(input_r_script = input_r_script)}
            ],
            temperature = 0
        )

        python_script = response.choices[0].message.content.strip()
        self.write(os.path.basename(self.r_script_path), python_script)


def main(input_dir: str, output_dir: str):
    """
    Main entry point for the script.

    This function reads R scripts from a specified input directory, converts them
    to Python using the OpenAI API, and writes the converted Python scripts to an
    output directory.

    Environment Variables:
        OPENAI_API_KEY (str): The API key for authenticating with the OpenAI service.
    """
    api_key = os.getenv('OPENAI_API_KEY')
    
    input_files = os.listdir(input_dir)
    input_files = [file for file in input_files if file.endswith('.R')]

    for file_name in input_files:
        converter = R_Converter(api_key, 
                                os.path.join(input_dir, file_name),
                                output_dir)
        converter.convert()

if __name__ == "__main__":
    main(input_dir = 'C:/Project_Euler/Solution Scripts', 
         output_dir = 'C:/Project_Euler/Converted Scripts')
