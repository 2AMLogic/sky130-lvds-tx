"""Smoke test for the cold-start harness: a free-running counter."""

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge


async def _start(dut):
    cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())
    dut.rst.value = 1
    for _ in range(2):
        await RisingEdge(dut.clk)
    dut.rst.value = 0
    await RisingEdge(dut.clk)


@cocotb.test()
async def test_reset_clears_count(dut):
    await _start(dut)
    dut.rst.value = 1
    await RisingEdge(dut.clk)
    await RisingEdge(dut.clk)
    assert dut.count.value == 0


@cocotb.test()
async def test_counts_by_one(dut):
    await _start(dut)
    prev = int(dut.count.value)
    for _ in range(20):
        await RisingEdge(dut.clk)
        cur = int(dut.count.value)
        assert cur == (prev + 1) % 16, f"count went {prev} -> {cur}, expected +1"
        prev = cur
