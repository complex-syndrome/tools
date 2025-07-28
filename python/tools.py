import os

# Make multiple directories with no errors
def mkdirs(*dirs): 
    for d in dirs:
        os.makedirs(d, exist_ok=True)


def file_is_empty(file: str) -> bool:
    return not os.path.exists(file) or os.path.getsize(file) == 0