import pytest

from tools.utils import binary_json_decode, normalize, flatten


@pytest.mark.parametrize('max_msg_count', [10])
def test_message_published_with_proper_format(max_msg_count, hostnames, pages, kafka_consumer, run_publisher):
    msgs_count = 0
    pages = flatten(list(pages.values()))
    for message in kafka_consumer:
        if msgs_count > max_msg_count:
            break
        msg = message.value
        assert msg['ts']
        assert msg['hostname'] in hostnames
        assert msg['page'] in pages
        assert msg['status'] == 200
        assert msg['regex_valid'] in [True, False]
        msgs_count += 1


