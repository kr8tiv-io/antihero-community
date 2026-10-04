# Put AntiHero AI on Hostinger

Do this from your own computer when you are ready. Nothing in this repo uploads, connects, or deploys by itself.

You upload the contents of `dist/`. That folder is a finished static site: each page is a folder with `index.html`, images and scripts have hashed names under `_astro/`, and there is no server to run.

## Before you build

Two values are baked into the HTML at build time. Change them, then build again. Editing them on the server later does nothing.

1. Domain. Open `src/data/site.ts` and set `SITE_URL` to the real origin, including `https://`. That constant is the only copy. `astro.config.mjs` imports it. The current value is `https://antiheroai.com`. Confirm that is the domain you actually own.
2. Mailchimp. In Mailchimp, open the embedded form for the audience. Copy the form `action` URL. It starts with `https://` and contains `list-manage.com`. Put it in a file named `.env` in the project folder:

```
MAILCHIMP_FORM_ACTION=https://YOUR-SERVER.list-manage.com/subscribe/post?u=YOUR_U&id=YOUR_ID
```

Copy `.env.example` to `.env` first if you do not have that file yet. `.env` stays on your machine. It is not part of the upload.

In the same embed code, find the hidden input whose name looks like `b_0123abc_4567def`. Open `src/components/EmailForm.astro` and replace `b_TODO_TODO` with that exact name. Until you do, the email field on the site stays closed and the group link stands in for it.

`public/.htaccess` sends `www` to the bare domain (so `www.antiheroai.com` becomes `antiheroai.com`) and forces HTTPS. Confirm that is the host you want. If you want `www` to be the real site, say so before upload and the two rewrite rules get flipped.

## Build

From the project folder:

```
npm install
npm run build
```

Check the build on your machine. This project uses port 4330. Port 4321 belongs to another project on this PC. Do not use it.

```
npx astro preview --port 4330 --host localhost
```

Open `http://localhost:4330`. Click through Home, Guides, Prompts, Videos, Blog, About, Join, and Credits. Open a nonsense address such as `http://localhost:4330/not-a-page` and confirm the missing page, with links to Home and Guides. Preview does not apply `.htaccess`. HTTPS and the www redirect show up only after Hostinger is serving the files.

## Upload with File Manager

1. Log in to Hostinger hPanel.
2. Open Websites, then Manage on this domain, then File Manager.
3. Open `public_html`. That folder is the site root.
4. If Hostinger left a default page there, move it into a folder named `_old-hostinger`. Leave it until the new site is up. Do not upload the project on top of a default `index.html` and hope.
5. Upload the contents of `dist/`, not the `dist` folder itself. `index.html` and `.htaccess` sit directly inside `public_html`. So do the folders `_astro`, `fonts`, `media`, `guides`, `about`, and the rest.
6. File Manager often hides dotfiles. Turn on hidden files, or the site will go up without `.htaccess` and you will not get the 404 page, the cache rules, or the www redirect. If you cannot see `.htaccess` after upload, use FTP for that one file.
7. Do not upload `node_modules`, `src`, `.env`, or the rest of the project.

## Upload with FTP

1. In hPanel, open FTP accounts and note the host, username, and password.
2. Connect with an FTP client. Use port 21, or the port hPanel prints. If the transfer stalls, switch to passive mode.
3. Open `public_html` on the server.
4. Upload everything inside `dist/` into `public_html`. Include `.htaccess`.
5. Same rule as File Manager: the contents, not a nested `dist` folder, and not the source project.

## After it is up

Visit `https://` plus your bare domain. Then visit `http://` and `https://www.` and confirm both land on the bare `https://` host. Visit a bad path and confirm the missing page. Send one test address through the email form only after the Mailchimp action and bot field are real.

Replacing a file under `/fonts/` or `/media/` without changing its name can stay cached for a year. Hashed files in `/_astro/` are safe to cache, because a new build changes the name. HTML is cached for 5 minutes.

If the host answers with a 500 after upload, the first place to look is `public/.htaccess`. Some plans reject `Options -Indexes`. Remove that one line, rebuild, and upload `.htaccess` again.

## Pre-launch checklist

- [ ] `SITE_URL` in `src/data/site.ts` is the real domain, then you built again.
- [ ] `MAILCHIMP_FORM_ACTION` is the real https action, and `b_TODO_TODO` in `src/components/EmailForm.astro` is the real bot-field name, then you built again.
- [ ] `public/.htaccess` sends www where you actually want it.
- [ ] The PDFs in `public/guides` are the real guides. Two filenames are still stand-ins: `todo-older-live-1.pdf` and `todo-older-live-2.pdf`.
- [ ] The files in `public/media` are the real stills and video. Matching stand-in covers: `public/media/covers/todo-older-live-1.jpg` and `todo-older-live-2.jpg`.
- [ ] Every TODO below is either done or a line you have chosen to ship.
- [ ] You uploaded only the contents of `dist/`.
- [ ] Home, Guides, a guide, Prompts, the copy button, Videos, Blog, About, Join, Credits, and a bad URL all look right on a phone.

## Every TODO

Searched the project for `TODO` on 3 October 2026, skipping `node_modules`, `dist`, `.astro`, and local browser output. These are the hits.

Site copy and config still open:

- `src/data/site.ts` line 2. Confirm the real domain.
- `astro.config.mjs` line 10. Same domain note. The value lives in `site.ts`.
- `README.md` line 32. Same domain note.
- `public/.htaccess` line 2. Confirm bare domain versus www.
- `src/components/EmailForm.astro` line 12 and line 13. Replace `b_TODO_TODO` with the Mailchimp bot-field name.
- `src/components/JoinBand.astro` line 48. Matt confirms each line is true before launch.
- `src/pages/about.astro` line 68. Matt reviews this copy.
- `src/pages/about.astro` line 76. Matt writes the first-person note.
- `src/pages/join.astro` line 98. Matt confirms each line.
- `src/content/blog/why-we-built-this-site-live.md` line 3, line 9, line 11, and line 13. The post is still a draft, so it is not a public page yet.
- `src/content/videos/websites-on-autopilot-live.md` line 4 and line 9. YouTube id, duration, and poster.
- `src/content/videos/build-a-brand-from-scratch-live.md` line 4 and line 9. Same.
- `src/content/guides/websites-on-autopilot.md` line 17. Cover image still marked TODO.
- `src/content/guides/build-a-brand-from-scratch-with-ai.md` line 17. Cover image still marked TODO.

Code that treats the word as empty, not a missing page:

- `src/pages/guides/[slug].astro` line 55. A related value of `TODO` is skipped.

Prompt text. These lines are the words you copy into a build. They are not unfinished pages on this site:

- `src/content/prompts/copy-pass.md` line 3 and line 12.
- `src/content/prompts/9-1-the-no-slop-rules-written-for-the-ai-not-for-you.md` line 9.
- `brand-kit/prompt-guide.md` line 337 and line 392.
