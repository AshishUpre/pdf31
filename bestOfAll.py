import os

def phred_score(qual_str):
    """Convert ASCII quality score string to a list of Phred scores."""
    return [ord(char) - 33 for char in qual_str]  # Phred+33 encoding

def find_best_sequence(fastq_file):
    """Finds the highest-quality sequence in a FASTQ file."""
    best_seq = None
    best_qual = -1

    with open(fastq_file, "r") as f:
        while True:
            try:
                identifier = next(f).strip()   # Line 1: Sequence ID
                sequence = next(f).strip()     # Line 2: DNA sequence
                plus = next(f).strip()         # Line 3: '+'
                quality = next(f).strip()      # Line 4: Quality scores
                
                avg_quality = sum(phred_score(quality)) / len(quality)

                if avg_quality > best_qual:
                    best_qual = avg_quality
                    best_seq = (identifier, sequence)

            except StopIteration:
                break  # End of file
            
    return best_seq, best_qual


def process_dataset(dataset_dir, output_fasta):
    """Processes all FASTQ files in the dataset and saves the best sequences in a FASTA file."""
    with open(output_fasta, "w") as out_f:
        for subdir in os.listdir(dataset_dir):
            subdir_path = os.path.join(dataset_dir, subdir)
            if os.path.isdir(subdir_path):  # Ensure it's a directory
                for file in os.listdir(subdir_path):
                    if file.endswith(".fastq"):
                        fastq_path = os.path.join(subdir_path, file)
                        best_seq, best_qual = find_best_sequence(fastq_path)
                        if best_seq:
                            identifier, sequence = best_seq
                            out_f.write(f">{identifier}\n{sequence}\n")
                            print(f"Processed {fastq_path}: Best sequence saved.")


# Set dataset directory and output file
dataset_path = "./dataset"
output_fasta_file = "./best_sequences.fasta"

process_dataset(dataset_path, output_fasta_file)
print(f"\nBest sequences saved in {output_fasta_file}")
