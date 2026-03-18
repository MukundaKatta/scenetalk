"""Tests for Scenetalk."""
from src.core import Scenetalk
def test_init(): assert Scenetalk().get_stats()["ops"] == 0
def test_op(): c = Scenetalk(); c.generate(x=1); assert c.get_stats()["ops"] == 1
def test_multi(): c = Scenetalk(); [c.generate() for _ in range(5)]; assert c.get_stats()["ops"] == 5
def test_reset(): c = Scenetalk(); c.generate(); c.reset(); assert c.get_stats()["ops"] == 0
def test_service_name(): c = Scenetalk(); r = c.generate(); assert r["service"] == "scenetalk"
