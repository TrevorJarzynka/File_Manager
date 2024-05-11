import os
import shutil
import logging
import argparse
import pdfplumber

# Setup logging
logging.basicConfig(filename='file_mover.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

# Custom rules for folder names based on file extensions
extension_folders = {
    '.txt': 'TextFiles',
    '.pdf': 'PDFDocuments',
    '.jpg': 'Images',
    '.png': 'Images',
}

def organize_files(source_directory):
    for filename in os.listdir(source_directory):
        full_path = os.path.join(source_directory, filename)
        if not os.path.isfile(full_path):
            continue

        # Check if the file name contains 'linear' (case insensitive)
        if 'linear' in filename.lower():
            new_folder_path = os.path.join(source_directory, 'Linear')
            if not os.path.exists(new_folder_path):
                os.makedirs(new_folder_path)
            shutil.move(full_path, os.path.join(new_folder_path, filename))
            logging.info(f'Moved {full_path} to {os.path.join(new_folder_path, filename)} due to keyword "linear" in file name')
            continue

        # Content-based handling for text and PDF files
        content_moved = False
        if filename.endswith('.txt') or filename.endswith('.pdf'):
            try:
                content = ''
                if filename.endswith('.txt'):
                    with open(full_path, 'r', encoding='utf-8') as file:
                        content = file.read().lower()
                elif filename.endswith('.pdf'):
                    with pdfplumber.open(full_path) as pdf:
                        content = ''.join(page.extract_text() or '' for page in pdf.pages).lower()

                if 'linear' in content:
                    new_folder_path = os.path.join(source_directory, 'Linear')
                    if not os.path.exists(new_folder_path):
                        os.makedirs(new_folder_path)
                    shutil.move(full_path, os.path.join(new_folder_path, filename))
                    logging.info(f'Moved {full_path} to {os.path.join(new_folder_path, filename)} due to content "linear"')
                    content_moved = True
            except Exception as e:
                logging.error(f'Error reading {full_path}: {e}')
        
        if content_moved:
            continue

        # File extension categorization
        extension = os.path.splitext(filename)[1]
        if extension in extension_folders:
            new_folder = extension_folders[extension]
            new_folder_path = os.path.join(source_directory, new_folder)
            if not os.path.exists(new_folder_path):
                os.makedirs(new_folder_path)
            shutil.move(full_path, os.path.join(new_folder_path, filename))
            logging.info(f'Moved {full_path} to {os.path.join(new_folder_path, filename)}')
        else:
            logging.info(f'No category found for {filename}, left in place.')

def main():
    parser = argparse.ArgumentParser(description="Organize files based on content and type")
    parser.add_argument("path", type=str, help="The path to the directory to scan and organize")
    args = parser.parse_args()

    print(f"Running file organization on directory: {args.path}")
    organize_files(args.path)

if __name__ == '__main__':
    main()
