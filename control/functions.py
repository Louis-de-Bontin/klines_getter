import os.path

def create_file(path, content):
    '''
    Create a new file, withe the full path (name included) and the content.
    '''
    if not os.path.isfile(path):
        with open(path, 'w') as f:
            f.write(content)