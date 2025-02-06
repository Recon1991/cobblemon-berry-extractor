# Cobblemon Berry Extractor

A Python script that extracts **berry information** from Cobblemon JAR archives and outputs structured CSV files.

## Features  
✅ Extracts berry data from **`data/cobblemon/berries/`** inside a JAR archive  

✅ Outputs two CSV files:  
   - **Berry Info CSV:** Includes berry name, preferred biomes, and favorite mulches  
   - **Berry Mutations CSV:** Lists mutation results along with required berry pairs
  
✅ **Formatted output:**  
   - Properly capitalizes names  
   - Sorts the **mutation CSV by mutation berry name**
 
✅ **Configurable via `config.json`** 

---

## Installation & Setup  
### 1️⃣ Clone the Repository
```sh
git clone https://github.com/YOUR_GITHUB_USERNAME/Cobblemon-Berry-Extractor.git
cd Cobblemon-Berry-Extractor
```

### 2️⃣ Install Dependencies
Make sure you have Python installed (`>=3.7`), then install dependencies:
```sh
pip install -r requirements.txt
```
*(If `requirements.txt` isn’t available, install manually: `pip install colorama`)*  

### 3️⃣ Configure `config.json`
Edit the `config.json` file to match your setup:
```json
{
    "ARCHIVES_DIR": "../../zip_archives",
    "JAR_FILENAME": "Cobblemon-fabric-1.5.2+1.20.1.jar",
    "output_filename": "Cobblemon_berry_info_extract_v1.0",
    "MAX_WORKERS": 8,
    "LOG_FILENAME": "process_log.txt",
    "LOG_LEVEL": "INFO",
    "LOG_FORMAT": "%(asctime)s - %(levelname)s - %(message)s"
}
```

---

## Usage
Run the script with:
```sh
python Berry_Extractor_Cobblemon.py
```
Upon success, the following CSVs will be generated:  
✅ **`Cobblemon_berry_info_extract_v1.0.csv`** → Berry names, biomes, and mulches  
✅ **`Cobblemon_berry_mutations_v1.0.csv`** → Mutation berry results with parent berries  

---

## Example CSV Output

### Berry Info CSV (`Cobblemon_berry_info_extract_v1.0.csv`)
| Berry Name  | Preferred Biomes | Favorite Mulches  |
|-------------|-----------------|-------------------|
| Oran Berry  | Forest          | Peat Mulch       |
| Pecha Berry | Plains          | Rich Mulch       |

### Berry Mutations CSV (`Cobblemon_berry_mutations_v1.0.csv`)
| Mutation Berry Name | Berry #1     | Berry #2     |
|---------------------|--------------|--------------|
| Lum Berry         | Oran Berry   | Pecha Berry |
| Mago Berry        | Persim Berry | Wiki Berry  |

---

## Troubleshooting
🛠️ If the script fails to find the JAR file, ensure:  
1️⃣ The `zip_archives` directory is **two levels up** (`../../zip_archives`).  
2️⃣ The `JAR_FILENAME` in `config.json` matches the actual file name.  

For additional logging, check `process_log.txt`.

---

## Contributing
Pull requests are welcome! Open an issue if you find a bug or have feature suggestions.

---

## License
Mozilla Public License Version 2.0 
