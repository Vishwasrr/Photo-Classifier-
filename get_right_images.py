import shutil
from tqdm import tqdm
from PIL import Image
import imagehash
import os

IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.webp')


def get_images(folder):
    files = []
    for file in os.listdir(folder):
        if file.lower().endswith(IMAGE_EXTENSIONS):
            files.append(os.path.join(folder, file))
    return files


def get_hash(image_path):
    try:
        img = Image.open(image_path)
        return imagehash.phash(img)
    except:
        return None


def similarity(hash1, hash2):
    return 1 - (hash1 - hash2) / 64


def group_images(image_paths):
    hashes = {}

    for path in tqdm(image_paths):
        h = get_hash(path)
        if h:
            hashes[path] = h

    groups = []
    visited = set()

    for img1, hash1 in hashes.items():
        if img1 in visited:
            continue

        group = [img1]
        visited.add(img1)

        for img2, hash2 in hashes.items():
            if img2 in visited:
                continue

            if similarity(hash1, hash2) >= 0.9:
                group.append(img2)
                visited.add(img2)

        if len(group) > 1:
            groups.append(group)

    return groups


def get_resolution(image_path):
    try:
        img = Image.open(image_path)
        return img.size[0] * img.size[1]
    except:
        return 0


def pick_best(group):
    return max(group, key=get_resolution)


def organize_groups(groups):
    for group in groups:
        best = pick_best(group)
        base_name = os.path.splitext(os.path.basename(best))[0]

        folder_name = f"{base_name}_group"
        os.makedirs(folder_name, exist_ok=True)

        for img in group:
            if img == best:
                continue
            shutil.move(img, os.path.join(folder_name, os.path.basename(img)))


def main(folder):
    images = get_images(folder)
    groups = group_images(images)
    organize_groups(groups)


if __name__ == "__main__":
    folder_path = r"C:\Users\Vishw\Downloads\Image\Vineeth's wedding"
    main(folder_path)
