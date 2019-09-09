#!/usr/bin/env python3
"""
Check sha256 hash of file against a checksum

python3 check_hash.py file_name checksum
"""
import hashlib
import pathlib


def get_digest(file_path):
    """Get sha256 for a file

    from:
    https://stackoverflow.com/a/55542529/5501519
    """
    h = hashlib.sha256()
    with open(file_path, "rb") as file:
        while True:
            # Reading is buffered, so we can read smaller chunks.
            chunk = file.read(h.block_size)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Check sha256 hash of a file against a checksum passed."
        " Doesn't print anything if they match."
        " Else prints 'Checksum doesn\'t match'."
    )
    parser.add_argument("file_name", help="name of file to calculate checksum")
    parser.add_argument("checksum", help="the checksum to check against")
    args = parser.parse_args()
    file_to_check = pathlib.Path(args.file_name)
    if file_to_check.is_file():
        try:
            assert get_digest(file_to_check) == args.checksum
        except AssertionError:
            print("Checksum doesn't match")
    else:
        raise Exception("{} file doesn't exists".format(args.file_name))
