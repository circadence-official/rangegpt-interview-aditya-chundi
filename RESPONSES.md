# Candidate Responses

## Cross-Stack Questions

### Question 1
> The React app currently fetches models with a cached query hook and renders a list of cards. If the leaderboard view you've built becomes the primary landing page, what caching and invalidation strategy would you recommend on the frontend, and what affordances from your API would make that strategy easier to implement?

[Since the leaderboard is the main view I built, I would treat it as a high-priority, frequently used endpoint. I would cache it on the frontend using a key based on the benchmark (for example, “leaderboard + benchmark name”), so each leaderboard is stored separately.

At the same time, I would make sure it stays fresh. Whenever a new benchmark result is added, I would refresh only the affected leaderboard instead of reloading everything. This keeps the experience fast while still showing updated rankings.

From the API side, I designed the endpoint to be simple, predictable, and filterable by benchmark. I also included timestamps, which gives the frontend a clear signal of how recent the data is. That makes caching reliable without adding unnecessary complexity.]

### Question 2
> Looking at how the app currently handles loading and error states per request, what would you change about your summary endpoint's response shape — or split into multiple endpoints — to give the frontend a better experience when one benchmark's data is slow or unavailable?

[For the summary endpoint, my goal is to make sure the user always sees something useful, even if some data is slow or missing.

Instead of returning one big response that fails completely, I would structure the response so each benchmark is handled independently. That way, if one benchmark is delayed, the others can still be shown immediately.

In simple terms, the system should never “go blank” just because one piece of data is slow. It should show what it has and clearly indicate what is still loading or unavailable.

Since my current implementation already groups results by benchmark, it can easily support this kind of partial response without major changes.]

### Question 3
> If a later iteration needed to show near-real-time updates whenever a new benchmark run completes, what pattern would you suggest instead of the current fetch-on-mount approach, and what would that require you to add on the backend?

[Right now, results are added through a POST API, and the frontend would normally fetch data when the page loads. To make this more dynamic, I would move to a real-time update approach.

For example, when a new benchmark result is added, the backend can immediately notify the frontend using WebSockets or a similar mechanism. The frontend can then update the leaderboard and model summary instantly.

This avoids constant polling and makes the system feel much more responsive. Since I already separated result storage from leaderboard logic, adding this real-time layer would be a natural next step without changing the core design.]

## Notes (optional)

[I focused on building the core backend pieces that directly support the product need: storing benchmark results, tracking history, ranking models, and summarizing performance across benchmarks.

One thing I paid attention to was consistency. For example, both the leaderboard and summary use the most recent run, so the numbers match and avoid confusion.

I also made sure the design is flexible. Benchmarks are not hardcoded, so new ones can be added without changing the database structure.

If I were to extend this further, I would focus on performance and scale, things like indexing, pagination, and caching, so the system remains fast even with a large number of models and historical runs.]