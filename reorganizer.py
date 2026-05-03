import os
import shutil
from PIL import Image
from pathlib import Path

# Configuration
ROOT_FOLDER = r"C:\Everything\PhotoClassifier"
IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.webp', '.gif', '.bmp')


def get_images(folder):
    """Get all image files in a folder"""
    files = []
    try:
        for file in os.listdir(folder):
            if file.lower().endswith(IMAGE_EXTENSIONS):
                files.append(os.path.join(folder, file))
    except:
        pass
    return files


def get_image_quality(image_path):
    """
    Assess image quality based on resolution and file size
    Returns a score for quality ranking
    """
    try:
        # Get resolution
        img = Image.open(image_path)
        resolution = img.width * img.height

        # Get file size
        file_size = os.path.getsize(image_path)

        # Quality score: prioritize resolution, then file size
        quality_score = (resolution * 1000) + file_size
        return quality_score, resolution, file_size
    except Exception as e:
        print(f"Error analyzing {image_path}: {e}")
        return 0, 0, 0


def process_image_groups():
    """Process all image group folders"""
    group_folders = []

    # Find all folders ending with _group
    for item in os.listdir(ROOT_FOLDER):
        item_path = os.path.join(ROOT_FOLDER, item)
        if os.path.isdir(item_path) and item.endswith('_group'):
            group_folders.append(item_path)

    print(f"Found {len(group_folders)} image group folders")

    stats = {"moved": 0, "deleted": 0, "skipped": 0}

    for folder in sorted(group_folders):
        images = get_images(folder)
        folder_name = os.path.basename(folder)

        if len(images) == 0:
            print(f"[SKIP] {folder_name}: No images found")
            stats["skipped"] += 1
            continue

        elif len(images) == 1:
            # Move single image to root
            src = images[0]
            filename = os.path.basename(src)
            dst = os.path.join(ROOT_FOLDER, filename)

            try:
                shutil.move(src, dst)
                print(f"[MOVE] {folder_name}: Moved {filename} to root")
                stats["moved"] += 1
            except Exception as e:
                print(f"[ERROR] {folder_name}: Failed to move {filename}: {e}")

        else:
            # Multiple images: keep only the highest quality one
            print(f"[INFO] {folder_name}: Found {len(images)} images")

            # Score all images
            scored_images = []
            for img_path in images:
                score, resolution, file_size = get_image_quality(img_path)
                scored_images.append((img_path, score, resolution, file_size))

            # Sort by quality score (highest first)
            scored_images.sort(key=lambda x: x[1], reverse=True)

            # Keep the best one
            best_image = scored_images[0]
            best_path = best_image[0]
            best_resolution = best_image[2]
            best_size = best_image[3]

            # Move best image to root
            filename = os.path.basename(best_path)
            dst = os.path.join(ROOT_FOLDER, filename)

            try:
                shutil.move(best_path, dst)
                print(
                    f"  ✓ Kept: {filename} ({best_resolution}px, {best_size} bytes)")
                stats["moved"] += 1
            except Exception as e:
                print(f"  ✗ Failed to move best image: {e}")

            # Delete lower quality images
            for img_path, score, resolution, file_size in scored_images[1:]:
                filename = os.path.basename(img_path)
                try:
                    os.remove(img_path)
                    print(
                        f"  ✗ Deleted: {filename} ({resolution}px, {file_size} bytes)")
                    stats["deleted"] += 1
                except Exception as e:
                    print(f"  ✗ Failed to delete {filename}: {e}")

    print("\n" + "="*60)
    print(
        f"Summary: Moved: {stats['moved']} | Deleted: {stats['deleted']} | Skipped: {stats['skipped']}")
    print("="*60)


if __name__ == "__main__":
    process_image_groups()
