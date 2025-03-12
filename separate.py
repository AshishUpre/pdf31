import os
import csv
import gzip
from Bio import SeqIO

# Paths
DATASET_DIR = "dataset"
CROHNS_DIR = "crohns_disease_fastq"
NON_CROHNS_DIR = "non_crohns_fastq"
METADATA_FILE = "detailsDiseasedOrNot.csv"

# Ensure output directories exist
os.makedirs(CROHNS_DIR, exist_ok=True)
os.makedirs(NON_CROHNS_DIR, exist_ok=True)

# Read metadata and create a mapping of Run ID to diagnosis
diagnosis_map = {}
with open(METADATA_FILE, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        run_id = row["Run"]
        diagnosis = row["diagnosis"]
        diagnosis_map[run_id] = diagnosis

# Function to process and save in FASTQ format
def process_fastq(fastq_path, output_path):
    try:
        # Handle gzipped files
        if fastq_path.endswith(".gz"):
            with gzip.open(fastq_path, "rt") as handle, open(output_path, "w") as out_handle:
                SeqIO.write(SeqIO.parse(handle, "fastq"), out_handle, "fastq")
        else:
            with open(fastq_path, "r") as handle, open(output_path, "w") as out_handle:
                SeqIO.write(SeqIO.parse(handle, "fastq"), out_handle, "fastq")

        print(f"Processed: {fastq_path} → {output_path}")
    except Exception as e:
        print(f"Error processing {fastq_path}: {e}")

# Process each folder inside the dataset directory
for folder in os.listdir(DATASET_DIR):
    folder_path = os.path.join(DATASET_DIR, folder)

    if os.path.isdir(folder_path):  # Ensure it's a directory
        run_id = folder  # Run ID is the folder name

        # Look for a FASTQ file inside the folder
        for file in os.listdir(folder_path):
            if file.endswith((".fastq", ".fastq.gz")):
                fastq_path = os.path.join(folder_path, file)

                if run_id in diagnosis_map:
                    output_dir = CROHNS_DIR if diagnosis_map[run_id] == "CD" else NON_CROHNS_DIR
                    output_path = os.path.join(output_dir, run_id + ".fastq")
                    process_fastq(fastq_path, output_path)
                else:
                    print(f"Run ID {run_id} not found in metadata.")

print("FASTQ processing complete.")
