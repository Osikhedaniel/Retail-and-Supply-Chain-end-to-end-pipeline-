from extract_script import extracting_csv,structure_json
from Transformation_script import data_quality_check,data_transformation
from pathlib import Path 

def main():
    filepaths = [Path("Data Folder") / "Inventory Management E-Grocery - InventoryData.csv"]

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

        data_quality_checking = data_quality_check(df)
        Transformation =data_transformation(df)

if __name__  == "__main__":
    main()

