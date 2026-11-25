def read_packages(path):
    packages = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            name, assign, version = line.partition('==')
            clean_name = name.replace("\x00", "").strip()
            clean_version = version.replace("\x00", "").strip()

            packages.append({'name' : clean_name, 'version' : clean_version})
    return packages
