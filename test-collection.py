import csv
import os

# Input and output file paths
envs_csv = ['environemntA', 'environmentB']
zero_connections = 'rds-instances-zero-connections.csv'

# Open input CSV file in read mode
with open(zero_connections, mode='w', newline='', encoding='utf-8') as outfile:
    writer = csv.writer(outfile)
    
    # Loop through each input file
    for env in envs_csv:
        # Check if the file exists before processing
        if os.path.exists(env):
            print(f"Processing {env}...")
            # Open the current input file in read mode
            with open(env, mode='r', newline='', encoding='utf-8') as infile:
                reader = csv.reader(infile)

                writer.writerow([f"For the file {env} :"])
                writer.writerow(["Instance Name", "Instance Class", "Allocated Storage", "Postgres Version", "multiAZ", "Connections in the last 4 weeks"])
                
                
                # Iterate through each row in the input CSV
                for row in reader:
                    # Check if '0.0' exists in the row
                    if '0.0' in row:
                        # Write the row to the output file
                        writer.writerow(row)
        else:
            print(f"File {env} does not exist. Skipping.")
            
print(f"Rows with '0.0' have been copied to {zero_connections}")