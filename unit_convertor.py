import streamlit as st
from forex_python.converter import CurrencyRates  # type: ignore

# Streamlit UI settings
st.set_page_config(page_title="Unit Converter", layout="centered")
st.title("🌍 Advanced Unit Converter")

# Dark Mode Toggle
dark_mode = st.sidebar.checkbox("🌙 Enable Dark Mode")
if dark_mode:
    st.markdown(
        """
        <style>
            body { background-color: #1e1e1e; color: white; }
            .stTextInput, .stNumberInput, .stSelectbox { background-color: #2e2e2e; color: white; }
        </style>
        """,
        unsafe_allow_html=True
    )

# Sidebar Navigation
st.sidebar.header("Select Conversion Type")
conversion_type = st.sidebar.selectbox("Choose a category", [
    "Length", "Weight", "Temperature", "Time", "Speed", "Currency"
])

# History Storage
if "history" not in st.session_state:
    st.session_state.history = []

# Conversion Functions
def convert_length(value, from_unit, to_unit):
    units = {"Meter": 1, "Kilometer": 1000, "Mile": 1609.34, "Inch": 0.0254}
    return value * (units[to_unit] / units[from_unit])

def convert_weight(value, from_unit, to_unit):
    units = {"Gram": 1, "Kilogram": 1000, "Pound": 453.592}
    return value * (units[to_unit] / units[from_unit])

def convert_temperature(value, from_unit, to_unit):
    if from_unit == "Celsius" and to_unit == "Fahrenheit":
        return (value * 9/5) + 32
    elif from_unit == "Fahrenheit" and to_unit == "Celsius":
        return (value - 32) * 5/9
    elif from_unit == "Celsius" and to_unit == "Kelvin":
        return value + 273.15
    elif from_unit == "Kelvin" and to_unit == "Celsius":
        return value - 273.15
    return value

def convert_time(value, from_unit, to_unit):
    units = {"Seconds": 1, "Minutes": 60, "Hours": 3600}
    return value * (units[to_unit] / units[from_unit])

def convert_speed(value, from_unit, to_unit):
    units = {"m/s": 1, "km/h": 3.6, "mph": 2.237}
    return value * (units[to_unit] / units[from_unit])

def convert_currency(value, from_currency, to_currency):
    try:
        c = CurrencyRates()
        return c.convert(from_currency, to_currency, value)
    except Exception as e:
        return None, str(e)

# Auto Conversion
if conversion_type == "Length":
    from_unit = st.selectbox("From Unit", ["Meter", "Kilometer", "Mile", "Inch"], key="from_length")
    to_unit = st.selectbox("To Unit", ["Meter", "Kilometer", "Mile", "Inch"], key="to_length")
    value = st.number_input("Enter Value", min_value=0.0, key="length_value")
    result = convert_length(value, from_unit, to_unit)
    st.success(f"{value} {from_unit} = {result:.2f} {to_unit}")

elif conversion_type == "Weight":
    from_unit = st.selectbox("From Unit", ["Gram", "Kilogram", "Pound"], key="from_weight")
    to_unit = st.selectbox("To Unit", ["Gram", "Kilogram", "Pound"], key="to_weight")
    value = st.number_input("Enter Value", min_value=0.0, key="weight_value")
    result = convert_weight(value, from_unit, to_unit)
    st.success(f"{value} {from_unit} = {result:.2f} {to_unit}")

elif conversion_type == "Temperature":
    from_unit = st.selectbox("From Unit", ["Celsius", "Fahrenheit", "Kelvin"], key="from_temp")
    to_unit = st.selectbox("To Unit", ["Celsius", "Fahrenheit", "Kelvin"], key="to_temp")
    value = st.number_input("Enter Value", key="temp_value")
    result = convert_temperature(value, from_unit, to_unit)
    st.success(f"{value}° {from_unit} = {result:.2f}° {to_unit}")

elif conversion_type == "Time":
    from_unit = st.selectbox("From Unit", ["Seconds", "Minutes", "Hours"], key="from_time")
    to_unit = st.selectbox("To Unit", ["Seconds", "Minutes", "Hours"], key="to_time")
    value = st.number_input("Enter Value", min_value=0.0, key="time_value")
    result = convert_time(value, from_unit, to_unit)
    st.success(f"{value} {from_unit} = {result:.2f} {to_unit}")

elif conversion_type == "Speed":
    from_unit = st.selectbox("From Unit", ["m/s", "km/h", "mph"], key="from_speed")
    to_unit = st.selectbox("To Unit", ["m/s", "km/h", "mph"], key="to_speed")
    value = st.number_input("Enter Value", min_value=0.0, key="speed_value")
    result = convert_speed(value, from_unit, to_unit)
    st.success(f"{value} {from_unit} = {result:.2f} {to_unit}")

elif conversion_type == "Currency":
    from_currency = st.text_input("From Currency (e.g., USD, EUR, INR)", key="from_currency").upper()
    to_currency = st.text_input("To Currency (e.g., USD, EUR, INR)", key="to_currency").upper()
    value = st.number_input("Enter Amount", min_value=0.0, key="currency_value")
    if from_currency and to_currency and value:
        result, error_message = convert_currency(value, from_currency, to_currency)
        if result:
            st.success(f"{value} {from_currency} = {result:.2f} {to_currency}")
        else:
            st.error(f"Invalid currency code or API error: {error_message}")

# Display Conversion History
if st.sidebar.button("Show History"):
    st.sidebar.write("### Conversion History")
    for item in st.session_state.history[-10:]:
        st.sidebar.write(item)

st.sidebar.info("Built with ❤️ by Vandana using Streamlit with AI-powered enhancements")
