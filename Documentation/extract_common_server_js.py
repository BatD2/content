import sys
import yaml

<<<<<<< HEAD

def readFile(filepath):
    with open(filepath, 'r') as f:
        out = yaml.safe_load(f)
        return out
    return []


def main(argv):
    # create commonServer js file to extract doc from
    commonServer = readFile('./Packs/Base/Scripts/script-CommonServer.yml')
=======
def readFile(filepath):
    with open(filepath, 'r') as f:
        out = yaml.load(f)
        return out
    return []

def main(argv):
    # create commonServer js file to extract doc from
    commonServer = readFile('./Scripts/script-CommonServer.yml')
>>>>>>> 9796c09436b0e20b9c2496c40e737b4d4922bc07
    jsScript = commonServer.get("script", "")
    with open('./Documentation/commonServerJsDoc.js', 'w') as fp:
        fp.write(jsScript)


if __name__ == "__main__":
    main(sys.argv[1:])
