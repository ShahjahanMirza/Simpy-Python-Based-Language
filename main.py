# simpy_app.py

import streamlit as st
import re
import sys
import io

# Define the keyword mapping using regular expressions
keyword_mapping = {
    # Control Keywords
    r'\bcheck\b': 'if',
    r'\balso\b': 'elif',
    r'\botherwise\b': 'else',
    r'\bloopwhile\b': 'while',
    r'\brepeat\b': 'for',
    r'\bbreak\b': 'break',      # Loop Control
    r'\bcontinue\b': 'continue',# Loop Control

    # Function Definition and Return
    r'\bcreate\b': 'def',
    r'\bgiveback\b': 'return',

    # Data Types
    r'\bwhole\b': 'int',
    r'\bdecimal\b': 'float',
    r'\btext\b': 'str',
    r'\bflag\b': 'bool',
    r'\barray\b': 'list',
    r'\bmap\b': 'dict',

    # Comparison Operators
    r'\bequals\b': '==',
    r'\bnotequals\b': '!=',
    r'\bgreater\b': '>',
    r'\bless\b': '<',
    r'\bgreaterequal\b': '>=',
    r'\blessequal\b': '<=',

    # Logical Values
    r'\byes\b': 'True',
    r'\bno\b': 'False',

    # Logical Operators
    r'\bboth\b': 'and',
    r'\beither\b': 'or',
    r'\bnothaving\b': 'not',

    # Exception Handling
    r'\battempt\b': 'try',
    r'\bhandle\b': 'except',
    r'\bafterall\b': 'finally',
    r'\btrigger\b': 'raise',
    r'\bensure\b': 'assert',

    # Variable Scope
    r'\buniversal\b': 'global',
    r'\bouter\b': 'nonlocal',

    # Functionality Keywords
    r'\banon\b': 'lambda',
    r'\bproduce\b': 'yield',
    r'\bskipop\b': 'pass',

    # Import Statements
    r'\binclude\b': 'import',
    r'\boutof\b': 'from',
    r'\balias\b': 'as',

    # Context Managers
    r'\busing\b': 'with',

    # Identity and Membership Operators
    r'\bbe\b': 'is',
    r'\bnotbe\b': 'is not',
    r'\binside\b': 'in',
    r'\boutside\b': 'not in',

    # Deletion of Objects
    r'\bremove\b': 'del',

    # Built-in Functions
    r'\bdisplay\b': 'print',
    r'\blength\b': 'len',
    r'\bgetinput\b': 'input',
    r'\bkind\b': 'type',
    r'\bseries\b': 'range',
    r'\btotal\b': 'sum',
    r'\bmaximum\b': 'max',
    r'\bminimum\b': 'min',
    r'\babsolute\b': 'abs',
    r'\bapproximate\b': 'round',
    r'\bitemize\b': 'enumerate',
    r'\bcombine\b': 'zip',
    r'\bapply\b': 'map',
    r'\bselect\b': 'filter',
    r'\barranged\b': 'sorted',
    r'\baccess\b': 'open',
    r'\bassist\b': 'help',
    r'\bisofkind\b': 'isinstance',
    r'\battributes\b': 'dir',

    # Class Definition
    r'\bblueprint\b': 'class',
}

simpy_keywords = [
    'check', 'also', 'otherwise', 'loopwhile', 'repeat', 'break', 'continue',
    'create', 'giveback', 'whole', 'decimal', 'text', 'flag', 'array', 'map',
    'equals', 'notequals', 'greater', 'less', 'greaterequal', 'lessequal',
    'yes', 'no', 'both', 'either', 'nothaving', 'attempt', 'handle', 'afterall',
    'trigger', 'ensure', 'universal', 'outer', 'anon', 'produce', 'skipop',
    'include', 'outof', 'alias', 'using', 'be', 'notbe', 'inside', 'outside',
    'remove', 'display', 'length', 'getinput', 'kind', 'series', 'total',
    'maximum', 'minimum', 'absolute', 'approximate', 'itemize', 'combine',
    'apply', 'select', 'arranged', 'access', 'assist', 'isofkind', 'attributes',
    'blueprint',
]

# Token specification
token_specification = [
    ('COMMENT',    r'#.*'),                         # Comments
    ('NEWLINE',    r'\n'),                          # Line endings
    ('SKIP',       r'[ \t]+'),                      # Spaces and tabs
    ('STRING',     r'(\".*?\"|\'.*?\')'),           # String literals
    ('NUMBER',     r'\b\d+(\.\d*)?\b'),             # Integer or decimal numbers
    ('OPERATOR',   r'==|!=|<=|>=|<|>|[+\-*/%=]'),   # Operators
    ('DELIMITER',  r'[\(\)\[\]\{\},:]'),            # Delimiters
    ('IDENTIFIER', r'\b[a-zA-Z_][a-zA-Z_0-9]*\b'),  # Identifiers
    ('MISMATCH',   r'.'),                           # Any other character
]
# Compile regex patterns
token_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specification)
compiled_regex = re.compile(token_regex)

# Function to tokenize Simpy code
def tokenize_simpy_code(simpy_code):
    tokens = []
    for mo in compiled_regex.finditer(simpy_code):
        kind = mo.lastgroup
        value = mo.group()
        if kind == 'SKIP' or kind == 'NEWLINE' or kind == 'COMMENT':
            continue
        elif kind == 'IDENTIFIER' and value in simpy_keywords:
            kind = 'KEYWORD'
        elif kind == 'MISMATCH':
            raise RuntimeError(f'Unexpected character {value!r}')
        tokens.append((kind, value))
    return tokens

# Function to translate Simpy code to Python code with explanations
def translate_simpy_to_python_with_explanation(simpy_code):
    explanations = []
    python_code = simpy_code  # Start with the original code
    # Sort the keywords by length in descending order to prevent partial replacements
    sorted_keywords = sorted(keyword_mapping.items(), key=lambda x: len(x[0]), reverse=True)
    for simpy_keyword, python_keyword in sorted_keywords:
        # Find all occurrences of the Simpy keyword
        matches = re.findall(simpy_keyword, python_code)
        for match in matches:
            # Explain the replacement
            explanation = f"Replacing `{match}` with `{python_keyword}`"
            explanations.append(explanation)
        # Replace the Simpy keyword with the Python keyword
        python_code = re.sub(simpy_keyword, python_keyword, python_code)
    return python_code, explanations

# Function to translate Simpy code to Python code
def translate_simpy_to_python(simpy_code):
    # Sort the keywords by length in descending order to prevent partial replacements
    sorted_keywords = sorted(keyword_mapping.items(), key=lambda x: len(x[0]), reverse=True)
    for simpy_keyword, python_keyword in sorted_keywords:
        simpy_code = re.sub(simpy_keyword, python_keyword, simpy_code)
    return simpy_code

# Sample Simpy Programs
sample_programs = {
    "Hello World": '''display("Hello, World!")''',

    "Simple Function": '''create add_numbers(a, b):
    giveback a + b

result = add_numbers(5, 7)
display("The sum is:", result)''',

    "Control Flow": '''number = 10

check number greater 0:
    display("Positive number")
also number equals 0:
    display("Zero")
otherwise:
    display("Negative number")''',

    "Loopwhile Example": '''counter = 5

loopwhile counter greater 0:
    display("Countdown:", counter)
    counter = counter - 1
display("Blast off!")''',

    "Repeat (For Loop) Example": '''numbers = [1, 2, 3, 4, 5]

repeat num inside numbers:
    display("Number:", num)''',

    "Working with Data Types": '''num1 = 10
num2 = 3.14
message = "Simpy is fun!"
is_active = yes

display("Whole number:", num1)
display("Decimal number:", num2)
display("Message:", message)
display("Is Active:", is_active)''',

    "Using Arrays and Maps": '''fruits = ["apple", "banana", "cherry"]
ages = {"Alice": 30, "Bob": 25}

display("Fruits:", fruits)
display("Ages:", ages)''',

    "Function with Loop": '''create factorial(n):
    result = 1
    repeat i inside series(1, n + 1):
        result = result * i
    giveback result

number = 5
display("Factorial of", number, "is", factorial(number))''',

    "Nested Control Structures": '''number = 7

check number greater 1:
    loopwhile number less 100:
        display("Number is:", number)
        number = number * 2''',

    "Handling Flags": '''is_raining = no

check is_raining equals yes:
    display("Take an umbrella.")
otherwise:
    display("Enjoy the sunshine!")''',

    "Using Built-in Functions": '''name = getinput("Enter your name: ")
display("Hello, " + name + "!")

numbers = [1, 2, 3, 4, 5]
size = length(numbers)
display("The array has", size, "elements.")

sum_of_numbers = total(numbers)
display("The sum is:", sum_of_numbers)''',

    "Apply and Select Functions": '''numbers = [1, 2, 3, 4, 5]

# Double each number
doubled = list(apply(anon x: x * 2, numbers))
display("Doubled numbers:", doubled)

# Select even numbers
evens = list(select(anon x: x % 2 equals 0, numbers))
display("Even numbers:", evens)''',

    "Class Example": '''blueprint Person:
    create __init__(self, name):
        self.name = name

    create greet(self):
        display("Hello, " + self.name)

person = Person("Alice")
person.greet()''',

    "Exception Handling": '''attempt:
    number = getinput("Enter a number: ")
    number = whole(number)
    result = 100 / number
    display("Result is:", result)
handle ZeroDivisionError as e:
    display("Cannot divide by zero.")
handle ValueError as e:
    display("Invalid input.")
afterall:
    display("Done.")''',
}


def display_customization_guide():
    st.write("""
    ## Introduction

    This guide provides step-by-step instructions on how to customize the Simpy language by changing keywords. If you wish to modify existing keywords or add new ones, follow the instructions below.

    ### Understanding the Keyword Mapping

    The `keyword_mapping` dictionary in the `simpy_app.py` script defines how Simpy keywords are translated into Python keywords. Each entry in the dictionary maps a Simpy keyword (using a regular expression) to its Python equivalent.

    **Example Entry:**

    ```python
    keyword_mapping = {
        r'\\banon\\b': 'lambda',
        # ... other mappings ...
    }
    ```

    ### Steps to Change a Keyword

    Suppose you want to change the Simpy keyword `anon` (which maps to Python's `lambda`) to `short_func`. Here's how you can do it:

    1. **Locate the `keyword_mapping` Dictionary**

       Open the `simpy_app.py` script and find the `keyword_mapping` dictionary.

    2. **Update the Mapping**

       - **Remove** the old mapping for `anon`:

         ```python
         # Remove or comment out the old mapping
         # r'\\banon\\b': 'lambda',
         ```

       - **Add** the new mapping for `short_func`:

         ```python
         r'\\bshort_func\\b': 'lambda',
         ```

       - The updated `keyword_mapping` should include:

         ```python
         keyword_mapping = {
             # ... other mappings ...
             r'\\bshort_func\\b': 'lambda',
             # ... other mappings ...
         }
         ```

    3. **Update the Keyword Descriptions**

       If you have a `keyword_descriptions` dictionary used for explanations, update it accordingly.

       - **Remove** or **update** the old description:

         ```python
         # Remove or update the old description
         # 'anon': 'Defines an anonymous function (lambda)',
         ```

       - **Add** the new description:

         ```python
         'short_func': 'Defines an anonymous function (lambda)',
         ```

       - The updated `keyword_descriptions` should include:

         ```python
         keyword_descriptions = {
             # ... other descriptions ...
             'short_func': 'Defines an anonymous function (lambda)',
             # ... other descriptions ...
         }
         ```

    4. **Update Sample Programs (If Necessary)**

       Search through the `sample_programs` dictionary to find any instances of `anon` and replace them with `short_func`.

       - **Example:**

         ```python
         "Apply and Select Functions": '''numbers = [1, 2, 3, 4, 5]

         # Double each number
         doubled = list(apply(short_func x: x * 2, numbers))
         display("Doubled numbers:", doubled)

         # Select even numbers
         evens = list(select(short_func x: x % 2 equals 0, numbers))
         display("Even numbers:", evens)''',
         ```

    5. **Test the Changes**

       - **Run the App**:

         ```bash
         streamlit run simpy_app.py
         ```

       - **Test the Translation**:

         - Go to the **"Translation Process"** page.
         - Enter code using `short_func` instead of `anon`.
         - Click **"Translate Code"** and verify that `short_func` is correctly translated to `lambda`.

       - **Test Sample Programs**:

         - In the **"Simpy IDE"**, select the updated sample programs.
         - Run the code to ensure it executes without errors.

    ### Additional Tips

    - **Regular Expressions**:

      - The keys in `keyword_mapping` are regular expressions. The `\\b` denotes a word boundary to ensure only whole words are matched.
      - When adding new keywords, make sure to include `\\b` at the beginning and end if you want to match whole words.

    - **Order of Mappings**:

      - The order of mappings can affect replacements. Longer keywords should be replaced before shorter ones to prevent partial matches.
      - The translation function sorts keywords by length in descending order to handle this.

    - **Consistent Naming**:

      - Keep the naming consistent across `keyword_mapping`, `keyword_descriptions`, and `sample_programs`.

    - **Updating Documentation**:

      - If you have a **"Language Documentation"** page, remember to update it with the new keyword and its mapping.

    ### Example

    **Before Change:**

    Simpy code using `anon`:

    ```plaintext
    doubled = list(apply(anon x: x * 2, numbers))
    ```

    **After Change:**

    Simpy code using `short_func`:

    ```plaintext
    doubled = list(apply(short_func x: x * 2, numbers))
    ```

    **Translation:**

    - The code will now correctly translate `short_func` to `lambda`.

    ### Conclusion

    By following these steps, you can customize the Simpy language to suit your preferences or requirements. Always ensure you test your changes thoroughly to avoid any unexpected behavior.

    If you have any questions or need assistance, feel free to reach out!

    """)

# Main function to run the Streamlit app
def main():
    st.title("Simpy Compiler and IDE")

    # Sidebar for navigation
    page = st.sidebar.selectbox("Navigation", ["Simpy IDE", "Translation Process", "Tokenization Process", "Language Documentation", "Language Customization Guide"])

    if page == "Simpy IDE":
        st.header("Simpy IDE")

        # Dropdown for sample programs
        sample_choice = st.selectbox("Choose a sample program:", ["(Select a sample)"] + list(sample_programs.keys()))

        if sample_choice != "(Select a sample)":
            code_input = sample_programs[sample_choice]
        else:
            code_input = ""

        # Code input area
        code_input = st.text_area("Write your Simpy code here:", value=code_input, height=300)

        # Run code button
        if st.button("Run Code"):
            # Translate the Simpy code to Python code
            python_code = translate_simpy_to_python(code_input)

            # Capture the output of the executed code
            old_stdout = sys.stdout
            redirected_output = sys.stdout = io.StringIO()

            try:
                # Execute the Python code
                exec(python_code, {})
                # Get the output
                output = redirected_output.getvalue()
                # Display the output
                st.subheader("Output")
                st.code(output)
            except Exception as e:
                # Display the error message
                st.subheader("Error")
                st.error(e)
            finally:
                # Reset stdout
                sys.stdout = old_stdout

    elif page == "Language Documentation":
        st.header("Simpy Language Documentation")

        st.write("Simpy is a Python-like language with alternative keywords.")
        st.write("Below are the mappings and regular expressions used for translation.")

        st.subheader("Keyword Mappings and Regular Expressions")

        # Display the mappings in a table
        for simpy_regex, python_keyword in keyword_mapping.items():
            simpy_keyword = simpy_regex.strip(r'\b').replace(r'\s+', ' ')
            st.markdown(f"- **Simpy Keyword**: `{simpy_keyword}` ➔ **Python Equivalent**: `{python_keyword}`")
            st.markdown(f"  - **Regex**: `{simpy_regex}`")
    
    elif page == "Tokenization Process":
        st.header("Simpy Tokenization Process")
        
        # Dropdown for sample programs
        sample_choice = st.selectbox("Choose a sample program:", ["(Write your own)"] + list(sample_programs.keys()))
        
        if sample_choice != "(Write your own)":
            code_input = sample_programs[sample_choice]
        else:
            code_input = ""
        
        # Code input area
        code_input = st.text_area("Enter Simpy code to tokenize:", value=code_input, height=300)
        
        if st.button("Tokenize Code"):
            try:
                tokens = tokenize_simpy_code(code_input)
                st.subheader("Tokens")
                # Display tokens in a table
                token_df = [{"Token Type": kind, "Value": value} for kind, value in tokens]
                st.table(token_df)
            except Exception as e:
                st.subheader("Error")
                st.error(e)

    elif page == "Translation Process":
        st.header("Simpy Translation Process")
        
        # Dropdown for sample programs
        sample_choice = st.selectbox("Choose a sample program:", ["(Write your own)"] + list(sample_programs.keys()))
        
        if sample_choice != "(Write your own)":
            code_input = sample_programs[sample_choice]
        else:
            code_input = ""
        
        # Code input area
        code_input = st.text_area("Enter Simpy code to translate:", value=code_input, height=300)
        
        if st.button("Translate Code"):
            try:
                python_code, explanations = translate_simpy_to_python_with_explanation(code_input)
                
                st.subheader("Translated Python Code")
                st.code(python_code, language='python')
                
                st.subheader("Step-by-Step Explanation")
                for explanation in explanations:
                    st.write("- " + explanation)
            except Exception as e:
                st.subheader("Error")
                st.error(e)
                
    elif page == "Language Customization Guide":
        st.header("Language Customization Guide")
        display_customization_guide()


if __name__ == "__main__":
    main()