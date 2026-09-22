# Setup

## 1. Repository

Use your public GitHub profile repository:

`Sarath-ASIC`

## 2. Copy the files

Keep this structure:

```text
README.md
profile.yml
scripts/generate_profile.py
profile-data/profile-data.json
.github/workflows/update-profile.yml
```

## 3. Edit `profile.yml`

Only the human-maintained focus and learning lists normally need editing.

The profile currently emphasizes:

- SystemVerilog
- SVA
- functional coverage
- layered testbenches
- memory verification
- CXL.mem
- LPDDR5X
- UVM progression

## 4. Push to GitHub

After pushing, open:

**Actions → Update Engineering Profile → Run workflow**

The workflow then refreshes automatically every 12 hours.

## What updates automatically?

- public repository count
- followers
- repository languages
- detected SystemVerilog/SVA/UVM/CXL/LPDDR5X evidence
- recent public commits
- active repositories
- repository stars
- last-update times

The generator does not assign skill percentages or claim proficiency from keywords.

## Why no FPGA section?

FPGA/SmartFusion2/Vivado/Libero work is intentionally not part of the current profile identity. Those repositories can remain on GitHub; they are simply not highlighted here.
