
"""
Extract email body
"""

from bs4 import BeautifulSoup


def extract_body(msg):

    plain_text = ""
    html_text = ""

    if msg.is_multipart():

        for part in msg.walk():

            content_type = (
                part.get_content_type()
            )

            disposition = str(
                part.get(
                    "Content-Disposition"
                )
            )

            if "attachment" in disposition:
                continue

            try:

                payload = part.get_payload(
                    decode=True
                )

                charset = (
                    part.get_content_charset()
                    or "utf-8"
                )

                text = payload.decode(
                    charset,
                    errors="ignore"
                )

            except:
                continue

            if content_type == "text/plain":

                plain_text += text

            elif content_type == "text/html":

                html_text += text

    else:

        payload = msg.get_payload(
            decode=True
        )

        charset = (
            msg.get_content_charset()
            or "utf-8"
        )

        plain_text = payload.decode(
            charset,
            errors="ignore"
        )

    if html_text and not plain_text:

        soup = BeautifulSoup(
            html_text,
            "lxml"
        )

        plain_text = soup.get_text()

    return {
        "plain": plain_text.strip(),
        "html": html_text,
    }
