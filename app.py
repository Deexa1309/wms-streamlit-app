import streamlit as st
import pandas as pd
import altair as alt
from io import StringIO
from pandasai import SmartDataframe
from pandasai.llm import OpenAI

st.set_page_config(page_title="📦 WMS Mapper", layout="wide")
st.title("📦 Warehouse Management System – SKU to MSKU Mapper")

st.markdown("Upload your **mapping file** and one or more **sales CSVs** to map SKUs to MSKUs.")

# Upload mapping file
mapping_file = st.file_uploader("📘 Upload SKU → MSKU Mapping File (.csv)", type=["csv"])

# Upload sales files
sales_files = st.file_uploader("📥 Upload Sales Data Files (.csv)", type=["csv"], accept_multiple_files=True)

if mapping_file and sales_files:
    try:
        mapping_df = pd.read_csv(mapping_file)
        if not {"SKU", "MSKU"}.issubset(mapping_df.columns):
            st.error("❌ Mapping file must contain 'SKU' and 'MSKU' columns.")
        else:
            mapping_dict = dict(zip(mapping_df['SKU'], mapping_df['MSKU']))
            combined_df = pd.DataFrame()

            for file in sales_files:
                df = pd.read_csv(file)
                if "SKU" not in df.columns:
                    st.warning(f"⚠️ File {file.name} skipped: No 'SKU' column found.")
                    continue
                df["MSKU"] = df["SKU"].map(mapping_dict).fillna("UNKNOWN")
                combined_df = pd.concat([combined_df, df], ignore_index=True)

            st.success("✅ Mapping Completed")
            st.write(combined_df.head())

            # Download button
            csv_data = combined_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Download Mapped CSV",
                data=csv_data,
                file_name="mapped_sales.csv",
                mime="text/csv"
            )

            # Optional Chart
            if "Quantity" in combined_df.columns:
                st.subheader("📊 MSKU Quantity Distribution")
                chart = alt.Chart(combined_df).mark_bar().encode(
                    x=alt.X("MSKU", sort='-y'),
                    y="Quantity"
                ).properties(width=700)
                st.altair_chart(chart, use_container_width=True)

            # Optional: Ask your data with OpenAI
            with st.expander("🤖 AI: Ask Your Data (Optional)"):
                api_key = st.text_input("Enter your OpenAI API key", type="password")
                query = st.text_input("What do you want to know?")
                if api_key and query:
                    llm = OpenAI(api_token=api_key)
                    smart_df = SmartDataframe(combined_df, config={"llm": llm})
                    response = smart_df.chat(query)
                    st.write(response)

    except Exception as e:
        st.error(f"❌ Error: {e}")
else:
    st.info("⬆️ Please upload a mapping file and at least one sales file.")
