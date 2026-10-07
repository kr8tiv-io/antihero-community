---
title: "Safe dependency check-up"
useItFor: "Update packages without waking up to a broken site."
category: Websites
goal: grok-build
order: 206
---

[RULES]

TASK: Dependency check-up, safe updates only
Run the package manager's outdated and audit commands. Sort what you find into three groups: security fixes, safe patch/minor updates, and major updates that could break things.
Apply only the first two groups. Run the build and the tests after. If anything breaks, roll that one package back and note it. Don't touch major versions; list them with what would need to change. One commit: "Safe dependency updates".
