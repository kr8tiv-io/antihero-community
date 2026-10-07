---
title: "MCP connector security review"
useItFor: "Check what an MCP server can actually touch before you connect it."
category: Prompts
goal: business
order: 709
---

Read this MCP server's code and docs: [repo link]. Before I connect it, tell me in plain English:
1. Every tool it exposes and what each one can read, change or delete.
2. What credentials it needs and where it stores them.
3. Anything it sends to outside servers.
4. The worst thing that could happen if my AI misuses it or gets tricked by a bad email or web page.
5. Settings to lock it down (read-only mode, scopes, approval steps).
Finish with: safe to use as-is, safe with changes (list them), or don't install.
