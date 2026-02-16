# CRITICAL UPDATE: Parallel Needle Configuration Explained

## 🔌 Your ACTUAL Circuit Topology (Corrected)

```
+3 kV DC ----+----+----+----+----+----+----+
             |    |    |    |    |    |    |
           [R1] [R2] [R3] [R4] [R5] [R6] [R7]  ← 2 MΩ each
             |    |    |    |    |    |    |
             +----+----+----+----+----+----+---- Common HV Node
             |    |    |    |    |    |    |
           [C1] [C2] [C3] [C4] [C5] [C6] [C7]  ← 100 pF each
             |    |    |    |    |    |    |
           [C1] [C2] [C3] [C4] [C5] [C6] [C7]  ← 200 pF each
             |    |    |    |    |    |    |
             +----+----+----+----+----+----+---- GND


Needles connect PARALLEL to capacitors:

Common HV Node → Needle tip (sharp) → Air gap → GND
       ↑                                          ↑
       +------------------------------------------+
                (Parallel path to capacitors)
```

## ⚡ KEY INSIGHT: Needles in PARALLEL with Capacitors

**This is DIFFERENT from what I initially thought!**

During spark, **BOTH** paths conduct:
1. **Capacitor path**: C → Spark → GND
2. **Supply path**: +3kV → R → Spark → GND

They are **in parallel**, so currents ADD!

---

## 📊 Current Analysis (CORRECTED)

### During Charging (No Spark):
```
Current path: +3kV → R → C1,C2 → GND
Needle: Non-conducting (air gap open)

I_charging = (V_supply - V_cap) / R
           = (3kV - V_cap) / 2MΩ
           ≈ 0.9 mA average per needle
```

### During Spark (Breakdown):
```
TWO current sources in PARALLEL:

Source 1 - Capacitor discharge:
  Path: C → Spark → GND
  I_capacitor = V_breakdown / R_spark
              = 2.5 kV / 100 Ω
              = 25 mA (initial)
  
  Decays exponentially: τ = R_spark × C
                           = 100 Ω × 66.7 pF
                           = 6.67 ns

Source 2 - Supply through resistor:
  Path: +3kV → R → Spark → GND
  I_supply = V_supply / (R + R_spark)
           = 3 kV / (2 MΩ + 100 Ω)
           ≈ 3 kV / 2 MΩ
           = 1.5 mA (continuous)

TOTAL PEAK CURRENT:
  I_total = I_capacitor + I_supply
          = 25 + 1.5
          = 26.5 mA initially!
```

---

## 🔬 Why This Matters

### Old Understanding (WRONG):
- Spark current = V_cap / R_spark only
- Peak current ≈ 25 mA
- After capacitor empties, spark stops

### Corrected Understanding (RIGHT):
- Spark current = (V_cap / R_spark) + (V_supply / (R + R_spark))
- Peak current ≈ **26.5 mA** (6% higher!)
- After capacitor empties, current drops to **1.5 mA** from supply
- Spark may continue at low current or extinguish

---

## 📈 Time Evolution of Spark Current

```
    ^
    | 26.5 mA ___
    |          \  \___
    |           \     \___
I   |            \        \___  ← Capacitor depletes
    | 1.5 mA -----\___________\________ ← Supply current
    |              ↑           ↑
    |          Breakdown   Capacitor
    |                      empty
    +---------------------------------> t
         |←------ ~10 ns ----→|
```

**Phase 1** (0-10 ns): Both sources active
- Total current: 26.5 → ~1.5 mA
- Exponential decay as C empties

**Phase 2** (after 10 ns): Only supply source
- Current: 1.5 mA (limited by R)
- May sustain arc or spark extinguishes
- If continues, prevents capacitor from recharging!

---

## 🎯 Implications for Your Setup

### With 2 MΩ, 66.7 pF:

**Peak current**: 26.5 mA
- Capacitor: 25.0 mA (94%)
- Supply: 1.5 mA (6%)

**After capacitor empties**:
- Supply current: 1.5 mA
- Too low to sustain arc in most cases
- Spark extinguishes
- Capacitor recharges

### With 10 MΩ, 66.7 pF:

**Peak current**: 25.3 mA
- Capacitor: 25.0 mA (99%)
- Supply: 0.3 mA (1%)

**After capacitor empties**:
- Supply current: 0.3 mA
- Definitely too low to sustain
- Clean self-extinguishing behavior

---

## 💡 Why Parallel Configuration is Better

### Advantages:

1. **Higher peak power** for brief moment
   - Both sources contribute
   - Better plasma initiation

2. **Self-limiting duration**
   - Capacitor empties quickly
   - Supply current too low to sustain
   - Natural pulse termination

3. **Energy efficient**
   - Concentrated energy delivery
   - Short interaction time
   - Less thermal damage to electrodes

4. **Cleaner chemistry**
   - Intense short pulse
   - Better for specific reactions
   - Less heating of bulk gas

### vs Series Configuration (if needles were in series):

**Series would mean:**
- Only capacitor current during spark
- No supply contribution
- Lower peak current
- But same average charging current

**Parallel (your actual config) gives:**
- Capacitor + supply current
- Slightly higher peak
- Continuous path available (if arc sustains)

---

## 📊 Updated Calculations

### Your Configuration: 2 MΩ, 100+200 pF (66.7 pF)

```
CHARGING PHASE:
  Time constant: τ = 2 MΩ × 66.7 pF = 133 μs
  Charging time: t ≈ 1.79 × τ = 238 μs
  Frequency: f = 1/238μs = 4.2 kHz per needle
  
  Average current: ~0.9 mA per needle
  Total (7 needles): ~6.3 mA

SPARK DISCHARGE:
  Initial peak:
    I_capacitor = 2.5 kV / 100 Ω = 25.0 mA
    I_supply = 3 kV / 2.000 MΩ = 1.5 mA
    I_total = 26.5 mA ← PEAK
  
  Discharge time constant:
    τ_discharge = 100 Ω × 66.7 pF = 6.67 ns
  
  After ~30 ns (5τ):
    I_capacitor ≈ 0 mA (depleted)
    I_supply = 1.5 mA (continuous)
    Likely extinguishes

ENERGY PER SPARK:
  E = 0.5 × C × V²
    = 0.5 × 66.7 pF × (2.5 kV)²
    = 208 nJ per spark
```

---

## 🔄 Comparison: 2 MΩ vs 10 MΩ

| Parameter | 2 MΩ | 10 MΩ | Ratio |
|-----------|------|-------|-------|
| **Charging** |
| Time constant | 133 μs | 667 μs | 5× |
| Frequency | 4.2 kHz | 0.84 kHz | 5× |
| Avg current | 0.9 mA | 0.18 mA | 5× |
| **Spark** |
| Capacitor current | 25.0 mA | 25.0 mA | 1× |
| Supply current | 1.5 mA | 0.3 mA | 5× |
| **Peak total** | **26.5 mA** | **25.3 mA** | **1.05×** |
| Energy/spark | 208 nJ | 208 nJ | 1× |

**Key insight**: 
- Changing R affects supply contribution to spark
- But capacitor dominates (94-99%)
- So peak current barely changes!
- Main effect is on frequency and average current

---

## 🎓 Physical Interpretation

### Why Supply Current Matters (Even Though Small):

1. **Arc stability**
   - Sustains ionization path
   - May extend spark duration slightly
   - Affects chemistry

2. **Power delivery**
   - 1.5 mA at 3 kV = 4.5 W continuous
   - Can heat gas if arc persists
   - Usually too low to sustain, so spark ends

3. **Recharge prevention**
   - If arc doesn't extinguish
   - Supply current prevents capacitor recharge
   - System may latch (continuous glow)
   - Sharp needles usually prevent this

### With 2 MΩ:
- 1.5 mA supply current
- May briefly sustain arc (few ns extra)
- Still self-extinguishes
- Clean pulsing

### With 10 MΩ:
- 0.3 mA supply current
- Definitely cannot sustain arc
- Immediate extinguishing
- Cleaner pulsing (but slower)

---

## 🔧 Dashboard Updates

The updated dashboard now shows:

1. **Correct peak current calculation**
   - Displays both contributions
   - Shows total = capacitor + supply

2. **Current breakdown visualization**
   - Separate traces for each source
   - Combined total in bold

3. **Percentage contribution**
   - Shows capacitor dominance (94-99%)
   - Highlights supply role

4. **Circuit diagram updated**
   - Shows parallel configuration clearly
   - Explains dual current paths

---

## 📋 Summary

### Your Circuit (2 MΩ, 100+200 pF):

**Charging:**
- 4.2 kHz per needle
- 0.9 mA average per needle
- 6.3 mA total (7 needles)

**Spark:**
- Peak: **26.5 mA** (25.0 from C, 1.5 from supply)
- Duration: ~10-30 ns
- Energy: 208 nJ per spark

**Parallel configuration advantages:**
- Higher peak current (both sources)
- Self-limiting (C empties fast)
- Supply too weak to sustain arc
- Clean transient pulses

### Effect of Changing Components:

**C (100+100 → 100+200 pF):**
- Peak current: 26.5 mA (same path)
- Frequency: 5.6 → 4.2 kHz (slower)
- Energy: 156 → 208 nJ (higher)
- ✓ Fewer but stronger sparks

**R (2 → 10 MΩ):**
- Peak current: 26.5 → 25.3 mA (barely changes!)
- Supply contribution: 1.5 → 0.3 mA (5× lower)
- Frequency: 4.2 → 0.84 kHz (5× slower)
- Average current: 6.3 → 1.3 mA (5× lower)
- ✓ Much slower, lower power, but same spark intensity

---

**Bottom Line**: Your parallel needle configuration gives you the best of both worlds - intense capacitor discharge for chemistry, with minimal continuous current from the supply. The 2 MΩ gives ~6% boost to peak current from supply, while 10 MΩ makes it purely capacitor-driven (99%). Both work well for self-pulsing transient sparks!

---

**Created**: February 2026  
**For**: Srikar's 7-needle plasma research  
**Status**: Final corrected topology
