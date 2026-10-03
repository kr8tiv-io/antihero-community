import rss from "@astrojs/rss";
import { getCollection } from "astro:content";
import { SITE_URL } from "../data/site";

export async function GET(context) {
	const posts = (await getCollection("blog")).filter((post) => post.data.draft === false);
	posts.sort(
		(a, b) => b.data.date.getTime() - a.data.date.getTime() || b.id.localeCompare(a.id),
	);

	return rss({
		title: "AntiHero AI",
		description: "Short posts about what worked, what broke, and what I'd do differently.",
		site: context.site ?? SITE_URL,
		items: posts.map((post) => ({
			title: post.data.title,
			pubDate: post.data.date,
			description: post.data.description,
			link: `/blog/${post.id}/`,
		})),
		customData: "<language>en</language>",
	});
}
