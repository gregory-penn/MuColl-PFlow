#!/bin/bash
# Delete all files of exactly 512 bytes in the current directory

# This works in the current directory. You could copy this to the running directory, or add a path feature.
# Dry run first: show which files would be deleted
echo "The following files are 512 bytes and will be deleted:"
find . -type f -size 0c -print

read -p "Delete these files? (y/N): " confirm
if [[ "$confirm" =~ ^[Yy]$ ]]; then
    find . -type f -size 512c -delete
    echo "Deleted all 512-byte files."
else
    echo "Aborted."
fi
