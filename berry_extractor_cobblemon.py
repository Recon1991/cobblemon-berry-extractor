import os
import json
import csv
import zipfile
import logging
from concurrent.futures import ThreadPoolExecutor
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Load config
CONFIG_FILE = "config.json"
def load_config():
    """Load configuration from the config.json file."""
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(Fore.RED + "Config file not found! Using defaults.")
        return {}

config = load_config()

# Set up paths
ARCHIVES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../zip_archives"))  # Two levels up
JAR_FILENAME = config.get("JAR_FILENAME", "Cobblemon-fabric-1.5.2+1.20.1.jar")  # Configurable JAR file name
OUTPUT_FILENAME = config.get("output_filename", "Cobblemon_berry_info_extract_v1.0")
MUTATION_FILENAME = "Cobblemon_berry_mutations_v1.0.csv"  # Mutation CSV filename
MAX_WORKERS = config.get("MAX_WORKERS", 8)

# Ensure output filenames have .csv extension
if not OUTPUT_FILENAME.endswith(".csv"):
    OUTPUT_FILENAME += ".csv"

# Set up logging
logging.basicConfig(
    filename=config.get("LOG_FILENAME", "process_log.txt"),
    level=getattr(logging, config.get("LOG_LEVEL", "INFO").upper(), logging.INFO),
    format=config.get("LOG_FORMAT", "%(asctime)s - %(levelname)s - %(message)s")
)

def format_biome_tag(tag):
    """Format biome tags like 'cobblemon:is_forest' to 'Forest'."""
    return tag.split(":")[-1].replace("is_", "").replace("_", " ").title()

def find_berry_archive():
    """Find the specific JAR archive containing the berry data."""
    jar_path = os.path.join(ARCHIVES_DIR, JAR_FILENAME)
    
    if not os.path.exists(jar_path):
        print(Fore.RED + f"Target JAR not found: {jar_path}")
        logging.error(f"Target JAR not found: {jar_path}")
        return None

    print(Fore.CYAN + f"Using JAR archive: {JAR_FILENAME}")
    return jar_path

def extract_berry_data(jar_path):
    """Extract berry biome tags, favorite mulches, and mutations from a given JAR archive."""
    berry_data = []
    mutation_data = []
    
    with zipfile.ZipFile(jar_path, 'r') as jar_file:
        for file in jar_file.namelist():
            if file.startswith("data/cobblemon/berries/") and file.endswith(".json"):
                with jar_file.open(file) as f:
                    try:
                        data = json.load(f)
                        berry_name = os.path.basename(file).replace(".json", "").replace("cobblemon:", "").replace("_", " ").title()
                        
                        # Extract biome tags
                        biomes = data.get("preferredBiomeTags", [])
                        formatted_biomes = [format_biome_tag(b) for b in biomes]
                        
                        # Extract favorite mulches and format them with title()
                        favorite_mulches = [mulch.title() + " Mulch" for mulch in data.get("favoriteMulches", [])]
 
                        berry_data.append([berry_name, ", ".join(formatted_biomes), ", ".join(favorite_mulches)])
                        
                        # Extract mutations
                        mutations = data.get("mutations", {})
                        for other_berry, mutation_berry in mutations.items():
                            # Format berry names properly (remove 'cobblemon:' prefix if present)
                            formatted_other_berry = other_berry.replace("cobblemon:", "").replace("_", " ").title()
                            formatted_mutation_berry = mutation_berry.replace("cobblemon:", "").replace("_", " ").title()

                            # Add to mutation CSV data
                            mutation_data.append([berry_name, formatted_other_berry, formatted_mutation_berry])
                    except json.JSONDecodeError:
                        print(Fore.RED + f"Failed to parse {file} in {jar_path}")
                        logging.error(f"Failed to parse {file} in {jar_path}")
    
    return berry_data, mutation_data

def process_archive():
    """Process the single JAR archive containing berry data."""
    jar_path = find_berry_archive()
    if not jar_path:
        return [], []

    print(Fore.CYAN + f"Processing archive: {os.path.basename(jar_path)}")
    return extract_berry_data(jar_path)

def write_csv(filename, data, headers):
    """Write extracted data to CSV."""
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(data)
    print(Fore.GREEN + f"CSV saved: {filename}")

def main():
    print(Fore.YELLOW + "Starting Cobblemon Berry Extractor...")
    
    berry_data, mutation_data = process_archive()
    
    if berry_data:
        write_csv(OUTPUT_FILENAME, berry_data, ["Berry Name", "Preferred Biomes", "Favorite Mulches"])
    else:
        print(Fore.RED + "No berry data extracted!")

    if mutation_data:
        mutation_data.sort(key=lambda x: x[0])  # Sort by Mutation Berry Name (column 0)
        write_csv(MUTATION_FILENAME, mutation_data, ["Mutation Berry Name", "Berry Name", "Other Berry Name"])
    else:
        print(Fore.RED + "No mutation data extracted!")

    print(Fore.GREEN + "Extraction complete!")

if __name__ == "__main__":
    main()
