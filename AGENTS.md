# Agent and contributor contract

- Prefer `mncs-language` for implementation.
- State units, potential/model, cutoff, boundary conditions, timestep, precision and integration method explicitly.
- Validate force/energy kernels and conservation properties against trusted reference cases.
- Keep algorithmic meaning separate from CPU/GPU layout and scheduling choices.
- Deterministic/reproducible modes must define force-accumulation and reduction semantics.
- Record language/compiler/runtime pressure in `docs/LANGUAGE_PRESSURES.md`.
- Do not imply quantum-chemistry accuracy from classical molecular-dynamics foundations.
