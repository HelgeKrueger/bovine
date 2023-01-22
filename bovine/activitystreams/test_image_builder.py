import json

import pytest
import rdflib


@pytest.mark.skip
def test_image_builder():
    image_dict = {
        "@context": [
            "https://www.w3.org/ns/activitystreams",
            {"schema": "https://schema.org#"},
        ],
        "type": "Image",
        "name": "Cat Jumping on Wagon",
        "url": [
            {
                "@context": "https://www.w3.org/ns/activitystreams",
                "type": "Link",
                "href": "http://example.org/image.jpeg",
                "mediaType": "image/jpeg",
            },
            {
                "@context": "https://www.w3.org/ns/activitystreams",
                "type": "Link",
                "href": "http://example.org/image.png",
                "mediaType": "image/png",
            },
        ],
        "schema:license": "https://www.w3.org/Consortium/Legal/2015/copyright-software-and-document",
        "schema:creator": "James M Snell, IBM; Evan Prodromou, Fuzzy.ai",
        "schema:isBasedOnUrl": "https://www.w3.org/TR/activitystreams-vocabulary/#dfn-image",
    }
    G = rdflib.Graph()
    G.parse(data=json.dumps(image_dict), format="json-ld")

    print(
        G.serialize(
            format="json-ld",
            auto_compact=True,
            context="https://www.w3.org/ns/activitystreams",
            # use_rdf_types=True,
            # use_native_types=True,
        )
    )
