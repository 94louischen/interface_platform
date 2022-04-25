
def read_file(file_dir, size=1024):
    with open(file_dir) as file:
        while True:
            content = file.read(size)
            if not content:
                break
            yield content
