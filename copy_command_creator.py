import boto3
import re
import os

#Usage: python main.py --bucket wave-prod-datalake --prefix jno-1039/identity/identity/ --rs_schema l1_identity [--gzip] [--csv] [--header] [--compupdate]

def generate_copy_command(bucket, prefix, rs_schema, gzip, csv, header, compupdate):
    client = boto3.client('s3')
    result = client.list_objects_v2(Bucket=bucket, Prefix=prefix, Delimiter='/')

    output_file = 'copy_{}.sql'.format(rs_schema)

    print('Generating Copy Commands for {} from s3://{}/{}.'.format(rs_schema, bucket, prefix))

    # Delete DDL file if exists
    if os.path.exists(output_file):
        os.remove(output_file)

    for o in result.get('CommonPrefixes'):
        path = o.get('Prefix')
        folder = re.sub(prefix, "", path)
        if folder.endswith('/'):
            folder = folder.rstrip('/').lower()

        copy_command = """COPY {}.{}
FROM 's3://{}/{}'
iam_role '{}'
REGION 'us-east-1'
TIMEFORMAT 'YYYY-MM-DD HH:MI:SS'
TRIMBLANKS
BLANKSASNULL
EMPTYASNULL
TRUNCATECOLUMNS
""".format(rs_schema, folder, bucket, path, iam_role)

        if csv:
            copy_command += "CSV \n"

        if gzip:
            copy_command += "GZIP \n"

        if header:
            copy_command += "IGNOREHEADER 1 \n"

        if compupdate:
            copy_command += "COMPUPDATE ON \n"
        else: copy_command += "COMPUPDATE OFF \n"

        copy_command += "; \n\n"

        # Generate the Config File
        with open(output_file, 'a') as f:
            f.write(copy_command)

    print('File {} generated.'.format(output_file))

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--bucket', help='S3 Bucket (example: wave-prod-datalake', type=str, required=True)
    parser.add_argument('--prefix', help='Prefix (Path to S3 folder)', type=str, required=True)
    parser.add_argument('--rs_schema', help='Schema in Redshift (example: l1_amplitude)', type=str, required=True)
    parser.add_argument('--iam_role', help='IAM Role to Use', type=str, required=False, default='arn:aws:iam::447253099639:role/Wave__OmahaDevDataLakeRole')
    parser.add_argument('--gzip', help='GZIP?', action='store_true', required=False, default=False)
    parser.add_argument('--csv', help='CSV?', action='store_true', required=False, default=False)
    parser.add_argument('--header', help='Header?', action='store_true', required=False, default=False)
    parser.add_argument('--compupdate', help='Compupdate?', action='store_true', required=False, default=False)
    options = parser.parse_args()

    #Assign IAM Role
    iam_role = options.iam_role

    generate_copy_command(options.bucket, options.prefix, options.rs_schema, options.gzip, options.csv, options.header, options.compupdate)