# BigMacIndexVisualization
This repository contains the code for end-to-end deployment of BigMac Index using AWS and streamlit.
I deployed the dashboard to [the streamlit cloud](https://htng18-bigmacindexvisualization-dataapp-k6iusd.streamlit.app/).
This can be used via a brower. The solution architecture of this deployment is provided as follows:
![image](https://user-images.githubusercontent.com/35870518/219971111-48eba275-b150-4be0-98b8-2c9f8bb8693a.png)

This procedure of this deployment is outlined:
1. Download the source data from a URL using AWS Lambda function.
2. AWS Lambda function saved the data into AWS S3.
3. AWS Glue obtained the data from S3 and calculated the following quantities:
  * BigMac Index.
  * Actual exchange rate (USD).
  * Evaluation between BigMac Index and the actual exchange rate.
4. The processed data is then stored in S3
4. Deploy the app using streamlit, where the app can get the data from S3. 


