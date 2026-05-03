import os
import shutil

ROOT_FOLDER = r"C:\Everything\PhotoClassifier"


def is_empty_folder(folder_path):
    """Check if a folder is empty"""
    try:
        return len(os.listdir(folder_path)) == 0
    except:
        return False


def remove_empty_folders():
    """Remove all empty folders recursively"""
    removed_count = 0

    # Walk through all directories from deepest to shallowest
    for dirpath, dirnames, filenames in os.walk(ROOT_FOLDER, topdown=False):
        for dirname in dirnames:
            folder_path = os.path.join(dirpath, dirname)

            if is_empty_folder(folder_path):
                try:
                    os.rmdir(folder_path)
                    print(f"✓ Deleted: {folder_path}")
                    removed_count += 1
                except Exception as e:
                    print(f"✗ Failed to delete {folder_path}: {e}")

    print("\n" + "="*60)
    print(f"Total empty folders removed: {removed_count}")
    print("="*60)


if __name__ == "__main__":
    remove_empty_folders()
