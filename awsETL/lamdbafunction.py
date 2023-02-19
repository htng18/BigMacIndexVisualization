import json
import requests
import boto3

def lambda_handler(event, context):
    ''' 
        This lambda function is to download the data
        from economist BigMac Index github and save
        it into ASW S3. Then, it calls the job from
        AWS Glue for further data processing. 
    
    '''
    bucketName = 'bigmacindexdata2023'
    fileName = 'bigmacindex_source.csv'
    r = requests.get('https://raw.githubusercontent.com/TheEconomist/big-mac-data/master/source-data/big-mac-source-data-v2.csv')
    url_content = r.content
    with open('/tmp/download.csv', 'wb') as f:
        f.write(url_content)
    s3 = boto3.client('s3')
    s3.upload_file('/tmp/download.csv', bucketName, fileName)
    glue = boto3.client('glue')

    response = glue.start_job_run(
        JobName = 'BigMacIndex',
        Arguments = {
            '--s3_target_path_key': fileName,
            '--s3_target_path_bucket': bucketName}
    )
        
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
