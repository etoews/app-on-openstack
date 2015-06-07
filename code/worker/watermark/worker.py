import asyncio
import json
import uuid

import requests
from PIL import Image, ImageDraw

from openstack import exceptions
from openstack.message.v1 import claim

import connect

@asyncio.coroutine
def watermark(conn, message, href):
    download = conn.object_store.get_object(href, connect.NAME)
    file_in = open("/tmp/" + href, "r+b")
    file_in.write(download)
    file_in.flush()

    # credit: https://gist.github.com/snay2/876425
    main = Image.open(file_in)
    image = Image.new("RGBA", main.size)
    waterdraw = ImageDraw.ImageDraw(image, "RGBA")
    waterdraw.text((10, 10), "THANK YOU EVERYONE!")
    watermask = image.convert("L").point(lambda x: min(x, 200))
    image.putalpha(watermask)
    main.paste(image, None, image)

    file_out = open("/tmp/wm-" + href, "r+b")
    main.save(file_out)
    file_out.flush()
    file_out.seek(0)

    conn.object_store.create_object(data=file_out.read(),
                                    name="wm-" + href,
                                    container=connect.NAME)

    file_in.close()
    file_out.close()

def update_image(href):
    images_url = connect.API_URL + '/v1/images'
    headers = {'content-type': 'application/json'}
    requests.put(images_url, headers=headers, data=json.dumps({'href': "wm-" + href}))


@asyncio.coroutine
def worker():
    conn = connect.get_connection()
    client = str(uuid.uuid4())

    while True:
        try:
            messages = conn.message.claim_messages(claim.Claim.new(
                client=client, queue=connect.NAME, ttl=300, grace=150, limit=1))

            for message in messages:
                print(message)
                href = message.body['href']

                yield from watermark(conn, message, href)
                conn.message.delete_message(message)

                update_image(href)


        except exceptions.InvalidResponse as e:
            # An InvalidResponse is expected when there are no messages to claim
            pass

        yield from asyncio.sleep(5)

def event_loop():
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(worker())
    finally:
        loop.close()

if __name__ == '__main__':
    event_loop()
