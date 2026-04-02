# GitHub Announcement

I upgraded `one-person-company-os` again.

The previous V2 release already shifted the product from a startup manual to a round-based company OS.
This patch makes the runtime and delivery behavior much more trustworthy.

It now reports exactly where it is in the flow, whether outputs were really saved, and what to do when the local Python environment is not compatible.

The system remains Chinese-first for Chinese users, including workspace names, role names, and day-to-day operating language.

This release includes:

- fixed `Step 1/5 -> Step 5/5` progress reporting
- explicit save status and runtime status in the workflow output
- a new preflight command for environment checks and mode selection
- a checkpoint save command for real operating handoffs
- a Python runtime recovery command that prefers OpenClaw-managed recovery
- rewritten README and release copy aimed at founders actively building AI-native solo companies
