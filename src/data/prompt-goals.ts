/** Page order. Goals with no prompts stay out of the menu and the page. */
export const promptGoalIds = [
	"websites",
	"grok-build",
	"grok-bot",
	"brand",
	"images-video",
	"content",
	"business",
] as const;

export type PromptGoalId = (typeof promptGoalIds)[number];

export interface PromptGoal {
	id: PromptGoalId;
	label: string;
	description: string;
}

export const promptGoals: readonly PromptGoal[] = [
	{
		id: "websites",
		label: "Websites",
		description: "Plan a site that doesn't look like a template.",
	},
	{
		id: "grok-build",
		label: "Grok Build",
		description: "Build it one prompt, one job, one commit at a time.",
	},
	{
		id: "grok-bot",
		label: "Grok Bot",
		description: "Hand the busywork to your Bots. Read it before it goes out.",
	},
	{
		id: "brand",
		label: "Brand",
		description: "Find your why, your look, and your voice, in that order.",
	},
	{
		id: "images-video",
		label: "Images and video",
		description: "Stills and loops in Grok Imagine. No text in the picture.",
	},
	{
		id: "content",
		label: "Content and social",
		description: "Posts and emails that sound like you on a good day.",
	},
	{
		id: "business",
		label: "Business",
		description: "Capture emails, sell softly, and keep it honest.",
	},
];

export function promptCountLabel(count: number): string {
	return `${count} ${count === 1 ? "prompt" : "prompts"}`;
}
