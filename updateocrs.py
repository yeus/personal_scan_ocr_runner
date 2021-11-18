#!/usr/bin/env python

import concurrent.futures
import subprocess
from pathlib import Path

directory = "."
# all_files = [Path(os.path.join(path, name)) for path, subdirs, files in os.walk(directory) for name in files]
all_files = [f for f in Path('.').rglob('*') if f.is_file()]

# exclude ocrd path
scan_files = {f for f in all_files if not f.parts[0].startswith('ocrd')}
scan_files = {f for f in scan_files if f.suffix in ['.jpg']}

# remove ocrd parent dir from these files
ocrd_files = {f for f in all_files if f.parts[0].startswith('ocrd')}
ocrd_cmpr = {Path(*f.parts[1:]).with_suffix('') for f in ocrd_files}
#

# get files that weren't ocrd'd yet:
new_files = scan_files.difference(ocrd_cmpr)
info = dict(
    all_files_len=len(all_files),
    scan_files_len=len(scan_files),
    ocrd_files_len=len(ocrd_files),
    new_files_len=len(new_files)
)
print(f"{info}")


def ocr_path(f: Path):
    new_path = './ocrd' / f.parent
    new_path.mkdir(parents=True, exist_ok=True)
    return new_path


def symlink_file(f: Path):
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
    result = subprocess.run([
        "ocrmypdf", "--clean-final", "--deskew", "-l", "eng+deu",
        str(f.absolute()), str(new_file.absolute())])

    print(f"return code: {result}")
    return result


# current numberof files
# add suffix
# for i, f in enumerate(new_files):
#    ocr_file(f)
#    if i > 10: break

with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    future_to_file = {executor.submit(ocr_file, f): f for i, f in enumerate(new_files)}
    for future in concurrent.futures.as_completed(future_to_file):
        url = future_to_file[future]
        try:
            data = future.result()
            print(f"returned data: {data}")
        except Exception as exc:
            print('%r generated an exception: %s' % (url, exc))
        else:
            print('%r page is %d bytes' % (url, len(data)))

# TODO: add parallel processing with asyncio subprocesses
# https://docs.python.org/3/library/asyncio-subprocess.html

# https://stackoverflow.com/questions/48483348/how-to-limit-concurrency-with-python-asyncio/48486557
"""async def gather_with_concurrency(n, *tasks):
    semaphore = asyncio.Semaphore(n)

    async def sem_task(task):
        async with semaphore:
            return await task
    return await asyncio.gather(*(sem_task(task) for task in tasks))"""
