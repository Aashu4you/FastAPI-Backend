import streamlit as st
import requests

# Page configuration
st.set_page_config(
    page_title="Insurance Premium Predictor",
    page_icon="🏥",
    layout="centered"
)

st.title("🏥 Insurance Premium Predictor")
st.write("Enter your details to predict your insurance premium category.")

st.divider()

# User input form
with st.form("prediction_form"):

    st.subheader("Personal Information")

    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input(
            "Age",
            min_value=1,
            max_value=149,
            value=25
        )

        weight = st.number_input(
            "Weight (kg)",
            min_value=0.1,
            value=65.0
        )

        height = st.number_input(
            "Height (meters)",
            min_value=0.1,
            max_value=2.49,
            value=1.70
        )

    with col2:
        income_lpa = st.number_input(
            "Annual Income (LPA)",
            min_value=0.1,
            value=5.0
        )

        smoker = st.selectbox(
            "Are you a smoker?",
            ["No", "Yes"]
        )

        city = st.text_input(
            "City",
            placeholder="e.g. Bhopal"
        )

    occupation = st.selectbox(
        "Occupation",
        [
            "retired",
            "freelancer",
            "student",
            "government_job",
            "business_owner",
            "unemployed",
            "private_job"
        ]
    )

    submitted = st.form_submit_button(
        "Predict Insurance Premium",
        use_container_width=True
    )


# API request
if submitted:

    if not city.strip():
        st.error("Please enter your city.")

    else:

        input_data = {
            "age": age,
            "weight": weight,
            "height": height,
            "income_lpa": income_lpa,
            "smoker": smoker == "Yes",
            "city": city.strip(),
            "occupation": occupation
        }

        API_URL = "http://127.0.0.1:8000/predict"

        try:

            with st.spinner("Predicting your insurance premium..."):

                response = requests.post(
                    API_URL,
                    json=input_data,
                    timeout=30
                )

                response.raise_for_status()

                result = response.json()
                

            prediction_data = result["Predicted_category "]

            prediction = prediction_data["predicted_category"]
            confidence = prediction_data["confidence"]
            class_probabilities = prediction_data["class_probabilities"]

            st.divider()

            st.success("Prediction completed successfully!")

            # Display predicted category
            st.subheader("Your Prediction")

            st.metric(
                label="Predicted Insurance Category",
                value=prediction
            )

            # Display confidence
            st.subheader("Model Confidence")

            st.metric(
                label="Confidence Score",
                value=f"{confidence * 100:.2f}%"
            )

            st.progress(
                max(0.0, min(float(confidence), 1.0))
            )

            # Display class probabilities
            st.subheader("Probability Distribution")

            st.write(
                "Here's how the model distributes probabilities "
                "across the available insurance categories."
            )

            st.bar_chart(
                {
                    "Probability (%)": {
                        category: probability * 100
                        for category, probability
                        in class_probabilities.items()
                    }
                }
            )

            # Detailed probability values
            st.subheader("Detailed Probabilities")

            for category, probability in class_probabilities.items():

                st.write(
                    f"**{category}:** {probability * 100:.2f}%"
                )

        except requests.exceptions.ConnectionError:
            st.error(
                "Could not connect to FastAPI. "
                "Please make sure your backend is running."
            )

        except requests.exceptions.Timeout:
            st.error("The prediction request timed out. Please try again.")

        except requests.exceptions.HTTPError:
            st.error(f"API Error: {response.text}")

        except (KeyError, TypeError, ValueError) as e:
            st.error(f"Unexpected API response format: {e}")

        except Exception as e:
            st.error(f"Something went wrong: {e}")
