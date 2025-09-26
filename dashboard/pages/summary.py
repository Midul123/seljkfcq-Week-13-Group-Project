import streamlit as st
from get_all_data import get_all_data
from charts import avg_moisture, create_line_chart_temp
from graphs import summary_data
from tables import chosen_plants, selected_plants_name, selected_plants_soil, selected_plants_temp

if __name__ == "__main__":
    st.set_page_config(layout="wide")
    st.title("Daily Summary Dashboard")

    data = get_all_data()

    # Create two columns for filters
    filter_col1, filter_col2 = st.columns(2)

    with filter_col1:
        available_months = sorted(data['month'].unique())
        selected_month = st.selectbox("Select Month", available_months)

    # Filter by selected month
    filtered_data = data[data['month'] == selected_month]

    with filter_col2:
        available_days = sorted([int(day)
                                for day in filtered_data['day'].unique()])
        if len(available_days) > 1:
            selected_day_range = st.select_slider(
                "Select Day Range",
                options=available_days,
                value=(available_days[0], available_days[-1])
            )
        else:
            selected_day_range = (available_days[0], available_days[0])
            st.info(f"Only one day available: {available_days[0]}")

    # Filter by day range
    filtered_data = filtered_data[
        (filtered_data['day'].astype(int) >= selected_day_range[0]) &
        (filtered_data['day'].astype(int) <= selected_day_range[1])
    ]

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Temperature")
        st.altair_chart(create_line_chart_temp(
            filtered_data).interactive(), use_container_width=True)

    with col2:
        st.subheader("Moisture")
        st.altair_chart(avg_moisture(
            filtered_data).interactive(), use_container_width=True)

    data = summary_data()

    st.subheader("Summarised Plant data")
    chosen = chosen_plants(data, "Plant Selector")
    if len(chosen) > 0:
        new_df = selected_plants_name(data, chosen)
        temp = temp_threshold = st.number_input(
            "Enter a minimum temperature to filter by (°C):", min_value=0, max_value=100)
        soil = st.number_input(
            "Enter a minimum soil moisture to filter by (mm):")
        if temp:
            new_df = selected_plants_temp(new_df, temp)
        if soil:
            new_df = selected_plants_soil(new_df, soil)

        st.dataframe(new_df)
    else:
        st.write('Choose at least one plant')
