import base64
from openai import OpenAI
from keys import OPENAI_KEY

klient = OpenAI(
    api_key=OPENAI_KEY,
)

BASE64_LENGTH = 4

def lag_fil(fil):
    with fil as fil_innhold:
        resultat = klient.files.create(
            file=fil_innhold,
            purpose="vision",
        )
        return resultat.id


def base64_stream_encode(stream, chunk_size=4096):
    leftover = b""
    for chunk in iter(lambda: stream.read(chunk_size), b""):
        chunk = leftover + chunk
        full_len = (len(chunk) // 3) * 3
        to_encode, leftover = chunk[:full_len], chunk[full_len:]
        yield base64.b64encode(to_encode).decode("utf-8")
    if leftover:
        yield base64.b64encode(leftover).decode("utf-8")


def hent_avtale_fra_bilde(fil):

    fil_64 = "".join(base64_stream_encode(fil.stream))

    svar = klient.responses.create(
        model="gpt-5",
        service_tier="priority",
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_image",
                        "image_url": f"data:image/png;base64,{fil_64}",
                    },
                    {
                        "type": "input_text",
                        "text": """Du er en ekspert på å lese norske strømfakturaer. Ekstraher følgende fra fakturaen (tekst eller bilde):

                                - paaslag: Pris på påslaget i øre/kWh (kun tallet).
                                - maanedspris: Månedspris i kroner per måned (kun tallet).
                                - tillegstjenester: Sum av alle tillegg/ekstratjenester i kroner.
                                
                                Svar KUN med gyldig JSON på formatet:
                                {
                                  "paaslag": tall,
                                  "maanedspris": tall,
                                  "tillegstjenester": tall
                                }
                                
                                Bruk punktum som desimaltegn. Ikke ta med enheter. Hvis verdi mangler, bruk null.
                                Ikke legg til annen tekst enn JSON."""
                                
                    }
                ]
            }
        ]
    )

    return svar.output_text


def hent_avtale_fra_pdf(fil):

    fil_64 = "".join(base64_stream_encode(fil.stream))

    svar = klient.responses.create(
        model="gpt-5",
        service_tier="priority",
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_file",
                        "filename": "faktura.pdf",
                        "file_data": f"data:application/pdf;base64,{fil_64}",
                    },
                    {
                        "type": "input_text",
                        "text": """Du er en ekspert på å lese norske strømfakturaer. Ekstraher følgende fra fakturaen (tekst eller bilde):

                                - paaslag: Pris på påslaget i øre/kWh (kun tallet).
                                - maanedspris: Månedspris i kroner per måned (kun tallet).
                                - tillegstjenester: Sum av alle tillegg/ekstratjenester i kroner.

                                Svar KUN med gyldig JSON på formatet:
                                {
                                  "paaslag": tall,
                                  "maanedspris": tall,
                                  "tillegstjenester": tall
                                }

                                Bruk punktum som desimaltegn. Ikke ta med enheter. Hvis verdi mangler, bruk null.
                                Ikke legg til annen tekst enn JSON."""
                    }
                ]
            }
        ]
    )
    return svar.output_text

