import streamlit as st
import pandas as pd
from datetime import date
import os

st.title("🛒 Hyper-Local Inflation Tracker")

st.write(
    "Track grocery prices and predict your next month's budget."
)


# -----------------------------------
# CSV FILE
# -----------------------------------

FILE_NAME = "prices.csv"


# -----------------------------------
# LOAD EXISTING DATA
# -----------------------------------

if os.path.exists(FILE_NAME):

    price_data = pd.read_csv(FILE_NAME)

else:

    price_data = pd.DataFrame(
        columns=[
            "Date",
            "Item",
            "Price",
            "Quantity"
        ]
    )


# -----------------------------------
# PRICE ENTRY
# -----------------------------------

st.subheader("➕ Add Grocery Price")


entry_date = st.date_input(
    "Select date",
    value=date.today()
)


item = st.selectbox(
    "Select grocery item",
    ["Milk", "Eggs", "Rice"]
)


price = st.number_input(
    "Enter price (₹)",
    min_value=0.0,
    step=1.0
)


quantity = st.number_input(
    "Enter quantity",
    min_value=1.0,
    step=1.0
)


if st.button("Add Price"):

    new_data = pd.DataFrame(
        [{
            "Date": entry_date,
            "Item": item,
            "Price": price,
            "Quantity": quantity
        }]
    )

    price_data = pd.concat(
        [
            price_data,
            new_data
        ],
        ignore_index=True
    )

    price_data.to_csv(
        FILE_NAME,
        index=False
    )

    st.success(
        f"Added {item}: ₹{price} × {quantity}"
    )


# -----------------------------------
# CALCULATE TOTAL COST
# -----------------------------------

if not price_data.empty:

    price_data["Total Cost"] = (
        price_data["Price"]
        * price_data["Quantity"]
    )


# -----------------------------------
# PRICE HISTORY
# -----------------------------------

st.subheader("📋 Price History")

st.dataframe(
    price_data,
    use_container_width=True
)


# -----------------------------------
# PRICE TREND
# -----------------------------------

st.subheader("📈 Price Trend")


if not price_data.empty:

    selected_item = st.selectbox(
        "Select item to view trend",
        ["Milk", "Eggs", "Rice"]
    )

    chart_data = price_data[
        price_data["Item"] == selected_item
    ].copy()


    if not chart_data.empty:

        chart_data["Date"] = pd.to_datetime(
            chart_data["Date"]
        )

        chart_data = chart_data.sort_values(
            "Date"
        )

        chart_data = chart_data.set_index(
            "Date"
        )

        st.line_chart(
            chart_data["Price"]
        )

    else:

        st.info(
            f"No price data available for {selected_item}."
        )

else:

    st.info(
        "Add some grocery prices to see the trend."
    )


# -----------------------------------
# INFLATION CALCULATION
# -----------------------------------

st.subheader("📊 Inflation Summary")


if not price_data.empty:

    inflation_data = []


    for grocery in ["Milk", "Eggs", "Rice"]:

        item_data = price_data[
            price_data["Item"] == grocery
        ].copy()


        if len(item_data) >= 2:

            item_data["Date"] = pd.to_datetime(
                item_data["Date"]
            )

            item_data = item_data.sort_values(
                "Date"
            )


            old_price = item_data.iloc[0]["Price"]

            new_price = item_data.iloc[-1]["Price"]


            inflation = (
                (new_price - old_price)
                / old_price
            ) * 100


            inflation_data.append(
                {
                    "Item": grocery,
                    "Starting Price": old_price,
                    "Latest Price": new_price,
                    "Inflation (%)": round(
                        inflation,
                        2
                    )
                }
            )


    if inflation_data:

        inflation_df = pd.DataFrame(
            inflation_data
        )

        st.dataframe(
            inflation_df,
            use_container_width=True
        )

    else:

        st.info(
            "Add at least two prices for an item to calculate inflation."
        )

else:

    st.info(
        "Add some grocery prices first."
    )


# -----------------------------------
# CURRENT GROCERY BUDGET
# -----------------------------------

st.subheader("💰 Current Grocery Budget")


if not price_data.empty:

    total_budget = price_data[
        "Total Cost"
    ].sum()

    st.metric(
        "Total Recorded Grocery Cost",
        f"₹{total_budget:,.2f}"
    )

else:

    st.info(
        "Add grocery prices to calculate your budget."
    )


# -----------------------------------
# NEXT MONTH ESTIMATE
# -----------------------------------

st.subheader("🔮 Next Month Budget Estimate")


if not price_data.empty:

    monthly_data = []


    for grocery in ["Milk", "Eggs", "Rice"]:

        item_data = price_data[
            price_data["Item"] == grocery
        ].copy()


        if not item_data.empty:

            # Sort by date
            item_data["Date"] = pd.to_datetime(
                item_data["Date"]
            )

            item_data = item_data.sort_values(
                "Date"
            )


            # Get latest price
            latest_price = item_data.iloc[-1]["Price"]


            # Get latest quantity
            latest_quantity = item_data.iloc[-1]["Quantity"]


            # Estimated monthly cost
            monthly_cost = (
                latest_price
                * latest_quantity
            )


            monthly_data.append(
                {
                    "Item": grocery,
                    "Latest Price": latest_price,
                    "Quantity": latest_quantity,
                    "Estimated Monthly Cost": monthly_cost
                }
            )


    if monthly_data:

        monthly_df = pd.DataFrame(
            monthly_data
        )


        st.dataframe(
            monthly_df,
            use_container_width=True
        )


        estimated_budget = monthly_df[
            "Estimated Monthly Cost"
        ].sum()


        st.metric(
            "Estimated Next Month Budget",
            f"₹{estimated_budget:,.2f}"
        )

    else:

        st.info(
            "Add grocery prices to estimate next month's budget."
        )

else:

    st.info(
        "Add grocery prices first."
    )