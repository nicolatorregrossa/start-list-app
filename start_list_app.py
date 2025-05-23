import streamlit as st
import pandas as pd

st.set_page_config(page_title="Start List Generator", layout="wide")

# Initialize session state
if 'data_a' not in st.session_state:
    st.session_state['data_a'] = pd.DataFrame(columns=[
        'Heat Number', 'Lane Number', 'Athlete Name', 'Class & Section', 'School Name'
    ])

if 'data_b' not in st.session_state:
    st.session_state['data_b'] = pd.DataFrame(columns=[
        'Heat Number', 'Lane Number', 'Race Time'
    ])

# Sidebar navigation
page = st.sidebar.selectbox("Select Page", ["🏃 Athlete Entry", "⏱️ Race Times Entry", "📊 Start List"])

# ---------------------- PAGE 1: Athlete Entry ----------------------
if page == "🏃 Athlete Entry":
    st.title("🏃 Athlete Entry – Data Source A")
    st.markdown("Enter athlete details below:")

    with st.form("athlete_form", clear_on_submit=True):
        heat = st.number_input("Heat Number", min_value=1, step=1)
        lane = st.number_input("Lane Number", min_value=1, step=1)
        name = st.text_input("Athlete Name")
        class_sec = st.text_input("Class & Section (e.g., 2B)")
        school = st.text_input("School Name (optional)")

        submitted = st.form_submit_button("Add Athlete")
        if submitted:
            if name and class_sec:
                new_row = {
                    'Heat Number': heat,
                    'Lane Number': lane,
                    'Athlete Name': name,
                    'Class & Section': class_sec,
                    'School Name': school
                }
st.session_state['data_a'] = pd.concat(
    [st.session_state['data_a'], pd.DataFrame([new_row])],
    ignore_index=True
)
                st.success("Athlete added.")
            else:
                st.error("Please fill in all required fields.")

    st.subheader("Current Athlete Table")
    st.dataframe(st.session_state['data_a'])

    if st.download_button("Download as CSV", st.session_state['data_a'].to_csv(index=False), "athletes.csv"):
        st.success("Download started.")

# ---------------------- PAGE 2: Race Times Entry ----------------------
elif page == "⏱️ Race Times Entry":
    st.title("⏱️ Race Times Entry – Data Source B")
    st.markdown("Enter race results below:")

    with st.form("race_form", clear_on_submit=True):
        heat = st.number_input("Heat Number", min_value=1, step=1, key="heat_b")
        lane = st.number_input("Lane Number", min_value=1, step=1, key="lane_b")
        time = st.text_input("Race Time (e.g., 12.45)", key="time_b")

        submitted = st.form_submit_button("Add Time")
        if submitted:
            if time:
                new_row = {
                    'Heat Number': heat,
                    'Lane Number': lane,
                    'Race Time': time
                }
                st.session_state['data_b'] = st.session_state['data_b'].append(new_row, ignore_index=True)
                st.success("Race time added.")
            else:
                st.error("Please enter a valid time.")

    st.subheader("Current Time Table")
    st.dataframe(st.session_state['data_b'])

    if st.download_button("Download as CSV", st.session_state['data_b'].to_csv(index=False), "times.csv"):
        st.success("Download started.")

# ---------------------- PAGE 3: Start List View ----------------------
elif page == "📊 Start List":
    st.title("📊 Start List / Results View")

    df_merged = pd.merge(
        st.session_state['data_a'],
        st.session_state['data_b'],
        on=["Heat Number", "Lane Number"],
        how="left"
    )

    if df_merged.empty:
        st.warning("No data to display. Please add data in the previous pages.")
    else:
        heat_groups = df_merged.groupby("Heat Number")

        for heat, group in heat_groups:
            st.subheader(f"Heat {int(heat)}")
            try:
                group['Race Time (sec)'] = group['Race Time'].astype(float)
                group_sorted = group.sort_values("Race Time (sec)")
            except:
                group_sorted = group

            st.dataframe(group_sorted[[
                "Athlete Name", "Class & Section", "Lane Number", "Race Time"
            ]])

        if st.download_button("Download Full Start List", df_merged.to_csv(index=False), "start_list.csv"):
            st.success("Start list exported.")
