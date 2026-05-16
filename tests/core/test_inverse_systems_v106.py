from pytop.inverse_systems import inverse_limit, inverse_system


def test_inverse_system_descriptor_v106():
    system = inverse_system(["X0", "X1", "X2"], ["f01", "f12"])
    assert system["system_type"] == "inverse_system"
    assert system["space_count"] == 3
    assert system["bonding_map_count"] == 2
    assert system["is_chain_like"] is True
    assert system["version"] == "0.2.0"


def test_inverse_system_invalid_input_stays_none_v106():
    assert inverse_system(None, None) is None


def test_inverse_limit_descriptor_v106():
    system = inverse_system(["X0", "X1"], ["f01"])
    limit = inverse_limit(system)
    assert limit["limit_type"] == "inverse_limit"
    assert limit["space_count"] == 2
    assert "coherent tuples" in limit["carrier_hint"]
    assert limit["version"] == "0.2.0"


def test_inverse_limit_invalid_input_stays_none_v106():
    assert inverse_limit(None) is None
