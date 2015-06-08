import json
import logging
import os
import sys

import requests
from PIL import Image, ImageDraw
from openstack import exceptions
from openstack.message.v1 import claim

import asyncio
from config import config as conf
import connect

logger = logging.getLogger(__name__)
tmp_dir = '/tmp/worker/'
tmp_dir_wm = '/tmp/worker/wm-'

def save_file_locally(conn, filename):
    download = conn.object_store.get_object(filename, config.NAME)

    with open(tmp_dir + filename, "wb") as f:
        f.write(download)
        logger.debug('Saved file locally: %s' % os.path.abspath(f.name))


def watermark(filename):
    # credit: https://gist.github.com/snay2/876425
    main = Image.open(open(tmp_dir + filename, "rb"))
    image = Image.new("RGBA", main.size)
    waterdraw = ImageDraw.ImageDraw(image, "RGBA")
    waterdraw.text((10, 10), "THANK YOU EVERYONE!")
    watermask = image.convert("L").point(lambda x: min(x, 200))
    image.putalpha(watermask)
    main.paste(image, None, image)

    with open(tmp_dir_wm + filename, "wb") as f:
        main.save(f)
        logger.debug("Watermarked image: %s" % os.path.abspath(f.name))


def save_file_remotely(conn, filename):

    with open(tmp_dir_wm + filename, "rb") as f:
        conn.object_store.create_object(
            data=f.read(), name="wm-" + filename, container=config.NAME)

    logger.debug('Saved file remotely: {region}/{container}/{filename}'.format(
        region=config.OS_REGION_NAME,
        container=config.NAME,
        filename=filename
    ))


def update_image(filename):
    images_url = config.API_URL + '/v1/images'
    headers = {'content-type': 'application/json'}
    message = json.dumps({'filename': "wm-" + filename})
    requests.put(images_url, headers=headers, data=message)

    logger.debug("Updated image: %s" % message)


@asyncio.coroutine
def worker():
    conn = connect.get_connection(config)

    while True:
        try:
            messages = conn.message.claim_messages(claim.Claim.new(
                client=config.CLIENT, queue=config.NAME, ttl=300, grace=60, limit=1))

            for message in messages:
                logger.debug("Claimed message: %s" % message)
                filename = json.loads(message.body)['filename']

                save_file_locally(conn, filename)
                watermark(filename)
                save_file_remotely(conn, filename)
                update_image(filename)

                conn.message.delete_message(message)
                logger.debug("Deleted message: %s" % message)
        except exceptions.InvalidResponse:
            # An InvalidResponse is expected when there are no messages to claim :/
            pass

        yield from asyncio.sleep(5)


def event_loop():
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(worker())
    finally:
        loop.close()


if __name__ == '__main__':
    config_name = os.getenv('WM_CONFIG_ENV') or 'default'
    config = conf[config_name]()

    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)

    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s: %(name)s %(message)s')

    stdout = logging.StreamHandler(sys.stdout)
    stdout.setFormatter(formatter)
    logger.addHandler(stdout)

    file_handler = logging.FileHandler('/root/wm_worker.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    event_loop()
