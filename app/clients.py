import requests

def pypi(name):
    base_url = f"https://pypi.org/pypi/{name}/json"
    response = requests.get(base_url)

    if response.status_code == 200:
        data = response.json()
        files = data["urls"]
        return {"name" : name, "latest_version" : data["info"]["version"],
                "license" : data["info"]["license"] or "UNKNOWN",
                "last_release" : files[0]["upload_time_iso_8601"]
        }
    else:
        return f"Failed to retrieve data{response.status_code}"

package = 'requests'
pack_info = pypi(package)

if __name__ == "__main__":
    print(pypi('requests'))