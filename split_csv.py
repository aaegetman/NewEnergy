import pandas as pd
import os

# Define chunk size (number of rows per chunk)
CHUNK_SIZE = 100000  # Adjust this based on your needs

# Path to the large CSV file
file_path = 'energyThesis/data/P6269_1_50_DMK_Sample_Elek.csv'

print(f"Processing {file_path}...")

# Create output directories for chunks and combined files
base_dir = os.path.dirname(file_path)
chunks_dir = os.path.join(base_dir, 'chunks')
os.makedirs(chunks_dir, exist_ok=True)

# Use pandas read_csv with chunksize parameter
# This processes the CSV in chunks without loading the entire file into memory
chunk_paths = []
for i, chunk in enumerate(pd.read_csv(file_path, chunksize=CHUNK_SIZE)):
    chunk_file = os.path.join(chunks_dir, f'chunk_{i}.csv')
    print(f"Writing chunk {i} to {chunk_file}")
    chunk.to_csv(chunk_file, index=False)
    chunk_paths.append(chunk_file)

    # Stop after creating 60 chunks
    if i == 59:
        print("60 chunks created, stopping as requested.")
        break

# Combine all 60 chunks into a single file
print("Combining all 60 chunks...")
combined_path = os.path.join(base_dir, 'combined_60_chunks.csv')

# Read and combine all chunks
combined = pd.concat((pd.read_csv(chunk_path) for chunk_path in chunk_paths), ignore_index=True)

# Save combined file
combined.to_csv(combined_path, index=False)
print(f"Combined file saved to {combined_path}")

print("Chunking and combining completed!")