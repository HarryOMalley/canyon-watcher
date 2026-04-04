from domain.enums import StockState


def test_stock_state_values():
    assert StockState.IN_STOCK.value == "IN_STOCK"
    assert StockState.LOW_STOCK.value == "LOW_STOCK"
    assert StockState.COMING_SOON.value == "COMING_SOON"
    assert StockState.NOTIFY_ME.value == "NOTIFY_ME"
    assert StockState.UNAVAILABLE.value == "UNAVAILABLE"
    assert StockState.CONFIG_MISMATCH.value == "CONFIG_MISMATCH"
    assert StockState.BLOCKED.value == "BLOCKED"
    assert StockState.FETCH_FAILED.value == "FETCH_FAILED"
