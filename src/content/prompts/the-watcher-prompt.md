---
title: "The watcher prompt"
useItFor: "Hand each commit to a second AI and ask if the task is actually done."
category: Websites
source: websites-on-autopilot
order: 21
---

You're my build supervisor. Here is the full build package: [attach it]. Grok Build is running these prompts one at a time in my project. After each one I'll paste its final report and the output of `git show --stat HEAD` (and the diff if it's small).

For each step tell me:
1. Done or not done, against the TASK's own definition of done.
2. Did it touch anything the RULES protect? Name the file.
3. Any RULES broken (banned words, em dashes, wrong colors, missing credits entry, deploys, deleted files).
4. What to look at on localhost before moving on.
5. If something is wrong: the exact fix prompt to paste back into Grok Build, with the RULES paragraph on top.
Then give me the next prompt number. Keep it short.
