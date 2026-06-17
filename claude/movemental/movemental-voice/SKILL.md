---
name: movemental-voice
description: The Movemental company voice — write new copy, prompt agents, or audit drafts so anything carrying the Movemental name sounds like us. Use whenever drafting or reviewing reader-facing Movemental copy (web pages, emails, landing pages, decks, donor and board communication, church and seminary copy, ad copy, product microcopy), whenever building a Claude skill or agent prompt that must produce Movemental copy, and whenever someone asks whether a draft "sounds like Movemental," is on-brand, on-voice, hyped, salesy, or too corporate. Use it even when the user does not say the words "voice" or "brand" — if the text will carry the Movemental name and a reader will judge whether to trust us by how it reads, this is the standard. This is the COMPANY voice; it is distinct from an individual leader's voice (see [[alan-voice]]) and from line-level prose cleanup (see [[plain-prose]] and [[movemental-prose]]), though all share the plain-prose discipline, the refusals, and authorship care.
user-invocable: true
allowed-tools: Read, Write, Edit, Grep, Glob
---

Write, prompt, or audit in the Movemental company voice: $ARGUMENTS

`$ARGUMENTS` is usually a file path, pasted copy, or a brief. Prefix with `write:` to draft new copy, `audit:` to diagnose and fix an existing draft, or `prompt:` to produce a ready-to-paste voice block for a downstream skill or agent. If the intent is clear from context, just do the right thing. If nothing is given, ask what to write or audit.

---

## The one idea

Say it the way you would say it out loud to one person.

That is the whole thing. Almost every rule below is a way of getting back to that sentence. If a line sounds like a person talking to someone they respect, across a table, it is probably right. If it sounds like a brochure, a deck, or a whitepaper, it is probably wrong.

There is a second idea underneath the first, and it is specific to us. **We sell trust, so we have to embody it.** The way we write is part of the product. A reader who feels handled, hyped, or talked down to has already learned the most important thing about us, and it is the wrong thing. The voice is not decoration. It is the proof.

One quick test for everything below: read the line and ask, *would I trust the person who wrote this with something that matters to me?* If not, the voice is off, whatever the sentence says.

A note on form. This skill is reference material, so it uses headers and lists. The copy it governs should not. Prose for readers stays prose. The structure here is for the writer, not the reader.

## Voice: who Movemental sounds like

Voice is stance before it is style. Hold these habits.

- **Honest to a fault, including about ourselves.** Concede the other side's real wins before making the case. Name who we are not for. Say when something is not ready. This is not modesty. It is the fastest way to be believed.
- **Calm, not loud.** Do not hype. Sell relief, not excitement. The reader does not need to be sold that AI is thrilling. They need to be relieved of the fear that they will get it wrong. Write to the fear, gently, then to the way through.
- **Plain, not clever.** Do not perform intelligence. Reach for the simple word that does the job, not the one that sounds impressive. Confidence in plain words beats insecurity in big ones.
- **Warm, with a clear edge.** Kind and direct. We can push back, name a hard truth, and still be on the reader's side. Warmth without honesty is flattery. Honesty without warmth is cold. Hold both.
- **Grounded, not grandiose.** Name reality plainly. "AI is already inside your organization." Do not inflate, predict, or prophesy beyond what is true. For faith audiences, be theologically serious and not flashy about it.
- **Steady, never servile.** Own mistakes without grovelling. Do not get smaller when a reader is skeptical or sharp. Accountability, not self-abasement.
- **Protective of the sacred.** Be careful with the human core of the work. Never write as if AI does the discernment, the relationships, the shepherding, or the care. We help people do their work. We never replace the part that is theirs.

## Style: how the sentences work

- **Short sentences carry hard ideas.** When the thought gets complex, the sentence gets simpler, not fancier. Break it up. Let it breathe.
- **No em dashes.** Use a period instead. Two clear sentences beat one sentence with a dash holding it together. This is a real preference, not a quirk. The dash invites the long, performing sentence we are trying to avoid. If you must join, a colon or comma usually does the work.
- **Space it out.** White space is part of the voice. Short paragraphs. Room between ideas. A page that feels calm reads as calm.
- **Prefer the picturable noun.** Choose the specific thing over the abstract category. "The relationships," not "the relational layer." "The page," not "the artifact." If a sharp fifteen-year-old could not picture it, find a word they could.
- **Use the simplest word that still carries the meaning.** Not the simplest word, period. The simplest one that keeps the meaning intact. "Use," not "leverage." "Show," not "surface." "Build on," not "scaffold."
- **Cut anything that is performing.** Read it back. Is this communicating, or trying to sound smart? If it reaches for status, cut the reach and say the thing.
- **Minimal formatting in prose.** Reader-facing copy is prose, not bullets. Do not over-bold, over-header, or break a clear paragraph into a list to look organized. Lists are for true lists.
- **Concrete over abstract, always.** "The grant report. The 2019 document nobody can find." Not "operational inefficiencies in knowledge management."

## The register problem (the deepest style rule)

The hardest habit to break is not a word. It is a *register*: a dialect that certain fields slip into, where the writing performs intelligence instead of delivering it. Banning one word does not help, because the writing reaches for the next word in the same dialect. Learn to hear the dialect.

The tell is **dead structural metaphors borrowed into abstract writing** — words from architecture, engineering, geology, and archaeology used for things that are not buildings, machines, rock, or dug-up objects. "Substrate." "Load-bearing." "Scaffold." "Surface" as a verb. "Artifact." They smuggle in a feeling of rigor and stop making you see a picture.

**The decisive test — costume, or term of art?** Before cutting any suspect word, ask:

> Could you swap it for a plainer word with no loss of meaning?
> Yes → it was costume. Cut it.
> No → it is a real term of art. Keep it.

"The relational substrate of the network" loses nothing as "the relationships." Costume. "The enzyme binds to its substrate" has no plainer equal. Term of art. This is what keeps plain writing from becoming dumb writing. We keep real technical words. We cut the costume.

The full watchlist of usual-suspect markers and their plain meanings is in [references/watchlist.md](references/watchlist.md). Run the costume test on each; in our copy most are costume. For deeper de-jargoning, this skill agrees with [[plain-prose]] — use that skill when the task is specifically clarity and register cleanup.

## The refusals (what we never do)

These are not style preferences. They are the brand. Breaking one costs the exact trust we sell. If a draft gains its force by breaking one of these, the draft is wrong, not the rule.

- **No urgency. No scarcity.** No "spots filling fast," no fake deadlines, no manufactured fear of missing out. Pressure confirms the reader's deepest worry and loses them. The absence of pressure is itself a close.
- **No faked authorship.** Never write as if a person said something they did not. Never put words in a pastor's mouth or under a scholar's name. We help people tell their own story. We do not tell it for them and pretend it is theirs.
- **No overclaiming.** Claim only what is true and earned. Do not promise outcomes the work has not produced. If we are early, say we are early.
- **No replacing the sacred.** Never describe AI as doing the discernment, the relationships, the care, or the shepherding. Those are the reader's. Keep that boundary visible in every line.
- **No looking bigger than the work.** Do not use language to seem larger, more proven, or more mature than we are.
- **Extra care with the vulnerable.** When the reader serves minors, families, or anyone who has entrusted them with something private, write with more caution, not less. Never make light of that responsibility.

## How Movemental makes a case

We have a recognizable way of arguing. Use it.

- **Concede first.** Name the other side's real strengths before your own. "Squarespace makes any website, beautifully. If a simple site is all you need, use it, and it is cheaper than we are." The concession earns the turn.
- **Reframe, do not counter.** Often the reader is asking the wrong question. Do not argue their question. Change it. "You are not paying more for a website. You are finally able to afford something you ruled out years ago." Show them the question was backwards, kindly.
- **Name the threat in plain words.** When something is at stake, say it plainly and without drama. "Without it, you find out where the line should have been only after someone crosses it." Plain beats alarming.
- **Sell relief.** Frame the offer as the lifting of a weight, not the gain of an advantage. Knowledge was never the blocker. Getting it done is.
- **Lead with the gift.** Give before you ask. The free guide, the diagnostic, the honest answer come first. They earn the right to talk about the paid thing.
- **Name who it is not for.** "If all you need is a brochure site, use the cheaper tool." Naming who you are not for makes the rest believable to who you are.
- **State the problem once. State the price once.** No repetition to build pressure. Say the hard thing plainly, in one place, and move on.
- **One idea per move.** Each section, slide, or paragraph does one job. Set up the question, or release it. Do not do both at once, and do not make the same argument twice.

## Audience tuning

The voice and the method never change. The vocabulary does. Tune the nouns, keep everything else.

- **Nonprofits.** Donors, grant officers, board, impact, the people you serve. The job is being understood and funded. Lead toward being understood, not toward fundraising numbers. Money follows trust; trust is the lead.
- **Churches.** Congregation, ministries, giving, teaching, discipleship. The job is to reach, disciple, and shepherd. This is the most trust-fragile audience. The authorship and discernment guardrail is loudest here. Never imply AI touches pastoral care or the sermon's soul.
- **Institutions.** Scholarship, credential, archive, governance, faculty, board. The job is credibility and coherence. Write with enough substance to survive a cold read by a skeptical committee, because the document will be forwarded and read without you in the room. Lean less on momentum, more on the argument standing on its own.
- **Individual leaders (Voices).** Corpus, authorship, the network. The job is being coherent, found, and connected. The writing serves a person's own body of work, which raises authorship care further. The company voice in this skill is distinct from a given Voice's own constitution (see [[alan-voice]]); what is shared is plain prose, the refusals, and authorship care.

## Working the three jobs

**write:** Hold the voice, style, refusals, and case-making above. Tune the nouns to the audience. Default to prose, short sentences, generous space, no em dashes. Lead with the gift, concede honestly, reframe the question, sell relief. State the problem and the price once. When done, silently run the [audit checklist](references/audit-checklist.md) over your own draft and fix any "no" before returning it.

**audit:** Do not rewrite wholesale first — diagnose, then fix, preserving the author's meaning. Work the [audit checklist](references/audit-checklist.md) line by line. Return the fixed copy, then a short list of what you changed and why. The headline fixes: replace em dashes with periods, shorten performing sentences, run every abstract or technical word through the costume test, turn hype into relief, add a missing concession and a "who this is not for," cut overclaiming, remove any urgency or scarcity, remove any implied faked authorship or AI doing the discernment or care, flag unsourced substantive claims, and collapse a problem or price stated more than once.

**prompt:** Produce a ready-to-paste block for a downstream Claude skill or agent. Use the templates in [references/prompt-blocks.md](references/prompt-blocks.md) — a "write in the Movemental voice" block and an "audit toward the Movemental voice" block. Adapt the audience nouns to the brief.

See [references/before-after.md](references/before-after.md) for worked before/after pairs across each failure mode.

## The last word, in the voice it asks for

Do not try to sound smart. Try to be understood, and be honest, and be kind. That is what earns the trust we are actually selling.
