import numpy as np
import pandas as pd
import streamlit as st

# Generate some data
np.random.seed(0)
df = pd.DataFrame(np.random.randn(20, 3), columns=['a', 'b', 'c'])

# Plot the data
st.line_chart(df)
