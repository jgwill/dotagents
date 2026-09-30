# Page-circle wire contract

Verified on 2026-09-30 against Miadi's `lib/page-post.ts` and live episode 548 read-back. Authority remains the current `packages/community/PAGE-POST-CIRCLE.md` plus the human's latest instructions; this reference is not publication permission. Re-measure routes and identity before using them.

## Identity is a resolved person, not a variable label

Use the explicitly provided credential location without printing its value. Call `GET /api/identity/me` on the named Miadi front and require `person.id` and `person.name` to match the intended speaker before any ceremony or turn write. Reject a system identity or another person's identity. Then read `GET /api/circles/<id>` and verify membership and `can.open_ceremony`.

In the verified Kherix installation, the credential named `MIADI_API_TOKEN_WRITER` resolved to Kherix (`node:human:1790760357285:j7o5qx`), not a shared writer identity. The old variable name alone was not evidence of its current authority. Do not copy the token into a new store or enumerate unrelated secrets to find it.

## An image URL is not the Chronicle text-files route

For an already-authorized Chronicle image, the existing viewer asset route is:

```text
https://<Miadi-front>/v/asset/<absolute-file-path-without-leading-slash>
```

For example, `/srv/miadi/episodes/.../page-posts/guillaume-coder/image.png` becomes `/v/asset/srv/miadi/episodes/.../page-posts/guillaume-coder/image.png`. Construct and URL-encode path segments as needed. Require HTTP 200, the expected image MIME type, and byte equality (or SHA-256 equality) with the canonical file. Do not upload another copy or modify application routes to evade the viewer's allowed-root checks.

The image route implementation is `app/v/asset/[...path]/route.ts`; PNG support is in `app/v/asset-types.ts`. The text-oriented `/api/chronicle/episodes/<ref>/files/...` route returned 415 for this PNG while `/v/asset/...` served its exact bytes. A missing local file may yield a containment failure (403); verify existence before diagnosing permissions. Never disable containment.

## Proposal turn: exact syntax

Send one `POST /api/ceremony/<ceremony-id>/turns` body with `title` and `said`. The `said` string is:

```text
Page post · Guillaume Coder · https://www.facebook.com/Guillaumecoder/
Version: v2
Image: <verified public https image URL>
Episode: <public episode URL>

<exact Facebook post text>
```

No Markdown heading, JSON wrapper, commentary or blank line precedes the first line. Header lines end at the first blank line. Every subsequent line is post text, including links and AI attribution. Editorial caveats belong in the ceremony intention or a separate ordinary turn, not after the Facebook copy. A new complete version uses its actual version label; do not silently reuse a witnessed version for changed text or media.

The production parser is `lib/page-post.ts::parsePagePost`. When checking a constructed payload, exercise that actual parser and assert its Page URL, version, image, episode and body rather than making a permissive replacement parser.

## Open once, speak once, verify

1. Read the named circle and inspect its `ceremonies` before creating one. Match the intended post/episode; an episode can have several distinct post ceremonies, so do not reuse one by episode alone when that is ambiguous.
2. Open through `POST /api/circles/<circle-id>/ceremonies` with an intention, `type: talking_circle`, direction, and the exact episode directory name as `episode_path`. Preserve and commit any episode note returned by the app.
3. Read `GET /api/ceremony/<id>`. Require the correct circle and episode, the intended `me.id`, `can.speak`, and `closed: false`.
4. Compare existing turns by exact `speaker` and `prose` before speaking. A timeout is not proof that a write failed: re-read before retrying a POST.
5. After speaking, read the ceremony again and require the returned turn ID, exact `prose`, and expected `speaker`. Preserve IDs, URLs and text/image hashes in the canonical post's receipt; never save credentials there.
6. Creating or speaking does not witness or close anything. Do not call those endpoints as an incidental verification step. Read their actual state and leave later facilitator actions untouched.

## Publication receipt: only after Facebook read-back

```text
Page post published · <verified Facebook permalink>
Version: v2
```

The version must match the published proposal. Do not emit this receipt for a preview, queued browser action or unverified publication. Read `facilitator_witnessed` for the normal publication gate, or preserve the exact scope of an applicable direct human exception. An uncertain relay is not blanket permission.

Private circle access and public image access are separate. A working API read-back and parser check do not prove the browser's visual rendering; report precisely which surfaces were exercised. Deliver the ceremony link as the review door rather than a folder list.
