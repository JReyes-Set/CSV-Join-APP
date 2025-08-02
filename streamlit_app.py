import streamlit as st

st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)
# STEP 1: Install necessary packages (only needed once per session)
# - pandas: used for handling and merging the CSV data
# - ipywidgets: used for interactive dropdowns, checkboxes, buttons in Colab
!pip install -q pandas ipywidgets

# STEP 2: Import required Python libraries
import pandas as pd
import io
import ipywidgets as widgets
from IPython.display import display, clear_output
from google.colab import files

# STEP 3: Upload CSV files
# ✅ How to use: This block will prompt you to upload your two CSV files.
# - You must select the same column from each file later for the join.
# - Make sure both CSVs have headers (column names) in the first row.

print("📁 Upload File 1:")
upload1 = files.upload()  # Opens file picker for the first CSV
df1 = pd.read_csv(io.BytesIO(next(iter(upload1.values()))))  # Reads file into a DataFrame

print("📁 Upload File 2:")
upload2 = files.upload()  # Opens file picker for the second CSV
df2 = pd.read_csv(io.BytesIO(next(iter(upload2.values()))))  # Reads file into a DataFrame

# STEP 4: Create interactive controls for join options
# ✅ How to use: Select how you want to join the files.
# - Remove duplicates: Check this to remove exact duplicate rows before joining
# - Join type: Choose from 'inner', 'left', 'right', or 'outer' joins
# - File 1/2 Columns: Select the matching column from each file to use as join keys

remove_duplicates_checkbox = widgets.Checkbox(
    value=True, 
    description='Remove Duplicates'
)

join_type_dropdown = widgets.Dropdown(
    options=['inner', 'left', 'right', 'outer'],
    description='Join Type:'
)

col1_dropdown = widgets.Dropdown(
    options=df1.columns.tolist(), 
    description='File 1 Column:'
)

col2_dropdown = widgets.Dropdown(
    options=df2.columns.tolist(), 
    description='File 2 Column:'
)

run_button = widgets.Button(
    description='🔗 Perform Join', 
    button_style='success'
)

output = widgets.Output()  # Used to show the result and messages below the button

# STEP 5: Join logic and result preview
# ✅ What this code does:
# - When the "Perform Join" button is clicked:
#   1. It takes your selected options.
#   2. Drops duplicates if requested.
#   3. Joins the two files based on your column and type selection.
#   4. Previews the first 50 rows.
#   5. Lets you download the merged result as a new CSV file.

def perform_join(b):
    with output:
        clear_output()
        
        # Get user-selected column names and join type
        col1 = col1_dropdown.value
        col2 = col2_dropdown.value
        join_type = join_type_dropdown.value

        # Apply duplicate removal if checked
        df1_clean = df1.drop_duplicates() if remove_duplicates_checkbox.value else df1
        df2_clean = df2.drop_duplicates() if remove_duplicates_checkbox.value else df2

        try:
            # Perform the merge using pandas
            result = pd.merge(
                df1_clean, df2_clean,
                how=join_type,
                left_on=col1,
                right_on=col2,
                suffixes=('', '_file2')
            )
            
            print(f"✅ Join successful! {len(result)} rows returned.\n")
            display(result.head(50))  # Show a preview of the joined data
            
            # Save and prepare download
            result.to_csv('joined_result.csv', index=False)
            print("\n💾 Download your result:")
            files.download('joined_result.csv')

        except Exception as e:
            print(f"❌ Error: {e}")

# Attach join function to the button click event
run_button.on_click(perform_join)

# STEP 6: Display the full UI
# ✅ What you see here:
# - All the join settings
# - The preview table and download button after you click "Perform Join"

display(widgets.VBox([
    widgets.HTML("<h3>⚙️ Join Configuration</h3>"),
    remove_duplicates_checkbox,
    join_type_dropdown,
    col1_dropdown,
    col2_dropdown,
    run_button,
    output
]))
