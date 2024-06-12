import os
import sys


def rename_files_with_padded_index(directory):
    # Get list of files in the directory
    files = [
        file for file in os.listdir(directory)
        if not file.endswith('.py')
        and os.path.isfile(os.path.join(directory, file))
    ]

    # Calculate the total number of digits needed for the highest index
    num_files = len(files)
    num_digits = len(str(num_files))

    # Iterate over each file and rename it with a zero-padded index
    for index, filename in enumerate(files):
        # Construct zero-padded index
        padded_index = str(index + 1).zfill(num_digits)

        # Construct new filename with padded index
        new_filename = f"{padded_index}.json"

        # Rename the file
        os.rename(
            os.path.join(directory, filename),
            os.path.join(directory, new_filename)
        )


if __name__ == '__main__':
    DIRPATH = sys.argv[1]
    rename_files_with_padded_index(DIRPATH)
