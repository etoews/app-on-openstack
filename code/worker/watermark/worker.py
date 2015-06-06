import asyncio
import tempfile
import uuid

from openstack import exceptions
from openstack.message.v1 import claim

import connect

@asyncio.coroutine
def watermark(conn, message):
    print('Watermark image %s' % message)
    href = message.body['href']

    with tempfile.TemporaryFile() as f:
        download = conn.object_store.get_object(href, connect.NAME)
        f.write(download)
        f.flush()


@asyncio.coroutine
def worker():
    conn = connect.get_connection()
    client = str(uuid.uuid4())

    while True:
        print('Check queue for work')

        try:
            messages = conn.message.claim_messages(claim.Claim.new(
                client=client, queue=connect.NAME, ttl=300, grace=150))

            for message in messages:
                yield from watermark(conn, message)
                conn.message.delete_message(message)

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
