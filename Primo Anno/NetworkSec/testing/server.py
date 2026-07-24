# server.py
import asyncio
from typing import Optional

from aioquic.asyncio import QuicConnectionProtocol, serve
from aioquic.h3.connection import H3_ALPN, H3Connection
from aioquic.h3.events import DataReceived, HeadersReceived
from aioquic.quic.configuration import QuicConfiguration
from aioquic.quic.events import ProtocolNegotiated, QuicEvent


HOST = "127.0.0.1"
PORT = 4433


class LoudH3Server(QuicConnectionProtocol):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._http: Optional[H3Connection] = None
        self._request_bodies: dict[int, bytearray] = {}
        self._responded_streams: set[int] = set()

    def connection_made(self, transport) -> None:
        super().connection_made(transport)
        print("[CONNECTION] QUIC UDP transport created")

    def quic_event_received(self, event: QuicEvent) -> None:
        print(f"[QUIC] Event received: {type(event).__name__}")

        if isinstance(event, ProtocolNegotiated):
            print(f"[QUIC] ALPN protocol negotiated: {event.alpn_protocol}")

            if event.alpn_protocol in H3_ALPN:
                self._http = H3Connection(self._quic)
                print("[HTTP/3] HTTP/3 connection initialized")
            else:
                print("[ERROR] Client did not negotiate HTTP/3")
                return

        if self._http is None:
            return

        for http_event in self._http.handle_event(event):
            print(
                f"[HTTP/3] Event received: "
                f"{type(http_event).__name__}"
            )

            if isinstance(http_event, HeadersReceived):
                self._handle_headers(http_event)

            elif isinstance(http_event, DataReceived):
                self._handle_data(http_event)

    def _handle_headers(self, event: HeadersReceived) -> None:
        headers = dict(event.headers)

        method = headers.get(
            b":method",
            b"UNKNOWN",
        ).decode(errors="replace")

        path = headers.get(
            b":path",
            b"UNKNOWN",
        ).decode(errors="replace")

        authority = headers.get(
            b":authority",
            b"UNKNOWN",
        ).decode(errors="replace")

        print(
            f"[REQUEST RECEIVED] "
            f"stream={event.stream_id} "
            f"method={method} "
            f"path={path} "
            f"authority={authority}"
        )

        self._request_bodies.setdefault(
            event.stream_id,
            bytearray(),
        )

        if event.stream_ended:
            print(
                f"[REQUEST COMPLETE] "
                f"stream={event.stream_id} "
                f"body_bytes=0"
            )
            self._send_response(event.stream_id)

    def _handle_data(self, event: DataReceived) -> None:
        body = self._request_bodies.setdefault(
            event.stream_id,
            bytearray(),
        )
        body.extend(event.data)

        print(
            f"[REQUEST DATA RECEIVED] "
            f"stream={event.stream_id} "
            f"chunk_bytes={len(event.data)} "
            f"total_body_bytes={len(body)}"
        )

        if event.stream_ended:
            print(
                f"[REQUEST COMPLETE] "
                f"stream={event.stream_id} "
                f"body_bytes={len(body)}"
            )
            self._send_response(event.stream_id)

    def _send_response(self, stream_id: int) -> None:
        if self._http is None:
            print(
                f"[ERROR] Cannot send response for stream "
                f"{stream_id}: HTTP/3 is not initialized"
            )
            return

        if stream_id in self._responded_streams:
            return

        self._responded_streams.add(stream_id)

        request_size = len(
            self._request_bodies.get(stream_id, b"")
        )

        response_body = (
            "HTTP/3 communication successful.\n"
            f"Stream: {stream_id}\n"
            f"Request body bytes: {request_size}\n"
        ).encode("utf-8")

        self._http.send_headers(
            stream_id=stream_id,
            headers=[
                (b":status", b"200"),
                (b"server", b"fake-quic-firewall-test"),
                (b"content-type", b"text/plain; charset=utf-8"),
                (
                    b"content-length",
                    str(len(response_body)).encode(),
                ),
            ],
            end_stream=False,
        )

        self._http.send_data(
            stream_id=stream_id,
            data=response_body,
            end_stream=True,
        )

        self.transmit()

        print(
            f"[RESPONSE SENT] "
            f"stream={stream_id} "
            f"status=200 "
            f"response_bytes={len(response_body)}"
        )


async def main() -> None:
    configuration = QuicConfiguration(is_client=False)
    configuration.alpn_protocols = H3_ALPN
    configuration.load_cert_chain(
        "ssl_cert.pem",
        "ssl_key.pem",
    )

    print(
        f"[SERVER STARTED] "
        f"HTTP/3 server listening on udp://{HOST}:{PORT}"
    )
    print("[SERVER STATUS] Waiting for HTTP/3 requests")

    await serve(
        HOST,
        PORT,
        configuration=configuration,
        create_protocol=LoudH3Server,
    )

    await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())