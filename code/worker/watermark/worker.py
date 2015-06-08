import json
import logging
import os
import sys
from subprocess import call

import requests
from openstack import exceptions
from openstack.message.v1 import claim

import asyncio
from config import config as conf
import connect

logger = logging.getLogger(__name__)
tmp_dir = '/tmp/unwatermarked/'
tmp_dir_wm = '/tmp/watermarked/'

def save_file_locally(conn, filename):
    download = conn.object_store.get_object(filename, config.NAME)

    with open(tmp_dir + filename, "wb") as f:
        f.write(download)
        logger.debug('Saved file locally: %s' % os.path.abspath(f.name))


def watermark(filename):
    composite = [
        'composite',
        '-dissolve 50%',
        '-gravity south',
        'watermark.png',
        tmp_dir + filename,
        tmp_dir_wm + filename
    ]

    composite_cmd = " ".join(composite)

    # TODO: don't use shell=True
    call(composite_cmd, shell=True)

    logger.debug(os.path.dirname(os.path.realpath(__file__)))
    logger.debug("Watermarked image: %s" % composite_cmd)


def save_file_remotely(conn, filename):

    wm_filename = "wm-" + filename

    with open(tmp_dir_wm + filename, "rb") as f:
        conn.object_store.create_object(
            data=f.read(), name=wm_filename, container=config.NAME)

    logger.debug('Saved file remotely: {region}/{container}/{filename}'.format(
        region=config.OS_REGION_NAME,
        container=config.NAME,
        filename=wm_filename
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

    if not os.path.exists(tmp_dir_wm):
        os.makedirs(tmp_dir_wm)

    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s: %(name)s %(message)s')

    stdout = logging.StreamHandler(sys.stdout)
    stdout.setFormatter(formatter)
    logger.addHandler(stdout)

    file_handler = logging.FileHandler('wm_worker.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    logger.debug("Worker ready")

    try:
        event_loop()
    except Exception as e:
        logger.debug(e)
