from extract import structure_json, extract_csv
from transform import data_quality_check, data_transformation
from pathlib import Path

def main():
    filepaths = ["test_data.json", "data.csv"]

    for filepath in filepaths:
        ext = Path(filepath).suffix.lower()

        if ext == ".json":
            df = structure_json(filepath)

        elif ext == ".csv":
            df = extract_csv(filepath)

        else:
            raise ValueError(f"Unsupported file type: {filepath}")

        print(f"Processed {filepath}")
        print(df.head(), "\n")

    quality_check = data_quality_check(df)
    transformation = data_transformation(df)


if __name__ == "__main__":
    main()


    