import pytest

from tools.utils import binary_json_decode, normalize, flatten


@pytest.mark.parametrize('max_msg_count', [10])
def test_message_published_with_proper_format(max_msg_count, config, kafka_consumer, run_publisher):
    msgs_count = 0
    monitoring_settings = config['test']['monitoring']
    pages = flatten([v.keys() for k, v in monitoring_settings.items()])
    hostnames = [normalize(k) for k, _ in monitoring_settings.items()]
    for message in kafka_consumer:
        msg = binary_json_decode(message.value)
        assert msg['ts']
        assert msg['hostname'] in hostnames
        assert msg['page'] in pages
        assert msg['status'] == 200
        assert msg['regex_valid'] in [True, False]
        msgs_count += 1
        if msgs_count > max_msg_count:
            break

