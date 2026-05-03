# PhotoClassifier

A Python-based image organization and classification tool for managing photo collections.

## Overview

This project provides automated tools to:
- **Organize images** by grouping similar photos using perceptual hashing
- **Identify duplicates** and keep only the highest quality versions
- **Clean up** empty folders after reorganization

## Scripts

### `reorganizer.py`
Processes image group folders and consolidates them:
- **Single image folders**: Moves the image to the root directory
- **Multi-image folders**: Keeps only the highest quality image (by resolution and file size), deletes lower quality duplicates

**Usage:**
```bash
python reorganizer.py
```

### `empty_folder_deleter.py`
Removes all empty folders from the project directory, useful for cleanup after reorganization.

**Usage:**
```bash
python empty_folder_deleter.py
```

### `image_hash_generator.py`
Utility module for generating perceptual hashes of images to identify similar photos.

### `get_right_images.py`
Groups similar images together based on perceptual hashing algorithms.

## Quality Assessment

Images are ranked by quality based on:
1. **Resolution** (primary): Total pixel count (width × height)
2. **File size** (secondary): Larger files typically indicate better quality

## Requirements

- Python 3.6+
- Pillow (PIL)
- imagehash
- tqdm

## Installation

```bash
pip install Pillow imagehash tqdm
```

## Workflow

1. Run `get_right_images.py` to group similar photos
2. Run `reorganizer.py` to consolidate folders and keep only the best images
3. Run `empty_folder_deleter.py` to clean up remaining empty directories

## Output

All organized images are consolidated in the root directory. Group folders are cleaned up after processing.
