import { gsap, ScrollTrigger, onReducedMotionChange, prefersReducedMotion } from "./motion";

type Kind = "desktop" | "mobile";
type Mode = "still" | "video" | "frames";

interface FrameManifest {
  count: number;
  first: number;
  pad: number;
  ext: string;
}

interface NetworkInformation {
  saveData?: boolean;
  effectiveType?: string;
}

const DESKTOP_QUERY = "(min-width: 768px)";
const FINE_QUERY = "(hover: hover) and (pointer: fine) and (min-width: 768px)";
const DRIFT_MAX = 24;
const ROTATE_MAX = 3;

const MEDIA: Record<Kind, { video: string; poster: string; frames: string }> = {
  desktop: {
    video: "/media/hero-desktop.mp4",
    poster: "/media/hero-desktop-poster.jpg",
    frames: "/media/hero-frames/desktop/manifest.json",
  },
  mobile: {
    video: "/media/hero-mobile.mp4",
    poster: "/media/hero-mobile-poster.jpg",
    frames: "/media/hero-frames/mobile/manifest.json",
  },
};

function clamp01(value: number): number {
  return Math.min(1, Math.max(0, value));
}

function segment(progress: number, start: number, end: number): number {
  if (end <= start) return progress >= end ? 1 : 0;
  return clamp01((progress - start) / (end - start));
}

function pickKind(): Kind {
  return window.matchMedia(DESKTOP_QUERY).matches ? "desktop" : "mobile";
}

function posterOnly(): boolean {
  if (prefersReducedMotion()) return true;
  const connection = (navigator as Navigator & { connection?: NetworkInformation }).connection;
  if (!connection) return false;
  if (connection.saveData) return true;
  return connection.effectiveType === "slow-2g" || connection.effectiveType === "2g";
}

async function readManifest(kind: Kind): Promise<FrameManifest | null> {
  try {
    const response = await fetch(MEDIA[kind].frames);
    if (!response.ok) return null;
    const data = (await response.json()) as Partial<FrameManifest>;
    if (typeof data.count !== "number" || data.count < 1) return null;
    return {
      count: Math.floor(data.count),
      first: typeof data.first === "number" ? data.first : 1,
      pad: typeof data.pad === "number" ? data.pad : 4,
      ext: typeof data.ext === "string" && data.ext.length > 0 ? data.ext : "webp",
    };
  } catch {
    return null;
  }
}

/**
 * Scroll-scrubbed home hero. Maps section progress to the film, with a
 * frame-sequence fallback when seeking cannot keep up.
 */
export function initHero(root: HTMLElement): void {
  if (root.dataset.heroReady === "true") return;
  root.dataset.heroReady = "true";

  const video = root.querySelector<HTMLVideoElement>("[data-hero-video]");
  const canvas = root.querySelector<HTMLCanvasElement>("[data-hero-canvas]");
  const wordmark = root.querySelector<HTMLElement>("[data-hero-wordmark]");
  const copy = root.querySelector<HTMLElement>("[data-hero-copy]");
  const mono = root.querySelector<HTMLElement>("[data-hero-mono]");
  const visual = root.querySelector<HTMLElement>("[data-hero-mono-visual]");
  const scrollHint = root.querySelector<HTMLElement>("[data-hero-scroll]");
  const sweep = root.querySelector<HTMLElement>("[data-hero-sweep]");
  const button = root.querySelector<HTMLAnchorElement>("[data-hero-join]");
  if (!video || !canvas || !wordmark || !copy || !mono || !visual || !scrollHint || !sweep) return;

  const line = visual.dataset.line ?? visual.textContent ?? "";
  visual.textContent = "";
  const chars: HTMLElement[] = [];
  const sentences = line.split(/(?<=\.)\s+/).filter((sentence) => sentence.length > 0);
  sentences.forEach((sentence, sentenceIndex) => {
    const sentenceSpan = document.createElement("span");
    sentenceSpan.className = "hero-mono-sentence";
    const words = sentence.split(" ").filter((word) => word.length > 0);
    words.forEach((word, wordIndex) => {
      const wordSpan = document.createElement("span");
      wordSpan.className = "hero-mono-word";
      Array.from(word).forEach((char) => {
        const span = document.createElement("span");
        span.textContent = char;
        gsap.set(span, { opacity: 0 });
        wordSpan.append(span);
        chars.push(span);
      });
      sentenceSpan.append(wordSpan);
      if (wordIndex < words.length - 1) {
        const gap = document.createElement("span");
        gap.className = "hero-mono-gap";
        gap.textContent = " ";
        gsap.set(gap, { opacity: 0 });
        sentenceSpan.append(gap);
        chars.push(gap);
      }
    });
    visual.append(sentenceSpan);
    if (sentenceIndex < sentences.length - 1) {
      const gap = document.createElement("span");
      gap.className = "hero-mono-gap hero-mono-gap--sentence";
      gap.textContent = " ";
      gsap.set(gap, { opacity: 0 });
      visual.append(gap);
      chars.push(gap);
    }
  });

  const desktopQuery = window.matchMedia(DESKTOP_QUERY);
  const fineQuery = window.matchMedia(FINE_QUERY);
  const context = canvas.getContext("2d", { alpha: false });

  let mode: Mode = "still";
  let kind = pickKind();
  let progress = 0;
  let targetTime = 0;
  let smoothed = 0;
  let running = true;
  let canSeek = true;
  let stallSince = 0;
  let stalls = 0;
  let framesTried = false;
  let manifest: FrameManifest | null = null;
  let tween: gsap.core.Tween | undefined;
  let meltTween: gsap.core.Tween | undefined;
  let rafId = 0;
  const frameCache = new Map<number, HTMLImageElement>();
  const frameLoading = new Set<number>();
  let canvasWidth = 0;
  let canvasHeight = 0;
  let driftX = 0;
  let driftY = 0;
  let driftRot = 0;
  let targetX = 0;
  let targetY = 0;
  let targetRot = 0;
  let sweepTravel = 0;

  function measureSweep(): void {
    const stageWidth = stage?.clientWidth ?? 0;
    const barWidth = sweep?.offsetWidth ?? 0;
    if (stageWidth <= 0) return;
    sweepTravel = Math.max(0, stageWidth - barWidth);
  }

  function parkSweep(): void {
    const stageWidth = stage?.clientWidth ?? window.innerWidth;
    const left = desktopQuery.matches ? stageWidth * 0.07 : 16;
    sweep.style.transform = `translate3d(${left}px, 0, 0)`;
    sweep.style.opacity = "1";
  }

  function placeSweep(next: number, clear: number): void {
    if (mode === "still") {
      parkSweep();
      return;
    }
    if (sweepTravel === 0) measureSweep();
    sweep.style.transform = `translate3d(${next * sweepTravel}px, 0, 0)`;
    sweep.style.opacity = String(1 - clear);
  }

  function applyScene(next: number): void {
    progress = next;
    const lift = segment(next, 0.35, 0.5);
    gsap.set(copy, { y: -56 * lift, opacity: 1 - lift });
    if (button) {
      if (lift > 0.92) button.setAttribute("tabindex", "-1");
      else button.removeAttribute("tabindex");
    }
    copy.style.pointerEvents = lift > 0.92 ? "none" : "";

    const typed = segment(next, 0.6, 0.78);
    chars.forEach((span, index) => {
      const opacity = typed * chars.length >= index + 1 ? 1 : 0;
      if (span.dataset.on !== String(opacity)) {
        span.dataset.on = String(opacity);
        gsap.set(span, { opacity });
      }
    });

    const clear = segment(next, 0.9, 1);
    gsap.set(mono, { opacity: (typed > 0 ? 1 : 0) * (1 - clear), y: -20 * clear });
    const hint = (1 - segment(next, 0.08, 0.22)) * (1 - clear);
    gsap.set(scrollHint, { opacity: hint, y: 12 * (1 - hint) });
    gsap.set(wordmark, { opacity: 1 - clear });
    placeSweep(next, clear);

    if (!fineQuery.matches && mode !== "still") {
      // Parked on phones. A drift here would eat the 16px side clearance.
      targetX = 0;
      targetY = 0;
      targetRot = 0;
    }
  }

  function stepWordmark(): void {
    if (mode === "still") return;
    driftX += (targetX - driftX) * 0.08;
    driftY += (targetY - driftY) * 0.08;
    driftRot += (targetRot - driftRot) * 0.08;
    const x = Math.max(-DRIFT_MAX, Math.min(DRIFT_MAX, driftX));
    const y = Math.max(-DRIFT_MAX, Math.min(DRIFT_MAX, driftY));
    const rot = Math.max(-ROTATE_MAX, Math.min(ROTATE_MAX, driftRot));
    wordmark.style.transform = `translate3d(${x}px, ${y}px, 0) rotate(${rot}deg)`;
  }

  function noteStall(): void {
    stalls += 1;
    if (stalls >= 6) void useFrames();
  }

  function stepVideo(): void {
    if (mode === "frames") {
      drawFrame(progress);
      return;
    }
    if (mode !== "video") return;
    const duration = video.duration;
    if (!Number.isFinite(duration) || duration <= 0) return;
    if (video.readyState < 2) return;

    smoothed += (targetTime - smoothed) * 0.55;
    if (Math.abs(video.currentTime - smoothed) < 1 / 24) {
      canSeek = true;
      stallSince = 0;
      return;
    }
    if (!canSeek) {
      if (stallSince === 0) stallSince = performance.now();
      else if (performance.now() - stallSince > 280) {
        canSeek = true;
        stallSince = 0;
        noteStall();
      }
      return;
    }

    canSeek = false;
    stallSince = performance.now();
    const requested = smoothed;
    try {
      video.currentTime = requested;
    } catch {
      canSeek = true;
      noteStall();
      return;
    }

    const withFrame = video as HTMLVideoElement & {
      requestVideoFrameCallback?: (callback: () => void) => number;
    };
    if (typeof withFrame.requestVideoFrameCallback === "function") {
      withFrame.requestVideoFrameCallback(() => {
        canSeek = true;
        stallSince = 0;
        const late = Math.abs(video.currentTime - requested);
        if (video.readyState < 2 || late > 0.45) noteStall();
      });
    } else {
      canSeek = true;
      stallSince = 0;
    }
  }

  function loop(): void {
    if (!running) return;
    rafId = requestAnimationFrame(loop);
    if (document.hidden) return;
    stepWordmark();
    stepVideo();
  }

  function sizeCanvas(): void {
    if (!context) return;
    const rect = canvas.getBoundingClientRect();
    const cap = kind === "mobile" ? 1.25 : 2;
    const dpr = Math.min(window.devicePixelRatio || 1, cap);
    const width = Math.max(1, Math.round(rect.width * dpr));
    const height = Math.max(1, Math.round(rect.height * dpr));
    if (width === canvasWidth && height === canvasHeight) return;
    canvasWidth = width;
    canvasHeight = height;
    canvas.width = width;
    canvas.height = height;
  }

  function frameUrl(index: number): string {
    if (!manifest) return "";
    const name = String(index).padStart(manifest.pad, "0");
    return `/media/hero-frames/${kind}/${name}.${manifest.ext}`;
  }

  function wantFrame(index: number): void {
    if (!manifest) return;
    const last = manifest.first + manifest.count - 1;
    if (index < manifest.first || index > last) return;
    if (frameCache.has(index) || frameLoading.has(index)) return;
    frameLoading.add(index);
    const image = new Image();
    image.decoding = "async";
    image.onload = () => {
      frameCache.set(index, image);
      frameLoading.delete(index);
    };
    image.onerror = () => {
      frameLoading.delete(index);
    };
    image.src = frameUrl(index);
  }

  function nearestFrame(index: number): HTMLImageElement | undefined {
    if (frameCache.has(index)) return frameCache.get(index);
    let found: HTMLImageElement | undefined;
    let best = Number.POSITIVE_INFINITY;
    frameCache.forEach((image, key) => {
      const gap = Math.abs(key - index);
      if (gap < best) {
        best = gap;
        found = image;
      }
    });
    return found;
  }

  function drawCover(image: HTMLImageElement): void {
    if (!context) return;
    sizeCanvas();
    const scale = Math.max(canvas.width / image.naturalWidth, canvas.height / image.naturalHeight);
    const width = image.naturalWidth * scale;
    const height = image.naturalHeight * scale;
    context.drawImage(image, (canvas.width - width) / 2, (canvas.height - height) / 2, width, height);
  }

  function drawFrame(next: number): void {
    if (!manifest) return;
    const index = manifest.first + Math.round(next * (manifest.count - 1));
    const radius = kind === "mobile" ? 4 : manifest.count <= 180 ? manifest.count : 16;
    const start = kind === "mobile" || manifest.count > 180 ? index - radius : manifest.first;
    const end = kind === "mobile" || manifest.count > 180 ? index + radius : manifest.first + manifest.count - 1;
    for (let cursor = start; cursor <= end; cursor += 1) wantFrame(cursor);
    const image = nearestFrame(index);
    if (!image) return;
    drawCover(image);
    root.classList.add("is-frames");
  }

  async function useFrames(): Promise<void> {
    if (framesTried || mode === "frames" || mode === "still") return;
    framesTried = true;
    const next = await readManifest(kind);
    if (!next) return;
    manifest = next;
    mode = "frames";
    video.pause();
    root.classList.add("is-frames");
    root.classList.remove("is-video");
    drawFrame(progress);
  }

  function readRootNumber(name: string, fallback: number): number {
    const raw = getComputedStyle(document.documentElement).getPropertyValue(name).trim();
    const value = Number.parseFloat(raw);
    return Number.isFinite(value) ? value : fallback;
  }

  function readRootPx(name: string, fallbackVh: number): number {
    const raw = getComputedStyle(document.documentElement).getPropertyValue(name).trim();
    if (raw.endsWith("vh")) return (Number.parseFloat(raw) / 100) * window.innerHeight;
    if (raw.endsWith("px")) return Number.parseFloat(raw);
    return window.innerHeight * fallbackVh;
  }

  function meltEl(): HTMLElement | null {
    return root.querySelector<HTMLElement>("[data-hero-melt]");
  }

  function stopMelt(): void {
    meltTween?.scrollTrigger?.kill();
    meltTween?.kill();
    meltTween = undefined;
  }

  function parkMelt(): void {
    stopMelt();
    const el = meltEl();
    if (!el) return;
    el.style.willChange = "auto";
    el.style.filter = "none";
    el.style.setProperty("--melt", String(readRootNumber("--hero-melt", 0.07)));
  }

  function startMelt(): void {
    stopMelt();
    const el = meltEl();
    if (!el) return;
    const phone = !desktopQuery.matches;
    const maxMelt = readRootNumber("--hero-melt", phone ? 0.5 : 0.48);
    const maxBlur = phone ? 0 : 12;
    const state = { v: 0 };
    let shownBlur = -1;
    el.style.willChange = "auto";
    el.style.filter = "none";
    el.style.setProperty("--melt", "0");

    meltTween = gsap.to(state, {
      v: maxMelt,
      ease: "none",
      scrollTrigger: {
        trigger: root,
        start: () => {
          const vh = window.innerHeight;
          const overlap = readRootPx("--hero-overlap", phone ? 0.58 : 0.56);
          // Phone: the last 42vh of the film, always inside the overlap.
          // Desktop: the fade runs across the overlap minus a short buffer.
          const lead = phone
            ? Math.min(Math.max(0, overlap - vh * 0.06), vh * 0.42)
            : Math.max(vh * 0.14, overlap - vh * 0.1);
          return `bottom-=${Math.round(lead)}px bottom`;
        },
        end: "bottom bottom",
        scrub: phone ? true : 0.65,
        invalidateOnRefresh: true,
        onToggle: (self) => {
          el.style.willChange = self.isActive && maxBlur > 0 ? "filter" : "auto";
        },
      },
      onUpdate: () => {
        el.style.setProperty("--melt", state.v.toFixed(4));
        if (maxBlur <= 0) return;
        const blur = maxMelt > 0 ? (state.v / maxMelt) * maxBlur : 0;
        const next = blur > 0.15 ? blur : 0;
        if (Math.abs(next - shownBlur) < 0.08) return;
        shownBlur = next;
        el.style.filter = next === 0 ? "none" : `blur(${next.toFixed(2)}px)`;
      },
    });
  }

  function stopScrub(): void {
    tween?.scrollTrigger?.kill();
    tween?.kill();
    tween = undefined;
    stopMelt();
    video.pause();
  }

  function startScrub(): void {
    stopScrub();
    const playhead = { p: 0 };
    tween = gsap.to(playhead, {
      p: 1,
      ease: "none",
      duration: 1,
      scrollTrigger: {
        trigger: root,
        start: "top top",
        end: "bottom bottom",
        scrub: 0.5,
        invalidateOnRefresh: true,
        onToggle: (self) => {
          const moving = self.isActive ? "transform, opacity" : "auto";
          wordmark.style.willChange = moving;
          copy.style.willChange = moving;
          mono.style.willChange = moving;
          sweep.style.willChange = self.isActive ? "transform" : "auto";
        },
      },
      onUpdate: () => {
        applyScene(playhead.p);
        const duration = video.duration;
        if (mode === "video" && Number.isFinite(duration) && duration > 0) {
          targetTime = playhead.p * duration;
        }
      },
    });
    applyScene(0);
    startMelt();
  }

  function mountVideo(next: Kind): void {
    kind = next;
    mode = "video";
    stalls = 0;
    framesTried = false;
    manifest = null;
    frameCache.clear();
    root.classList.remove("is-frames", "hero--still");
    const paths = MEDIA[kind];
    video.poster = paths.poster;
    video.preload = "auto";
    video.muted = true;
    video.playsInline = true;
    if (video.getAttribute("src") !== paths.video) {
      root.classList.remove("is-video");
      video.src = paths.video;
      video.load();
    }
    measureSweep();
    startScrub();
  }

  function showStill(): void {
    mode = "still";
    stopScrub();
    video.removeAttribute("src");
    video.load();
    root.classList.add("hero--still");
    root.classList.remove("is-video", "is-frames");
    driftX = 0;
    driftY = 0;
    driftRot = 0;
    targetX = 0;
    targetY = 0;
    targetRot = 0;
    wordmark.style.transform = "none";
    gsap.set([copy, mono, scrollHint, wordmark], { clearProps: "transform,opacity" });
    gsap.set(copy, { opacity: 1, y: 0 });
    gsap.set(wordmark, { opacity: 1 });
    copy.style.pointerEvents = "";
    button?.removeAttribute("tabindex");
    chars.forEach((span) => gsap.set(span, { opacity: 0 }));
    wordmark.style.willChange = "auto";
    copy.style.willChange = "auto";
    mono.style.willChange = "auto";
    sweep.style.willChange = "auto";
    parkSweep();
    parkMelt();
  }

  function boot(): void {
    if (posterOnly()) {
      showStill();
      return;
    }
    mountVideo(pickKind());
  }

  function onPointer(event: PointerEvent): void {
    if (!fineQuery.matches || mode === "still") return;
    const nx = (event.clientX / window.innerWidth) * 2 - 1;
    const ny = (event.clientY / window.innerHeight) * 2 - 1;
    targetX = nx * DRIFT_MAX;
    targetY = ny * (DRIFT_MAX / 2);
    targetRot = nx * ROTATE_MAX;
  }

  function onPointerLeave(): void {
    if (!fineQuery.matches) return;
    targetX = 0;
    targetY = 0;
    targetRot = 0;
  }

  video.addEventListener("loadeddata", () => {
    if (mode === "video" && video.readyState >= 2) root.classList.add("is-video");
  });
  video.addEventListener("error", () => {
    root.classList.remove("is-video");
    void useFrames();
  });

  const stage = root.querySelector<HTMLElement>("[data-hero-stage]");
  stage?.addEventListener("pointermove", onPointer);
  stage?.addEventListener("pointerleave", onPointerLeave);

  function onResize(): void {
    measureSweep();
    if (mode === "still") parkSweep();
    else applyScene(progress);
  }
  window.addEventListener("resize", onResize);

  const stopReduced = onReducedMotionChange(() => {
    stalls = 0;
    framesTried = false;
    boot();
  });
  desktopQuery.addEventListener("change", () => {
    if (mode === "still") return;
    mountVideo(pickKind());
  });

  boot();
  rafId = requestAnimationFrame(loop);

  window.addEventListener("pagehide", () => {
    running = false;
    cancelAnimationFrame(rafId);
    window.removeEventListener("resize", onResize);
    stopScrub();
    stopReduced();
  });
}
