#!/bin/bash

# Configuration
S3_BUCKET="your-bucket-name"
IP_ADDRESS=$(hostname -I | awk '{print $1}')
OUTPUT_FILE="/tmp/${IP_ADDRESS}.txt"
DATE=$(date '+%Y-%m-%d %H:%M:%S')

# Ensure AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo "AWS CLI is not installed. Please install it first."
    exit 1
fi

# Create system information file
create_system_info() {
    echo "System Information Collection Date: $DATE" > "$OUTPUT_FILE"
    echo "========================================" >> "$OUTPUT_FILE"
    
    # Collection of system information
    echo -e "\n### System Information ###" >> "$OUTPUT_FILE"
    uname -a >> "$OUTPUT_FILE" 2>&1
    
    echo -e "\n### Disk Usage ###" >> "$OUTPUT_FILE"
    df -h >> "$OUTPUT_FILE" 2>&1
    
    echo -e "\n### Memory Usage ###" >> "$OUTPUT_FILE"
    free -h >> "$OUTPUT_FILE" 2>&1
    
    echo -e "\n### Process Information ###" >> "$OUTPUT_FILE"
    top -bn1 >> "$OUTPUT_FILE" 2>&1
    
    echo -e "\n### Network Connections ###" >> "$OUTPUT_FILE"
    netstat -tuln >> "$OUTPUT_FILE" 2>&1
    
    echo -e "\n### Running Processes ###" >> "$OUTPUT_FILE"
    ps aux >> "$OUTPUT_FILE" 2>&1
    
    echo -e "\n### CPU Information ###" >> "$OUTPUT_FILE"
    lscpu >> "$OUTPUT_FILE" 2>&1
    
    echo -e "\n### Full Hostname ###" >> "$OUTPUT_FILE"
    hostname -f >> "$OUTPUT_FILE" 2>&1
}

# Upload file to S3
upload_to_s3() {
    if aws s3 cp "$OUTPUT_FILE" "s3://${S3_BUCKET}/system_info/$(basename "$OUTPUT_FILE")"; then
        echo "Successfully uploaded system information to S3"
        return 0
    else
        echo "Failed to upload to S3"
        return 1
    fi
}

# Cleanup
cleanup() {
    if rm "$OUTPUT_FILE"; then
        echo "Cleaned up temporary file: $OUTPUT_FILE"
    else
        echo "Failed to clean up temporary file: $OUTPUT_FILE"
    fi
}

# Main execution
main() {
    echo "Starting system information collection..."
    create_system_info
    
    echo "Uploading to S3..."
    upload_to_s3
    
    echo "Cleaning up..."
    cleanup
}

# Run the script
main
