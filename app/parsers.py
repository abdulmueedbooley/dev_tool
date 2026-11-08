def read_packages(path):
    packages = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            name, assign, version = line.partition('==')
            packages.append({'name' : name, 'version' : version})
    return packages

path = 'C:/Users/abdul/Documents/GitHub/upstream/requirements.txt'