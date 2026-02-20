# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    dut._log.info("Test counter behavior")
    # After reset, counter should be 0
    assert dut.uo_out.value == 0, f"Counter should be 0 after reset, got {dut.uo_out.value}"

    # Wait for one clock cycle - counter should increment to 1
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == 0, f"Counter should be 1 after first clock cycle, got {dut.uo_out.value}"

    # Wait for more clock cycles and verify counter increments
    await ClockCycles(dut.clk, 5)
    assert dut.uo_out.value == 5, f"Counter should be 6 after 6 clock cycles, got {dut.uo_out.value}"

    # Test counter continues to increment
    await ClockCycles(dut.clk, 10)
    assert dut.uo_out.value == 15, f"Counter should be 16 after 16 clock cycles, got {dut.uo_out.value}"
