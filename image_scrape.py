import json, requests, shutil

from pathlib import Path
Path("./images").mkdir(parents=True, exist_ok=True)

def main():
    with open('data.json') as f:
        json_data = json.load(f)
        for item in json_data['RelaProperty']['imageListPS']:
            url = item['url']
            filename = url.split('/')[-1]
            r = requests.get(url, stream=True)
            print(f'getting {url}')
            if r.status_code == 200:
                with open(f'images/{filename}', 'wb') as of:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, of)

if __name__ == '__main__':
    main()
