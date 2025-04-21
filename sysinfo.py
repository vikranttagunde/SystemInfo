#!/usr/bin/env python3
import boto3
import subprocess
import socket
import os
from datetime import datetime

def get_system_info():
    # Get IP address
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    
    # Create filename with IP address
    filename = f"/tmp/{ip_address}.txt"
    
    # Collect system information
    system_info = []
    commands = [
        "uname -a",           # System information
        "df -h",              # Disk usage
        "free -h",            # Memory usage
        "top -bn1",          # Process information
        "netstat -tuln",      # Network connections
        "ps aux",            # Running processes
        "lscpu",             # CPU information
        "hostname -f"         # Full hostname
    ]
    
    with open(filename, 'w') as f:
        f.write(f"System Information Collection Date: {datetime.now()}\n")
        f.write("="*50 + "\n\n")
        
        for command in commands:
            try:
                output = subprocess.check_output(command.split()).decode()
                f.write(f"### {command} ###\n")
                f.write(output + "\n\n")
            except Exception as e:
                f.write(f"Error executing {command}: {str(e)}\n\n")
    
    return filename, ip_address

def upload_to_s3(file_path, bucket_name):
    try:
        s3_client = boto3.client('s3')
        file_name = os.path.basename(file_path)
        s3_client.upload_file(file_path, bucket_name, f"system_info/{file_name}")
        return True
    except Exception as e:
        print(f"Error uploading to S3: {str(e)}")
        return False

def main():
    # S3 bucket name
    BUCKET_NAME = "your-bucket-name"
    
    # Get system information
    file_path, ip_address = get_system_info()
    
    # Upload to S3
    if upload_to_s3(file_path, BUCKET_NAME):
        print(f"Successfully uploaded system information for {ip_address} to S3")
    else:
        print("Failed to upload to S3")
    
    # Cleanup temporary file
    try:
        os.remove(file_path)
        print(f"Cleaned up temporary file: {file_path}")
    except Exception as e:
        print(f"Error cleaning up file: {str(e)}")

if __name__ == "__main__":
    main()