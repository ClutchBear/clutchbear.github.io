import { defineAstroPaperConfig } from "./src/types/config";

export default defineAstroPaperConfig({
  site: {
    url: "https://clutchbear.github.io",
    title: "信哥的博客",
    description: "技术笔记与折腾记录：Python、运维、硬件、生活。",
    author: "ClutchBear",
    profile: "https://clutchbear.github.io",
    ogImage: "default-og.jpg",
    lang: "zh",
    timezone: "Asia/Shanghai",
    dir: "ltr",
  },
  posts: {
    perPage: 8,
    perIndex: 4,
    scheduledPostMargin: 15 * 60 * 1000,
  },
  features: {
    lightAndDarkMode: true,
    dynamicOgImage: false, // 关闭动态 OG 生成，省构建时间；回退 public/default-og.jpg
    showArchives: true,
    showBackButton: true,
    editPost: { enabled: false },
    search: "pagefind",
  },
  socials: [
    { name: "github", url: "https://github.com/ClutchBear" },
    { name: "mail", url: "mailto:skywater@gmail.com" },
  ],
  shareLinks: [],
});
