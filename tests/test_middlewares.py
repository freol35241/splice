import time
import skarv
from skarv.middlewares import throttle

import pytest


def test_throttle_middleware():

    count = 0

    @skarv.subscribe("throttled")
    def callback(_):
        nonlocal count
        count += 1

    skarv.register_middleware("throttled", throttle(at_most_every=0.1))

    start = time.time()

    # Publish at 100Hz during a second
    while time.time() - start < 1:
        skarv.put("throttled", 42)
        time.sleep(0.01)

    # It should still only have 10 invocations
    assert count == 10
