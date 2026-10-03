import { bootFilterShelf } from "./filter-shelf";

/** Guides page shelf. Same filter, same Flip, same ?c= URL as before. */
export function bootGuidesFilter(): void {
	bootFilterShelf({
		root: "[data-guides]",
		grid: "[data-guide-grid]",
		card: "[data-guide-card]",
		empty: "[data-guide-empty]",
		status: "[data-guide-status]",
		shelf: "[data-filter-shelf]",
		noun: "guide",
		emptyStatus: "Nothing here yet. Next live, probably.",
		readyKey: "guidesReady",
	});
}
