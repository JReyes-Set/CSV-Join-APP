# Import required libraries
import streamlit as st
import pandas as pd
from io import StringIO

# Set up the Streamlit app layout and title
st.set_page_config(page_title="CSV File Joiner", layout="wide")
st.title("🔗 CSV File Joiner")

# Brief description of what the app does
st.write("Upload two CSV files and choose how to join them using inner, left, right, or outer joins. "
         "You can also remove duplicate rows before merging.")

# -----------------------------------------
# STEP 1: Upload both CSV files
# Users will be prompted to upload File 1 and File 2
# -----------------------------------------

uploaded_file1 = st.file_uploader("📁 Upload File 1", type=["csv"])
uploaded_file2 = st.file_uploader("📁 Upload File 2", type=["csv"])

# Proceed only if both files are uploaded
if uploaded_file1 and uploaded_file2:
    # Read both uploaded files into DataFrames
    df1 = pd.read_csv(uploaded_file1)
    df2 = pd.read_csv(uploaded_file2)

    st.subheader("⚙️ Join Configuration")

    # -----------------------------------------
    # STEP 2: Join settings UI
    # Let user pick:
    # - Column from each file
    # - Join type
    # - Whether to remove duplicates
    # -----------------------------------------

    col1 = st.selectbox("Select join column from File 1", df1.columns)
    col2 = st.selectbox("Select join column from File 2", df2.columns)
    join_type = st.selectbox("Select Join Type", ["inner", "left", "right", "outer"])
    remove_duplicates = st.checkbox("✅ Remove duplicate rows before joining", value=True)

    # -----------------------------------------
    # STEP 3: Perform the join when button is clicked
    # - Join the two DataFrames
    # - Show preview
    # - Provide download button
    # -----------------------------------------

    if st.button("🔗 Perform Join"):
        try:
            # Optional: remove duplicates before merging
            if remove_duplicates:
                df1 = df1.drop_duplicates()
                df2 = df2.drop_duplicates()

            # Perform the join using pandas
            result = pd.merge(
                df1, df2,
                how=join_type,
                left_on=col1,
                right_on=col2,
                suffixes=("", "_file2")
            )

            # Show success message and preview the joined data
            st.success(f"✅ Join successful! {len(result)} rows returned.")
            st.dataframe(result.head(50), use_container_width=True)

            # -----------------------------------------
            # STEP 4: Enable download of the joined CSV
            # -----------------------------------------
            csv = result.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="💾 Download Joined CSV",
                data=csv,
                file_name='joined_result.csv',
                mime='text/csv'
            )

        except Exception as e:
            st.error(f"❌ Error during join: {e}")

# Optional footer
st.markdown("---")
st.caption("Built with ❤️ using Streamlit. Developed by Joseph Reyes.")
