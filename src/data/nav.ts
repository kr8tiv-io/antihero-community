export const facebookGroupUrl = "https://www.facebook.com/groups/antiheroai";

export interface NavLink {
  href: string;
  label: string;
  caption: string;
}

/** Desktop bar. Join and Credits stay off this row on purpose. */
export const desktopLinks: NavLink[] = [
  { href: "/guides", label: "Guides", caption: "Guides / read them, steal them" },
  { href: "/prompts", label: "Prompts", caption: "Prompts / copy, paste, done" },
  { href: "/videos", label: "Videos", caption: "Videos / every live" },
  { href: "/blog", label: "Blog", caption: "Blog / notes from the trenches" },
  { href: "/about", label: "About", caption: "About / why this exists" },
];

/** Full-screen menu. Join is the internal page. The red button is the group. */
export const menuLinks: NavLink[] = [
  ...desktopLinks,
  { href: "/join", label: "Join", caption: "Join / the good part" },
];

export function normalizePath(pathname: string): string {
  if (pathname.length > 1 && pathname.endsWith("/")) return pathname.slice(0, -1);
  return pathname || "/";
}

export function isCurrentPath(href: string, pathname: string): boolean {
  return normalizePath(href) === normalizePath(pathname);
}
