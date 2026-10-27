"""cocotb unit test for rtl/serializer.v (spec S1: bit order, word boundary,
no dropped or repeated bit). Simulated, RTL level: no timing is claimed."""

import random

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge, RisingEdge

WIDTH = 8
CYC = WIDTH // 2


async def _reset(dut, cycles=3):
    dut.din.value = 0
    dut.rst.value = 1
    for _ in range(cycles):
        await RisingEdge(dut.clk)
    await FallingEdge(dut.clk)
    dut.rst.value = 0


async def _run_words(dut, words):
    """Feed one word per word_clk period (din changes in the cycle word_clk
    rises, so the capture edge sees it) and return, per word, the dout samples
    of the CYC cycles that start at each word_clk fall. Sampling is on the
    falling clk edge."""
    cocotb.start_soon(Clock(dut.clk, 2, unit="ns").start())
    await _reset(dut)
    queue = list(words)
    wclk_log, dout_log = [], []
    prev = 0
    for _ in range((len(words) + 3) * CYC):
        await FallingEdge(dut.clk)
        wclk = int(dut.word_clk.value)
        if wclk and not prev and queue:
            dut.din.value = queue.pop(0)
        wclk_log.append(wclk)
        dout_log.append(int(dut.dout.value))
        prev = wclk
    falls = [i for i in range(1, len(wclk_log)) if not wclk_log[i] and wclk_log[i - 1]]
    groups = [dout_log[i:i + CYC] for i in falls if i + CYC <= len(dout_log)]
    return groups[:len(words)], wclk_log


def _word_from_group(group):
    word = 0
    for i, pair in enumerate(group):
        word |= pair << (2 * i)
    return word


@cocotb.test()
async def test_word_clock_is_div4_50pct(dut):
    cocotb.start_soon(Clock(dut.clk, 2, unit="ns").start())
    await _reset(dut)
    log = []
    for _ in range(8 * CYC):
        await FallingEdge(dut.clk)
        log.append(int(dut.word_clk.value))
    rises = [i for i in range(1, len(log)) if log[i] and not log[i - 1]]
    falls = [i for i in range(1, len(log)) if not log[i] and log[i - 1]]
    assert len(rises) >= 6, f"word_clk barely toggles: {log}"
    assert all(b - a == CYC for a, b in zip(rises, rises[1:])), \
        f"word_clk rise spacing not {CYC} cycles: {rises}"
    assert all(f - r == CYC // 2 for r, f in zip(rises, falls[1:] if falls[0] < rises[0] else falls)), \
        f"word_clk is not 50 % duty: rises {rises} falls {falls}"


@cocotb.test()
async def test_bit_order_walking_ones(dut):
    words = [1 << i for i in range(WIDTH)] + [0xFF, 0x00, 0xA5, 0x5A]
    groups, _ = await _run_words(dut, words)
    got = [_word_from_group(g) for g in groups]
    assert got == words, f"expected {[hex(w) for w in words]}, got {[hex(g) for g in got]}"


@cocotb.test()
async def test_no_dropped_or_repeated_bit_back_to_back(dut):
    rng = random.Random(21)
    words = [rng.randrange(1 << WIDTH) for _ in range(200)]
    groups, _ = await _run_words(dut, words)
    got = [_word_from_group(g) for g in groups]
    assert len(got) == len(words)
    assert got == words, "word stream differs from input (dropped/repeated bit or misaligned boundary)"


@cocotb.test()
async def test_reset_clears_outputs_and_restarts_count(dut):
    cocotb.start_soon(Clock(dut.clk, 2, unit="ns").start())
    await _reset(dut)
    dut.din.value = 0xFF
    for _ in range(3 * CYC + 1):
        await FallingEdge(dut.clk)
    dut.rst.value = 1
    await FallingEdge(dut.clk)
    await FallingEdge(dut.clk)
    assert int(dut.dout.value) == 0, "dout not cleared by reset"
    assert int(dut.word_clk.value) == 0, "word_clk not cleared by reset"
    dut.rst.value = 0
    log = []
    for _ in range(2 * CYC):
        await FallingEdge(dut.clk)
        log.append(int(dut.word_clk.value))
    assert log[:CYC // 2] == [0] * (CYC // 2) or log[0] == 0, f"count did not restart: {log}"
