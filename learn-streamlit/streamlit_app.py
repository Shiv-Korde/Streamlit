import streamlit as st
from asammdf import MDF
import pandas as pd
import numpy as np

st.title("📁 MF4 File Viewer and Signal Plotter")

# File uploader
with st.container(border=True):
    uploaded_file = st.file_uploader("Upload an .mf4 file", type=["mf4"])
    if uploaded_file:
        mdf = MDF(uploaded_file)
        st.success("MF4 file loaded successfully!")

        # Show general info
        with st.expander("📄 File Info"):
            st.write(f"Number of Channels: {len(mdf.channels_db)}")
            st.write(f"Duration: {mdf.duration:.2f} seconds")
            st.write(f"Time Range: {mdf.timestamps[0]:.2f}s to {mdf.timestamps[-1]:.2f}s")

        # Signal selection
        all_signals = list(mdf.channels_db.keys())
        selected_signals = st.multiselect("Select signals to plot", all_signals, max_selections=5)

        if selected_signals:
            rolling_average = st.toggle("Rolling average")
            signal_data = {}
            for signal in selected_signals:
                ts, values = mdf.get(signal).samples()
                df = pd.DataFrame({signal: values}, index=ts)
                if rolling_average:
                    df = df.rolling(100).mean().dropna()
                signal_data[signal] = df

            combined_df = pd.concat(signal_data.values(), axis=1)

            tab1, tab2 = st.tabs(["Chart", "Dataframe"])
            with tab1:
                st.line_chart(combined_df, height=300)
            with tab2:
                st.dataframe(combined_df.reset_index(), height=300, use_container_width=True)
    else:
        st.info("Please upload a valid .mf4 file to continue.")
