# PhotoClassifier - Agent Instructions

## Project Overview

PhotoClassifier is a Python tool for organizing and deduplicating photo collections. It uses perceptual image hashing to identify similar photos and automatically consolidates image groups, keeping only the highest quality versions.

## Key Workflows

### Image Organization Workflow
1. **Group similar images**: `get_right_images.py` - Groups similar photos using perceptual hashing (phash)
2. **Consolidate and deduplicate**: `reorganizer.py` - Moves single images to root, keeps best quality from multi-image groups
3. **Cleanup empty folders**: `empty_folder_deleter.py` - Removes empty directories after reorganization

## Project Structure

- `reorganizer.py` - Main consolidation script (empty file indicates user will implement)
- `empty_folder_deleter.py` - Removes empty folders recursively
- `image_hash_generator.py` - Utility module for computing perceptual hashes
- `get_right_images.py` - Groups similar images based on hash similarity
- `README.md` - Project documentation
- `.gitignore` - Git ignore patterns (includes image group folders)

## Image Quality Scoring

Quality is assessed using a composite score:
- **Primary metric**: Resolution (pixel count = width × height)
- **Secondary metric**: File size (bytes)
- **Formula**: `quality_score = (resolution * 1000) + file_size`

Higher scores indicate better quality images.

## Image Extensions Supported

`.jpg`, `.jpeg`, `.png`, `.webp`, `.gif`, `.bmp`

## Common Tasks

### Running the Complete Workflow
```bash
python get_right_images.py  # Group similar images
python reorganizer.py       # Consolidate and keep best quality
python empty_folder_deleter.py  # Clean up empty folders
```

### Adding New Features
- **Modify quality scoring**: Edit `reorganizer.py` `get_image_quality()` function
- **Change similarity threshold**: Edit `get_right_images.py` similarity comparison logic
- **Support new image formats**: Update `IMAGE_EXTENSIONS` tuple in relevant scripts

## Development Notes

- Images are identified by resolution and file size for quality ranking
- Perceptual hashing allows identification of nearly identical images
- All operations are file-system based (no database required)
- Scripts use `os.walk()` for robust directory traversal
- Error handling is comprehensive to handle corrupted images gracefully
