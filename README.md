# BigMacIndexVisualization
This repository contains the code for end-to-end deployment of BigMac Index using AWS and streamlit.
I deployed the dashboard to [the streamlit cloud](https://htng18-bigmacindexvisualization-dataapp-k6iusd.streamlit.app/).
This can be used via a brower.

This deployement can be done in the following:
1. Download the source data from a URL using AWS Lambda function.
2. AWS Lambda function saved the data into AWS S3.
3. AWS Glue obtained the data from S3 and calculated the following quantities:
* BigMac Index.
* Actual exchange rate (USD).
* Evaluation between BigMac Index and the actual exchange rate.
4. The processed data is stored in S3
4. Deploy the app using streamlit, where the app can get the data from S3. 


