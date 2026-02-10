from extract_script import extracting_csv,structure_json
from pathlib import Path 

def main():
    filepaths = ["C://Users//HP//Documents//winners_f1_1950_2025_v2.csv"]

    for filepath in filepaths:
        ext = Path(filepath).suffix.lower()

        if ext == ".json":
            df = structure_json(filepath)
        elif ext == ".csv":
            df = extracting_csv(filepath)
        else:
            raise ValueError(f"Unsupported file format: {filepath}")
        
        print(f"processed:{filepath}")
        print(df.head(),"\n")

if __name__  == "__main__":
    main()

