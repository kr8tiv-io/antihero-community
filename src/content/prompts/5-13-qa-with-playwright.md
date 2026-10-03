---
title: "5.13 QA with Playwright"
useItFor: "Open every page in a real browser and catch what broke."
category: Websites
source: websites-on-autopilot
order: 18
---

[RULES]

TASK: QA pass
Install Playwright as a dev dependency. Write tests/qa.spec.ts that, for every page at 375px, 768px, 1440px and 1920px: loads the page, fails on any console error or 404, takes a full-page screenshot into /qa/screenshots, checks every internal link resolves, checks every image has alt text, and checks the menu opens and closes with the keyboard. Also run it once with reduced motion on. Run npm run build, then the tests. Fix anything you broke. Report what you fixed and anything you need me to decide. Confirm with git diff that the protected files are unchanged.
