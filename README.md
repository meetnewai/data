> Official open data from [MeetNewAI](https://meetnewai.com). The MeetNewAI product source is closed; this repository contains public data snapshots only.

# MeetNewAI listings: weekly dataset

Weekly snapshots of every listing in the [MeetNewAI](https://meetnewai.com) directory: AI tools, browser AI games, MCP servers and agent skills. Each listing was checked on its official site, and the check date is included.

- Source feed: <https://meetnewai.com/api/tools.json>
- How listings are checked: [meetnewai/docs](https://github.com/meetnewai/docs/blob/main/docs/methodology.md)
- Traffic for these tools: [vaneform/data](https://github.com/vaneform/data)

## Files

| Path | What |
|---|---|
| `latest.json` | The most recent snapshot |
| `snapshots/YYYY-MM-DD.json` | Dated snapshots (UTC date of the fetch). A new file is written only when the content changed. |
| `scripts/snapshot.py` | Fetch, field filter and change check (standard-library Python) |
| `.github/workflows/snapshot.yml` | Weekly GitHub Action (Mondays 02:17 UTC, plus manual runs) |

## Schema

Top level: `version`, `name`, `provider` (`meetnewai`), `description`, `homepage`, `count`, `generatedAt` (ISO 8601 UTC), `items`.

| Field | Type | Meaning |
|---|---|---|
| `slug` | string | Listing id, stable across snapshots |
| `name` | string | Product name |
| `kind` | string | `product`, `game`, `mcp` or `skill` |
| `category` | string | Category slug |
| `categoryName` | string | Category name (English) |
| `url` | string | Official site |
| `domain` | string or null | Official domain; `null` when the official site lives under a path |
| `pricing` | string | Pricing note as checked, or `Price not checked yet` |
| `tags` | string[] | Tags |
| `listingUrl` | string | MeetNewAI page (English) |
| `listingUrlZh` | string | MeetNewAI page (Chinese) |
| `verified` | string `YYYY-MM-DD` | Last check on the official site |

## What is not included

Only MeetNewAI's own listing fields are kept. Third-party model data shown on meetnewai.com is **not** redistributed here: Codex Radar data (used with permission, attribution only) and real-api-pricing data (MIT) stay on the site with their notices. The snapshot script keeps an allowlist of fields, so a third-party field added to the feed later is dropped automatically.

Some listings started as leads from the [WorthToTry](https://worthtotry.com) catalogue (CC BY 4.0). Their facts were re-checked on each official site and the descriptions are MeetNewAI's own.

## License and attribution

This dataset is licensed under [CC BY 4.0](LICENSE). Please attribute as:

> Data: MeetNewAI listings (https://meetnewai.com), CC BY 4.0.

## 中文

本仓库每周保存 MeetNewAI 全部收录（AI 工具、AI 小游戏、MCP 服务器、Agent Skills）的数据快照，每条均在官网核对并附核对日期。只包含 MeetNewAI 自有字段，不再分发第三方模型数据。按 CC BY 4.0 授权，引用时请注明 MeetNewAI 并附链接。
