import os

def phred_score(qual_str):
    """Convert ASCII quality score string to a list of Phred scores."""
    return [ord(char) - 33 for char in qual_str]  # Phred+33 encoding

def find_best_sequence(relative_fastq_path):
    """Finds the highest-quality sequence in a FASTQ file using a relative path."""
    fastq_file = os.path.abspath(relative_fastq_path)  # Convert to absolute path
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
                    best_seq = (identifier, sequence, plus, quality)

            except StopIteration:
                break  # End of file
            
    return best_seq, best_qual


a, b = find_best_sequence("./dataset/ERR1369179/ERR1369179.fastq")

print("best seq:", a)
print("best qual:", b)

print("best seq:", a)