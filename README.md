# PSOR personal_scan_ocr_runner

This python script was developed to help organizing a directory of pdf/image scans into readable PDFs by applying OCR on them.

## Usage

```
Usage: updateocrs.py [OPTIONS]

Options:
  --ocr / --no-ocr                [default: False]
  --remove-empty-directories / --no-remove-empty-directories
                                  [default: False]
  --symlinks / --no-symlinks      [default: False]
  --show-info / --no-show-info    [default: True]
  --job-num INTEGER               [default: 5]
  --install-completion            Install completion for the current shell.
  --show-completion               Show completion for the current shell, to
                                  copy it or customize the installation.

  --help                          Show this message and exit.
```

## Features

This script is at the moment based on [OCRmyPDF](https://github.com/jbarlow83/OCRmyPDF) and [img2pdf](https://gitlab.mister-muffin.de/josch/img2pdf).

- Create a mirrored directory with the same structure as the original.
- All jpgs, pngs and pdfs are converted into reasonable sized black-white pdfs with OCR applied (we are using img2pdf and ocrmypdf).
- When updating, avoid rerunning OCR on pdfs/images that were already converted into readable text.
- The script does not touch or alter the original files/directories in any way.

## Installation:

- run the install script
- change the install script in order to support more languages (default: german)

## Introduction

### The Scenario

- one large directory for a family which gets synchronized using syncthing over multiple computers
- scans and documents (tax declarations, school-documents, scans of certificates etc...) all go into one large directory
- We have a system (tested with KDE for example) which can automatically read text in pdf
  files and make the searchable (In the case of KDE you can search the contents of a pdf file using
  the baloo file indexer)

### The Goal

- We would like to apply OCR on that directory including all its subdirectories to create a "mirrored" version of it
  which has a copy of all the scanned documents with machine-readable text created by an OCR application.
- The file indexer should now pick up the new ocrd files and register them in the index to make them searchable. We should
  now be able to search all of our scanned documents..

### Enter "PSOR"

- Scan a directory and ocr all pdfs and jpg and pngs. Convert them all into pdfs with a reasonable resolution.
  Mirror the directory structure into a new folder called "ocrd" inside the same directory.
  
Together with a file indexer such as *baloo* this makes it very easy to find old documents.

## Who can use this script?

- Whoever wants to regularly OCR a directory with scanned images.

## File Indexing alternatives:

- baloo (KDE/Linux)
- recoll
- and more ...

## Tested with:

- ubuntu 20.04
