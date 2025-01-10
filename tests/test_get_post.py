import pytest
from datastore.google_datastore import get_post

@pytest.mark.parametrize("post_id, expected", [
    (5669152601669632, "checking out the post"),
    ("5670392840585216", "My First Post")
])

def test_get_post(post_id, expected):
    result = get_post(post_id)["title"]
    assert result == expected

