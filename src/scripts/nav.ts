import { setSwapText } from "./cursor";
import {
  duration,
  ease,
  gsap,
  isMobile,
  prefersReducedMotion,
  stagger,
} from "./motion";

const DESKTOP = "(min-width: 1024px)";
const SCROLL_START = 80;

function initNav(): void {
  const header = document.querySelector<HTMLElement>("[data-header]");
  const scrim = document.querySelector<HTMLElement>("[data-header-scrim]");
  const button = document.querySelector<HTMLButtonElement>("[data-menu-button]");
  const label = document.querySelector<HTMLElement>("[data-menu-label]");
  const overlay = document.querySelector<HTMLElement>("[data-menu]");
  if (!header || !scrim || !button || !label || !overlay) return;
  if (header.dataset.ready === "true") return;
  header.dataset.ready = "true";

  const desktopQuery = window.matchMedia(DESKTOP);
  let open = false;
  let generation = 0;
  let lastY = window.scrollY;
  let ticking = false;
  let scrimShown = false;
  let headerHidden = false;

  const items = () =>
    [...overlay.querySelectorAll<HTMLElement>("[data-menu-item]")];

  const trapTargets = () => [button, ...items()];

  function motionDuration(kind: "fast" | "base"): number {
    if (prefersReducedMotion()) return 0;
    if (isMobile()) return duration.fast;
    return duration[kind];
  }

  function setExpanded(next: boolean): void {
    button.setAttribute("aria-expanded", next ? "true" : "false");
    setSwapText(label, next ? "Close" : "Menu");
    button.classList.toggle("is-open", next);
  }

  function showHeader(): void {
    if (!headerHidden) return;
    headerHidden = false;
    gsap.to(header, {
      yPercent: 0,
      duration: motionDuration("fast"),
      ease: ease.out,
      overwrite: "auto",
    });
  }

  function hideHeader(): void {
    if (headerHidden) return;
    headerHidden = true;
    gsap.to(header, {
      yPercent: -100,
      duration: motionDuration("fast"),
      ease: ease.out,
      overwrite: "auto",
    });
  }

  function paintScrim(on: boolean): void {
    if (on === scrimShown) return;
    scrimShown = on;
    gsap.to(scrim, {
      opacity: on ? 0.85 : 0,
      duration: motionDuration("fast"),
      ease: ease.out,
      overwrite: "auto",
    });
  }

  function applyScroll(): void {
    const y = window.scrollY;
    const scrolled = y > SCROLL_START;
    const goingDown = y > lastY + 6;
    const goingUp = y < lastY - 6;
    const nextScrim = scrolled && !open;
    header.classList.toggle("is-scrolled", nextScrim);
    paintScrim(nextScrim);

    const canHide = desktopQuery.matches && !open && y > SCROLL_START;
    if (canHide && goingDown) hideHeader();
    else if (!canHide || goingUp || y <= SCROLL_START) showHeader();

    lastY = y;
  }

  function onScroll(): void {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(() => {
      ticking = false;
      applyScroll();
    });
  }

  function finishClose(token: number): void {
    if (token !== generation || open) return;
    overlay.hidden = true;
    gsap.set(overlay, { autoAlpha: 0 });
  }

  function closeMenu(returnFocus: boolean): void {
    if (!open) return;
    open = false;
    const token = ++generation;
    setExpanded(false);
    document.documentElement.classList.remove("menu-open");
    gsap.killTweensOf(items());
    const fade = prefersReducedMotion() || desktopQuery.matches ? 0 : duration.fast;
    if (fade === 0) {
      finishClose(token);
    } else {
      gsap.to(overlay, {
        autoAlpha: 0,
        duration: fade,
        ease: ease.out,
        overwrite: "auto",
        onComplete: () => finishClose(token),
      });
    }
    if (returnFocus) button.focus();
    applyScroll();
  }

  function openMenu(): void {
    if (open || desktopQuery.matches) return;
    open = true;
    generation += 1;
    setExpanded(true);
    showHeader();
    gsap.killTweensOf(overlay);
    gsap.set(scrim, { opacity: 0 });
    scrimShown = false;
    header.classList.remove("is-scrolled");
    document.documentElement.classList.add("menu-open");
    overlay.hidden = false;
    const links = items();
    const reduced = prefersReducedMotion();
    // Opacity only. autoAlpha would set visibility:hidden and the first link could not take focus.
    gsap.set(overlay, { visibility: "visible", opacity: reduced ? 1 : 0 });
    if (reduced) {
      gsap.set(links, { y: 0, opacity: 1 });
    } else {
      const travel = isMobile() ? 16 : 40;
      gsap.to(overlay, {
        opacity: 1,
        duration: duration.fast,
        ease: ease.out,
        overwrite: "auto",
      });
      gsap.fromTo(
        links,
        { y: travel, opacity: 0 },
        {
          y: 0,
          opacity: 1,
          duration: motionDuration("base"),
          stagger,
          ease: ease.out,
          overwrite: "auto",
        },
      );
    }

    links[0]?.focus({ preventScroll: true });
  }

  function onKeydown(event: KeyboardEvent): void {
    if (!open) return;
    if (event.key === "Escape") {
      event.preventDefault();
      closeMenu(true);
      return;
    }
    if (event.key !== "Tab") return;

    const targets = trapTargets();
    if (targets.length === 0) return;
    const first = targets[0];
    const last = targets[targets.length - 1];
    const index = targets.indexOf(document.activeElement as HTMLElement);

    if (event.shiftKey) {
      if (index <= 0) {
        event.preventDefault();
        last.focus();
      }
      return;
    }

    if (index === -1 || index === targets.length - 1) {
      event.preventDefault();
      first.focus();
    }
  }

  function onClick(event: MouseEvent): void {
    const target = event.target;
    if (!(target instanceof Element)) return;
    const link = target.closest("a");
    if (!(link instanceof HTMLAnchorElement) || !overlay.contains(link)) return;
    const pathOf = (pathname: string) => pathname.replace(/\/$/, "") || "/";
    const leavesPage =
      link.target !== "_blank" &&
      link.origin === window.location.origin &&
      pathOf(link.pathname) !== pathOf(window.location.pathname);
    closeMenu(!leavesPage);
  }

  button.addEventListener("click", () => {
    if (open) closeMenu(true);
    else openMenu();
  });

  overlay.addEventListener("click", onClick);
  document.addEventListener("keydown", onKeydown);
  window.addEventListener("scroll", onScroll, { passive: true });
  desktopQuery.addEventListener("change", () => {
    if (desktopQuery.matches) closeMenu(false);
  });

  document.addEventListener(
    "touchmove",
    (event) => {
      if (!open) return;
      const list = overlay.querySelector("[data-menu-list]");
      if (event.target instanceof Node && list?.contains(event.target)) return;
      event.preventDefault();
    },
    { passive: false },
  );
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", initNav, { once: true });
} else {
  initNav();
}
