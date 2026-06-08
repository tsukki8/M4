from pathlib import Path
import argparse
from astropy.io import fits
import json

def read_sdfits_folder():
    # Reads all SDFITS (.fits) files in a folder.
    folder = Path("./fits")
    fits_files = list(folder.glob("*.fits")) + list(folder.glob("*.sdf"))

    if not fits_files:
        print(f"No SDFITS files found in: {folder}")
        return

    results = []

    for file in sorted(fits_files):
        print(f"Reading: {file.name}")
        with fits.open(file) as hdul:
            file_info = {
                "filename": file.name,
                "n_extensions": len(hdul),
                "extensions": []
            }
            for i, hdu in enumerate(hdul):
                ext_info = {
                    "index": i,
                    "name": hdu.name,
                    "type": type(hdu).__name__,
                    "header_keys": list(hdu.header.keys()),
                }
                if hasattr(hdu, 'columns') and hdu.columns:
                    ext_info["columns"] = hdu.columns.names
                if hasattr(hdu, 'data') and hdu.data is not None:
                    ext_info["n_rows"] = len(hdu.data)
                file_info["extensions"].append(ext_info)
            results.append(file_info)

    # saves summary if output_file is specified and prompted
    if output_file:
        output_path = Path(output_file)
        with open(output_path, "w") as f:
            json.dump(results, f, indent=2)
        print(f"Saved summary: {output_path}")

    # saves individual JSON files for ea FITS file
    output_dir = Path(__file__).parent / "translate_json"
    output_dir.mkdir(parents=True, exist_ok=True)

    for file_info in results:
        file_name = file_info["filename"]
        out_path = output_dir / (Path(file_name).stem + ".json")
        with open(out_path, "w") as f:
            json.dump(file_info, f, indent=2)
        print(f"Saved: {out_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Read SDFITS files from a folder.")
    read_sdfits_folder()