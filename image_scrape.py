import html
import json
import re
import shutil
import sys

from pathlib import Path

import requests


def main(url):
    content = requests.get(url).content.decode()
    gallery = json.loads(
        html.unescape(
            re.search(f'<div data-gallery-items="(\[[^\]]*\])" ', content)[1]
        )
    )

    path = "./images/" + re.sub(r'http.*:\/\/', '', url).replace('/', '_')
    Path(path).mkdir(parents=True, exist_ok=True)

    for item in gallery:
        image_url = item['large']['url'].split('?')[0]
        image_filename = image_url.split('/')[-1]

        r = requests.get(image_url, stream=True)
        print(f'getting {image_url}')
        if r.status_code == 200:
            with open(f'{path}/{image_filename}', 'wb') as of:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, of)


if __name__ == '__main__':
    main(sys.argv[1])
