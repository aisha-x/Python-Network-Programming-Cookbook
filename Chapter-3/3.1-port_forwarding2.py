# this script is not from the book
# since asyncore library is not available in Python 3.6+ I wrote a modern version using asyncio library
# modern asyncio-based port forwarding proxy

import asyncio
import argparse

BUFFSIZE = 4096
async def handle_connection(local_reader, local_writer, remote_host, remote_port):

    try:
        remote_reader, remote_writer = await asyncio.open_connection(remote_host, remote_port)
        print("Connected to remote %s" % remote_host)

        async def forwarder(reader, writer):
            try:
                while True:

                    data = await reader.read(BUFFSIZE)
                    if not data:
                        break

                    writer.write(data)
                    await writer.drain()

            except ConnectionResetError:
                pass
            finally:
                if writer is not None:
                    writer.close()
                    await writer.close()

        # run bidirectional forwarder
        await asyncio.gather(
            forwarder(local_reader, remote_writer),
            forwarder(remote_reader, local_writer)
        )

    except Exception as e:
        print(f"Error: {e}")

    finally:
        if local_writer is not None:
            local_writer.close()
            await local_writer.wait_closed()

async def start_portForwarder(local_host, local_port, remote_host, remote_port):

    server = await asyncio.start_server(
        lambda r,w: handle_connection(r,w, remote_host, remote_port),
        host=local_host,
        port=local_port
    )

    addr = server.sockets[0].getsockname()
    print(f"Port forwarding: {addr} => {remote_host}:{remote_port}")
    async with server:
        await server.serve_forever()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="asyncio port forwarder")

    parser.add_argument('--local_host', type=str, default='localhost')
    parser.add_argument('--local_port', type=int, required=True)
    parser.add_argument('--remote_host', type=str, default='www.google.com')
    parser.add_argument('--remote_port', type=int, default=80)

    args = parser.parse_args()

    asyncio.run(start_portForwarder(
        args.local_host,
        args.local_port,
        args.remote_host,
        args.remote_port
    ))


# python3 3.1-port_forwarding2.py  --local_port 8080
# then open the browser and go to http://localhost:8080