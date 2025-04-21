#!/usr/bin/env python3
import boto3
import subprocess
import argparse
import os
from datetime import datetime

def get_system_info(ip_address):
    # Create filename with IP address
    filename = f"/tmp/{ip_address}_system_info.txt"

    # Placeholder for system information collection command
    # This example assumes SSH access to execute commands remotely; customize as needed
    commands = [
        f"ssh user@{ip_address} 'uname -a'",
        f"ssh user@{ip_address} 'df -h'",
        # Add necessary commands here
    ]

    with open(filename, 'w') as f:
        f.write(f"System Information Collection Date: {datetime.now()}\n")
        f.write("="*50 + "\n\n")

        for command in commands:
            try:
                output = subprocess.check_output(command, shell=True).decode()
                f.write(f"### {command} ###\n")
                f.write(output + "\n\n")
            except Exception as e:
                f.write(f"Error executing {command}: {str(e)}\n\n")

    return filename

def upload_to_s3(file_path, bucket_name):
    try:
        s3_client = boto3.client('s3')
        file_name = os.path.basename(file_path)
        s3_client.upload_file(file_path, bucket_name, f"system_info/{file_name}")
        return True
    except Exception as e:
        print(f"Error uploading to S3: {str(e)}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Gather and upload system information.')
    parser.add_argument('--ip', required=True, help='IP address of the machine')
    parser.add_argument('--bucket', required=True, help='S3 bucket name')

    args = parser.parse_args()

    ip_address = args.ip
    bucket_name = args.bucket
    
    # Get system information
    file_path = get_system_info(ip_address)

    # Upload to S3
    if upload_to_s3(file_path, bucket_name):
        print(f"Successfully uploaded system information for {ip_address} to S3")
    
    # Cleanup temporary file
    try:
        os.remove(file_path)
        print(f"Cleaned up temporary file: {file_path}")
    except Exception as e:
        print(f"Error cleaning up file: {str(e)}")