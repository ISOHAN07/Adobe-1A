import os
import json
from pdf_parser import extract_pdf_structure # Import the logic

def main():
    """
    Main function to process all PDF files in the input directory
    and save the structured output to the output directory.
    """
    input_dir = "/app/input"
    output_dir = "/app/output"

    print("Starting PDF processing...")
    print(f"Input directory: {input_dir}")
    print(f"Output directory: {output_dir}")

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Get a list of all files in the input directory
    try:
        files_to_process = [f for f in os.listdir(input_dir) if f.lower().endswith('.pdf')]
    except FileNotFoundError:
        print(f"Error: Input directory '{input_dir}' not found. Please ensure it is mounted correctly.")
        return

    if not files_to_process:
        print("No PDF files found in the input directory.")
        return

    print(f"Found {len(files_to_process)} PDF file(s) to process.")

    # Process each PDF file
    for pdf_filename in files_to_process:
        input_pdf_path = os.path.join(input_dir, pdf_filename)
        
        # Define the output JSON filename
        base_filename = os.path.splitext(pdf_filename)[0]
        output_json_filename = f"{base_filename}.json"
        output_json_path = os.path.join(output_dir, output_json_filename)

        print(f"\nProcessing '{input_pdf_path}'...")

        # Extract the structure from the PDF
        structure_data = extract_pdf_structure(input_pdf_path)

        # Save the result to a JSON file
        try:
            with open(output_json_path, 'w', encoding='utf-8') as f:
                json.dump(structure_data, f, ensure_ascii=False, indent=4)
            print(f"Successfully saved structure to '{output_json_path}'")
        except Exception as e:
            print(f"Error saving JSON for '{pdf_filename}': {e}")

    print("\nPDF processing complete.")

if __name__ == "__main__":
    main()
