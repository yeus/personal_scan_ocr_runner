#!/usr/bin/env python3

import concurrent.futures
import os
import subprocess
from pathlib import Path

import typer


def ocr_path(f: Path):
    new_path = './ocrd' / f.parent
    new_path.mkdir(parents=True, exist_ok=True)
    return new_path


def remove_empty_dirs(root):
    folders = list(os.walk(root))[1:]

    for folder, files, subfolders in folders:
        # folder example: ('FOLDER/3', [], ['file'])
        # if no files and folders
        if not files and not subfolders:
            print(f"remove {folder}")
            os.rmdir(folder)


def symlink_file(f: Path):
    #TODO: make symlinks relativ, so that they also work on
    #       other computers...
    new_path = ocr_path(f)
    new_link = new_path / f.name
    # create a symlink to original file
    try:
        new_link.symlink_to(f.resolve())
    except:
        print("symlink exists already")


def ocr_file(f: Path):
    print(f"ocr#: {f}")
    new_path = ocr_path(f)
    new_file = new_path / (f.name + '.ocr.pdf')
    # try to ocr the file and save it in the respective directory with an additional
    # suffic
    # TODO: do the preprocessing only for images
    if f.suffix.lower() != '.pdf':
        cmd = (
            f'exiftool -n -Orientation=1 "{str(f.absolute())}" -o - | '
            'img2pdf --pagesize A4 | '
            f'ocrmypdf --clean-final --deskew --rotate-pages -l eng+deu - "{str(new_file.absolute())}"'
        )
        print(f"command: {cmd}")
        result = subprocess.run(cmd, shell=True)
    else:
        cmd = (
            f'ocrmypdf --clean-final --deskew --rotate-pages"'
            f'--optimize 2 -l eng+deu '
            f'"{str(f.absolute())}" "{str(new_file.absolute())}"'
        )
        print(f"command: {cmd}")
        result = subprocess.run(cmd, shell=True)

    """result = subprocess.run([
        "ocrmypdf", "--clean-final",
        "--rotate-pages",
        "--jobs", "5",
        "--optimize", "2",
        "--deskew",
        "-l", "eng+deu",
        str(f.absolute()), str(new_file.absolute())])"""

    # print(f"return code: {result}")
    return result


def main(
        ocr: bool = False,
        remove_empty_directories: bool = False,
        symlinks: bool = False,
        show_info: bool = True,
        job_num: int=5,
):
    directory = Path(".")
    # all_files = [Path(os.path.join(path, name)) for path, subdirs, files in os.walk(directory) for name in files]
    all_files = [f for f in Path(directory).rglob('*') if f.is_file()]

    # exclude ocrd path
    scan_files = {f for f in all_files if not f.parts[0].startswith('ocrd')}
    scan_files = {f for f in scan_files if f.suffix.lower() in ['.jpg', '.jpeg', '.png', '.pdf']}

    # remove ocrd parent dir from these files
    ocrd_files = {f for f in all_files if f.parts[0].startswith('ocrd')}
    ocrd_cmpr = {Path(*f.parts[1:]).with_suffix('').with_suffix('') for f in ocrd_files}
    # ocrd_cmpr = {f.parent / f.stems for f in ocrd_files}
    #

    # get files that weren't ocrd'd yet:
    new_files = scan_files.difference(ocrd_cmpr)
    if show_info:
        info = dict(
            all_files_len=len(all_files),
            scan_files_len=len(scan_files),
            ocrd_files_len=len(ocrd_files),
            new_files_len=len(new_files)
        )
        print(f"{info}")

    if ocr:
        with concurrent.futures.ThreadPoolExecutor(max_workers=job_num) as executor:
            future_to_file = {executor.submit(ocr_file, f): f for i, f in enumerate(new_files)}
            for future in concurrent.futures.as_completed(future_to_file):
                file = future_to_file[future]
                try:
                    data = future.result()
                    print(f"returned data: {data}")
                except Exception as exc:
                    print(f'{file} generated an exception: {exc}')

    if remove_empty_directories:
        for i in range(10):
            # remove subfolder up to 10 levels deep
            remove_empty_dirs(directory / "ocrd")

    if symlinks:
        # add symlinks
        for i, f in enumerate(all_files):
            symlink_file(f)


if __name__ == "__main__":
    typer.run(main)

# TODO: add parallel processing with asyncio subprocesses
# https://docs.python.org/3/library/asyncio-subprocess.html

# https://stackoverflow.com/questions/48483348/how-to-limit-concurrency-with-python-asyncio/48486557
"""async def gather_with_concurrency(n, *tasks):
    semaphore = asyncio.Semaphore(n)

    async def sem_task(task):
        async with semaphore:
            return await task
    return await asyncio.gather(*(sem_task(task) for task in tasks))"""
