import streamlit as st
from get_response_func import get_response_url, get_response_single_prompt
import ast
import pandas as pd
from text_extractor import WebpageTextExtractor

st.header("AI-BOARDING :scream_cat: :100:")

st.radio(
    "",
    ["Get response by URL", "Try it yourself"],
    key="mode",
    label_visibility='hidden',
    horizontal=True,
)

if st.session_state.mode == "Get response by URL":

    st.markdown("Use this tool to collect information about the merchant as part of the onboarding research. "
             "Just fill in the merchant's website and click go! \n")
    st.markdown("Note: The information reliability must be verified (AI can get creative)")
    st.markdown("**Your feedback is appreciated!** At the bottom you will find a CSV template, download it and fill in the following: \n")
    st.markdown("like_or_dislike \n")
    st.markdown("comments: comments you have about the tool outputs \n")
    st.markdown("suggestion: suggestions for prompt improvement")
    st.markdown("Upload the CSV file to: https://drive.google.com/drive/folders/17TlhsWgsRqcForpTxrxosWLGd5BrZRF1?usp=drive_link")

    st.text_input("URL", key="URL")
    st.text_input("Terms URL", key="terms_url")

    # access the value
    url = st.session_state.URL
    terms_url = st.session_state.terms_url

    st.markdown(
        """
        <style>
        div.stButton > button:first-child {
            width: 300px;
            height: 50px;
            font-size: 40px;
            display: flex;
            margin: auto;
            background-color: #2E8B57;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    if st.button('GO!'):
        extractor = WebpageTextExtractor(terms_url)
        extracted_text = extractor.extract_text()

        responses, questions = get_response_url(url, extracted_text)

        st.subheader(f"**URL:** {url}")
        print("------responses: ", responses)
        merchant_name = responses[0]["company"]
        description = responses[1]["description"]
        industry = responses[2]["industry"]
        channels = responses[3]["channels"]
        billings = responses[4]["billings"]
        email_address = responses[5]["emailAddress"]
        customer_support = responses[6]["customer_support"]
        cancellation = responses[6]["cancellation"]
        refund_policy = responses[6]["refund_policy"]
        delivery_methods = responses[7]["delivery_methods"]
        liability = responses[7]["liability"]
        if len(responses) == 9:
            crypto_transfers = responses[8]["crypto_transfers"]
        else:
            crypto_transfers = None

        st.subheader("Merchant name")
        st.write(merchant_name)

        st.subheader("Merchant description")
        st.write(description)

        st.subheader("Industry")
        st.write(industry)

        st.subheader("channels")
        st.write(channels)

        st.subheader("billings")
        st.write(billings)

        st.subheader("email_address")
        st.write(email_address)

        st.subheader("customer_support")
        if customer_support != "NULL":
            st.write(f"**timeframe:** {customer_support['timeframe']}")
            st.write(f"**summary:** {customer_support['summary']}")
            st.write(f"**quote:** {customer_support['quote']}")
            st.write(f"**specificConditions:** {customer_support['specificConditions']}")
            st.write(f"**source:** {customer_support['source']}")
        else:
            st.write(f"Information not found")


        st.subheader("cancellation")
        if customer_support != "NULL":
            st.write(f"**timeframe:** {cancellation['timeframe']}")
            st.write(f"**summary:** {cancellation['summary']}")
            st.write(f"**quote:** {cancellation['quote']}")
            st.write(f"**specificConditions:** {cancellation['specificConditions']}")
            st.write(f"**source:** {cancellation['source']}")
        else:
            st.write(f"Information not found")

        st.subheader("refund_policy")
        if customer_support != "NULL":
            st.write(refund_policy)
        else:
            st.write(f"Information not found")

        st.subheader("delivery_methods")
        st.write(delivery_methods)

        st.subheader("liability")
        st.write(liability)

        if crypto_transfers is not None:
            st.subheader("crypto_transfers")
            st.write(crypto_transfers)

        st.divider()
        df = pd.DataFrame({"prompt": pd.Series(questions),
                           "response": pd.Series(responses),
                           "like_or_dislike": None,
                           "comments": None,
                           "suggestion": None})


        st.download_button(
            "Download as a CSV",
            df.to_csv(index=False).encode('utf-8'),
            "file.csv",
            "text/csv",
            key='download-csv'
        )
        st.dataframe(df)

        # st.divider()
        #
        #
        # for i in range(len(questions)):
        #     st.divider()
        #     st.write(f"**Prompt**")
        #     st.write(f"{questions[i]}")
        #     st.write(f"**response**")
        #     st.write(f"{responses[i]}")

if st.session_state.mode == "Try it yourself":
    st.write(f"We welcome new prompt suggestions :blush:, feel free to post them here: https://drive.google.com/drive/folders/1kv4nwb49IhfOl6-SHu-sBZjCH7mtLs3A?usp=drive_link")
    st.text_input("Prompt", key="prompt")
    st.markdown(
            """
            <style>
            div.stButton > button:first-child {
                width: 300px;
                height: 50px;
                font-size: 40px;
                display: flex;
                margin: auto;
                background-color: #2E8B57;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
    if st.button('Try it yourself!'):
        single_response = get_response_single_prompt(st.session_state.prompt)
        st.write(f"**prompt**")
        st.write(st.session_state.prompt)
        st.write(f"**response**")
        st.write(single_response)