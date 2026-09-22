# SARATH-ASIC

**M.Tech VLSI · RTL Design · SystemVerilog · Design Verification**

> **BUILD → SIMULATE → ASSERT → COVER → VERIFY**

<!-- PROFILE:START -->
> Profile data has not been generated yet. Run `python scripts/generate_profile.py`, or let GitHub Actions generate it.
<!-- PROFILE:END -->

## Engineering Direction

My current engineering focus is building depth in **RTL design and Design Verification**, with SystemVerilog as the main verification language and increasing focus on memory and interconnect architecture.

### Current Focus

- SystemVerilog RTL and verification
- SystemVerilog Assertions (SVA)
- Temporal properties and assertion-based verification
- Functional coverage
- Layered testbench architecture
- Memory verification
- CXL.mem and memory-expansion concepts
- LPDDR5X / high-bandwidth memory architecture
- Progression from SystemVerilog verification toward UVM

### Verification Concepts

```text
SystemVerilog
├── RTL
├── Testbench Architecture
├── Assertions
│   ├── Immediate / Concurrent Assertions
│   ├── Sequences / Properties
│   ├── |-> / |=>
│   ├── ## temporal delays
│   ├── $past / $rose / $fell / $stable
│   └── disable iff
└── Functional Coverage
    ├── covergroup
    ├── coverpoint
    ├── bins
    ├── illegal_bins
    └── cross coverage
```

### Architecture Interests

```text
Memory & Interconnect
├── CXL
│   └── CXL.mem
│       ├── Memory expansion
│       ├── Host/device memory interaction
│       └── Memory hierarchy
└── LPDDR5X
    ├── Memory architecture
    ├── Controller concepts
    └── Verification considerations
```

## Verification Philosophy

> **Don't only check whether the design produces the expected output. Define what must always be true, exercise meaningful scenarios, and collect evidence that the intended behavior was explored.**

The generated section is evidence-driven: repository activity, languages, detected technologies, and recent commits are generated automatically. Subjective skill percentages are intentionally avoided.

## Connect

- GitHub: [Sarath-ASIC](https://github.com/Sarath-ASIC)

<!-- PROFILE:END -->
