# Interview — 2026-06-03 (Session 14: Comprehensive All-Topics Review)

- **Role**: Semi-Senior iOS Swift Developer
- **Level**: Semi-Senior (target)
- **Candidate**: Joan Silva
- **Mode**: Realistic simulation, comprehensive all-topics review
- **Topics covered**: Architecture (Repo/Service/UseCase), Design Patterns (Strategy, Singleton), Swift Language (`some`/`any`, property wrappers), Memory & ARC (Timer), Swift Concurrency (async let vs TaskGroup), Security (Keychain), Testing (Swift Testing), System Design (offline-first)
- **Questions asked**: 11 (Q1 main + Q11b follow-up)
- **Veredicto**: **Does Not Qualify as Semi-Senior (borderline, lower-end)** — same as session 13. Macro judgment solid, execution depth loose.

---

## Q&A Summary (Session 14)

### Q1 — Architecture / Repo vs Service vs UseCase
**Question**: Fetch user data from network + cache locally. Separate Repository, Service, UseCase. What does each do?
**Answer category**: Improvised
**Notes**:
- Said UseCase is Domain layer with business logic ✓
- Said Repository is Data layer that returns DTOs ✗ (inverted: Repository should return domain entities, Service returns DTOs/raw responses)
- Said Service is concrete implementation (remote or cache) ✗ (Service is one concrete implementation; Repository abstracts WHERE data comes from)
- **Core issue**: doesn't articulate abstraction vs implementation separation. Erosion confirmed from session 13 where he had this backwards.

### Q2 — Design Patterns / Strategy
**Question**: Three payment methods (card, PayPal, Apple Pay). How structure to avoid switch? What pattern?
**Answer category**: On Point
**Notes**:
- Named Strategy correctly (first time generating own example in 4 sessions — very good)
- Explained problem solved (avoid switch statement)
- Correct implementation: protocol + conformance
- Mentioned abstraction benefit (client doesn't know concrete type)
- Anchored in real experience (Planifi-K). **Pattern locked in** per progress carry-over.

### Q3 — Swift Language / some vs any
**Question**: Difference between `some View` and `any View` in SwiftUI? When use each?
**Answer category**: Don't Know → Reasoning
**Notes**:
- Initially "I don't know" (honest)
- When asked to reason with names: guessed "some = particular view, any = anyone" — has right intuition (specific vs general) but lacks mechanism
- Missing: `some` = opaque type (compile-time, one concrete type), `any` = existential (runtime, boxing, heterogeneous)
- Uses `some View` daily without underlying mental model.

### Q4 — Memory & ARC / Timer retain cycle
**Question**: Closure capturing `self` inside a timer in VM. Walk retain cycle and fix.
**Answer category**: Could Be Better
**Notes**:
- Correctly identified cycle: VM→Timer→(closure)→VM ✓
- Mentioned weak self as fix ✓
- Missing: Timer still runs as "zombie" after weak self prevents VM leak; needs `invalidate()` call to stop it. Nuance from session 12 that didn't stick.

### Q5 — Swift Concurrency / async let vs TaskGroup
**Question**: 3 independent network requests in parallel. Difference between async let and TaskGroup? When use each?
**Answer category**: Could Be Better
**Notes**:
- TaskGroup "used to wait all tasks running in parallel" — vague, doesn't specify dynamic count advantage
- async let "let task run in parallel and use single await" — correct idea but missing use-case distinction
- Missing: async let = fixed count upfront (ergonomic), TaskGroup = dynamic count at runtime (flexible). Also missed structured cancellation + iteration.

### Q6 — Security / Keychain token storage
**Question**: Store access token + refresh token. What to use? Specific considerations for each?
**Answer category**: Could Be Better
**Notes**:
- Correctly chose Keychain (best practice)
- Missing Semi-Senior depth: access vs refresh need **different access levels**
  - Access: shorter-lived, lower threshold → `kSecAttrAccessibleAfterFirstUnlockThisDeviceOnly`
  - Refresh: higher-value, biometric gating + Secure Enclave → `kSecAttrAccessibleWhenUnlockedThisDeviceOnly + SecAccessControl.userPresence`
- Critical for MFA role; erosion confirmed from session 12 (15-day recall loss). Needs daily drill.

### Q7 — Testing / Swift Testing mock structure
**Question**: Test LoginViewModel (async, can succeed/fail). Structure mock and test with AAA.
**Answer category**: Improvised (syntax errors blocking execution)
**Notes**:
- Wrote code (improvement vs session 13 pseudo-code) ✓
- **Syntax errors**:
  - `@test` → should be `@Test` (capital T)
  - `#expected()` → should be `#expect()`
  - Missing `async throws` on function signature
  - Mock as Spy (OK) but didn't show error handling or assertion on result
- Structure (AAA) correct in intent
- **Pattern**: avoids code writing, which costs points in whiteboard. Needs repetition until automatic.

### Q8 — Architecture / SwiftUI Navigation
**Question**: How handle navigation from ViewModel? Where does navigation logic live?
**Answer category**: Could Be Better
**Notes**:
- Option 1: `.navigation()` modifier in view (directional, simplified name for `.navigationDestination()`)
- Option 2: Router pattern for complex cases (testable independently)
- Missing **idiomatic SwiftUI pattern** (modern 2023+): VM exposes `@Published var route: Route?`, View observes with `.navigationDestination(item:)`. Testable AND simple (no Router needed for most cases).
- Chose Router without mentioning canonical pattern; implies over-engineering for simple cases.

### Q9 — Design Patterns / Singleton anti-pattern
**Question**: What's wrong with Singleton pattern? Don't just say testability.
**Answer category**: Could Be Better
**Notes**:
- Identified: "one part of code could modify object and you don't know" — touches on shared mutable state concern
- Missing **core architectural problem**: hidden dependencies. Using `.shared` inside methods means:
  - Can't grep to find all usages until runtime
  - Dependencies hidden from init signature
  - Architectural coupling worse than testability issue
- This is the key insight that distinguishes semi-senior understanding.

### Q10 — Swift Language / Property wrappers mechanism
**Question**: @State and @Published work how under the hood? What's the mechanism?
**Answer category**: Vague/Don't Know
**Notes**:
- Answered "create getter and setter to not pay attention to object lifecycle" — effect, not mechanism
- Missing: property wrappers are **structs with `wrappedValue` and `projectedValue` properties**
  - `@State var name = "foo"` desugars to `var _name = State(wrappedValue: "foo")`
  - `$name` = projected value (Binding), `_name` = wrapper instance
- Uses `$x` and `_x` symbols daily but doesn't understand struct model
- **Critical gap**: blocks custom wrapper writing and debugging. Needs code drill.

### Q11 — System Design / Offline-first sync
**Question**: Build offline-first sync. Actions while disconnected, sync when online. Layers, offline behavior, reconnect behavior?
**Answer category**: Could Be Better
**Notes**:
- Correct macro: Cache abstracts offline so upper layers unaware ✓
- Missing execution detail (depth for semi-senior):
  - Ordering: which requests sync first?
  - Batching: individual or batch?
  - Backoff with jitter: retry strategy
  - Reachability: how detect connectivity change (NWPathMonitor)?
  - BGTaskScheduler: handle app termination + resume
  - Idempotency: what if same request retries twice?
  - ACK protocol: confirm server received?
  - Conflict resolution: server data changed while offline?

### Q11b — System Design follow-up / Sync strategy
**Question**: User offline 2 hours, makes 50 POST requests. When online, sync strategy? What can go wrong?
**Answer category**: Could Be Better
**Notes**:
- Identified batching to avoid network saturation ✓ (good instinct)
- Missing: ordering (older first?), idempotency (retry if partial fails?), error handling per-request, atomic vs partial success acceptance
- Macro sound, execution detail shallow.

---

## Patterns Observed (Session 14)

**Positive**:
- Strategy pattern finally locked in (was weak 4 sessions ago, now On Point)
- Code writing resumed after session 13 avoidance
- Architecture thinking structured (layers correct) even if boundaries fuzzy
- Honest admission of gaps (doesn't invent)

**Negative**:
- Repo vs Service confusion persists (fundamental architecture knowledge needed for any role)
- Property wrappers mechanism missing (uses daily, doesn't understand)
- Keychain details erosion (15 days post-learning, needs daily drill per session 12)
- Swift Testing syntax avoidance (defaults to pseudo-code under pressure)
- System design macro only (missing execution checklist)

## Next Session Focus (Critical Priority)

1. **Property wrappers code drill** (1h) — write custom wrapper to understand `wrappedValue`/`projectedValue` struct model
2. **Repo vs Service clarity** (30m) — hammer abstraction vs implementation distinction with code example
3. **Keychain daily drill** (2 weeks) — memorize access/refresh token accessibility mappings
4. **Swift Testing full suite** (1h) — success + error cases, correct syntax, real mock structure
5. **some vs any applied** — scenario-based until automatic
6. **System design checklist** — 5-6 elements (ordering, batching, backoff, reachability, idempotency, ACK)

## Q&A

### Q1 — Real Experience / Architecture
**Question**: Most technically challenging feature you led at Planifi-K — decisions, things discarded, outcome.
**Answer category**: Could Be Better
**Notes**:
- Partial STAR: S (no architecture, inherited MVP) and T (propose scalable architecture) reasonable. A: MVVM + Clean (domain/business/presentation) + migration `@Published` → Observation. R weak — "solid and scalable application" without metrics, no concrete impact (perf, releases, regressions).
- Clean nomenclature: said "business" — the canonical layer is **data** (or infra). Possible confusion to verify.
- Mentioned that they **discarded tests in the first stage** to focus on the product. Defensible decision but contradicts the CV bullet ("TDD, 80% coverage"). Inconsistency to watch — don't follow up now, just note.
- Autonomy: says "I proposed" — good, own decision, not "the lead decided".
- Did not go deep into discarded trade-offs (why MVVM and not MVI? why Observation already, given deployment target?).

### Q2 — Frameworks / SwiftUI (Observation)
**Question**: What does `@Observable` do under the hood and what's the performance difference vs `@Published`/`ObservableObject`?
**Answer category**: Vague
**Notes**:
- Answered **only the ergonomics** (less verbose, mark the class vs each property) and the availability (iOS 17). Completely ignored the performance question and the "what does it do under the hood".
- Did not mention: tracking at the level of **property access** (Observation observes only the props the view read), vs `ObservableObject` which fires `objectWillChange` on ANY `@Published` change → every observing view re-evaluates `body`.
- Did not mention that `@Observable` is a macro that synthesizes accessors with `_$observationRegistrar`.
- Known pattern from progress: "what" intuitive, "how/why" incomplete.
**Follow-up**: depth follow-up focused on performance (Q2b).

### Q2b — Frameworks / SwiftUI (re-render)
**Question**: VM with 10 props, SubView reads 1. Another changes. Re-render with ObservableObject vs `@Observable`?
**Answer category**: Could Be Better
**Notes**:
- `@Observable`: correct, no re-render because that prop was not accessed.
- ObservableObject: hesitated but got directionally correct ("would have to redraw everything"). Did not articulate the mechanism (`objectWillChange` fires on any `@Published`, invalidates all observing views).
- Better than Q2: moved from not knowing to getting the "what". Still missing the "why" of the mechanism.

### Q3 — Security / Token storage
**Question**: Where to store access + refresh token on iOS and why discard the rest?
**Answer category**: Could Be Better
**Notes**:
- Correctly discarded UserDefaults ("it's not secure, easily accessible"). Did not articulate why: UserDefaults → flat plist in `Library/Preferences`, accessible if the device is jailbroken or via unencrypted backup.
- Chose Keychain but hedged with "we're in a spike" — dodged the question. From semi-senior you expect the direct canonical answer.
- **Did not mention**: encrypted by the OS, hardware-backed with Secure Enclave on modern devices, access control with `kSecAttrAccessible*` (`.whenUnlocked`, `.afterFirstUnlock`, `.whenUnlockedThisDeviceOnly` — disables iCloud sync), `SecAccessControl` for biometric gating.
- **Did not distinguish access vs refresh**: idiomatic pattern is refresh in Keychain with strict ACL + biometrics if applicable; access can live in memory (short TTL) or also in Keychain.
- Did not discard other options (unencrypted filesystem, Core Data without encryption, files in Documents).
- Observed pattern: when he doesn't have the answer locked in, he retreats to "we're analyzing it at work" instead of reasoning about the problem.

### Q4 — Error handling / function signature (carry-over session 9)
**Question**: `findBook` by ISBN — `Book`, `Book?`, `Result`, `throws`? Justify.
**Answer category**: On Point
**Notes**:
- **Correction retained**: in session 9 he chose `throws` importing context from Planifi-K. This time he chose **`Book?`** — the canonical answer. Correct reason: a single failure condition (not found), no need to differentiate errors.
- About `throws`: correct criterion, leaves it as an option conditional on more failure modes. Good.
- **Weak Result dismissal**: "we don't use it in the project" — weak reason. Should reason: Result makes sense when the error is a **storable value** (cache the last result, propagate across non-async boundaries), not out of project habit.
- Clear improvement vs session 9 — internalized the rule "one obvious failure reason → Optional".

### Q5 — Design patterns / Singleton (drill round 2, carry-over session 9)
**Question**: Define Singleton + is EnvironmentObject a Singleton?
**Answer category**: On Point
**Notes**:
- Singleton: definition correct at the idea level (single instance, global access). Missing technical precision: private init, static `.shared` property, single-instance guarantee via static lazy let. Acceptable for Semi-Senior.
- **EnvironmentObject: correction retained**. In session 9 he confused it with Singleton; this time he identified it as DI without hesitation. Reason directionally correct though imprecise: in SwiftUI the EnvObj is injected into the environment tree (`.environmentObject(_:)`) and descendants read it — it's scoped to the subtree, not global, and there can be multiple instances in different subtrees.
- **Clear internalization** of the pattern-vs-framework drill — the session 9 confusion is corrected.

### Q6 — Design patterns / Strategy (drill round 2)
**Question**: Define Strategy + two distinct iOS examples.
**Answer category**: Vague
**Notes**:
- **Weak definition**: described the mechanism ("instead of a switch we pass it an implementation") but not the essence of the pattern: family of interchangeable algorithms behind a common interface, swappable at runtime. Repeated pattern from session 5 and 9: knows the when, fails the what.
- **Only gave ONE example of the TWO requested**: PaymentProcessor — the same example we used in session 4. Did not generate his own. Indicator of the already-observed pattern: weak at inventing original iOS examples without pre-built context.
**Follow-up**: ask again for the second example (Q6b).

### Q6b — Strategy (second example)
**Question**: Give me the second example, no payments.
**Answer category**: Don't Know
**Notes**:
- "Nothing comes to mind." Honest, no bullshit (positive). But confirms the pattern: Strategy as a name is not fluid, he doesn't associate it with everyday cases.
- Canonical iOS examples he could have given: sorting/filter strategies (configurable `SortDescriptor`), compression strategies, image cache eviction policies (LRU/LFU/FIFO), networking retry strategies, JSON encoding strategies (`JSONEncoder.KeyEncodingStrategy`), animation curves.
- Skill rule: 2 consecutive failures on the same subtopic → skip and move on. Cover at close.

### Q7 — Swift language / Property wrappers under the hood
**Question**: What is a property wrapper, what does the compiler generate, `wrappedValue` and `projectedValue`?
**Answer category**: Vague
**Notes**:
- Answered **only the visible outputs** (`$x`, `_x`) without explaining the mechanics. Did not mention:
  - It's a `struct`/`class` marked with `@propertyWrapper`.
  - Requires a `wrappedValue` property (what it returns when you access `x`).
  - Optional `projectedValue` (what `$x` returns).
  - `_x` is the **wrapper instance itself**.
  - The compiler transforms `@MyWrapper var x: Int = 0` into `private var _x = MyWrapper(wrappedValue: 0)` + getter/setter delegating to `_x.wrappedValue`.
- Confuses "generates getter/setter" with "is sugar over composition": it doesn't synthesize accessors, **it's an indirection to an external struct**.
**Follow-up**: deeper follow-up on the concrete mapping (Q7b).

### Q7b — Property wrappers / `@State` mapping
**Question**: `count`, `$count`, `_count` in `@State` — what is each one concretely?
**Answer category**: Vague / partial Don't Know
**Notes**:
- `$count`: gave the **use case** (two-way binding from the view to a VM property) without saying what it is. Correct answer would be: `$count` is `State<Int>.projectedValue`, which returns a `Binding<Int>`.
- `count`: did not mention it. It's `State<Int>.wrappedValue` (access to the wrapped `Int`).
- `_count`: "I don't remember" — explicit Don't Know. It's the **wrapper instance itself** (`State<Int>`).
- Known pattern: uses property wrappers daily, has not internalized the underlying mental model. Confirms the "modern fundamentals" gap noted in session 9.
- Skill rule: two weak answers in a row on property wrappers → skip topic, log and move on.

### Q8 — Architecture / SwiftUI navigation (carry-over session 8/9)
**Question**: List → detail → checkout. How do you model navigation, what API, where does the decision live?
**Answer category**: Could Be Better
**Notes**:
- Chose **Router/Coordinator** with good criteria: testability + deeplink support (showed forward vision, +autonomy).
- Correctly dismissed `.navigationDestination` as not-scalable, but the dismissal is partial: the modern idiomatic API in SwiftUI is `NavigationStack(path:)` + `.navigationDestination(for:)` with a router managing the `path`. It's not a "vs": the Router uses that API internally.
- **Did not get concrete**: did not mention what the Router looks like (`@Observable` class with `path: NavigationPath` or `[Route]`, `push`/`pop` methods), nor how to model the Route (enum `case checkout(Product)` with associated value to pass the product).
- **Did not close where the decision lives**: said "neither in View nor in VM" but did not complete: typically the View fires an intent to the VM, the VM calls the injected Router, or emits an event the Router catches.
- Known pattern: macro correct, concrete mechanics weak.

### Q9 — Swift Concurrency / AsyncSequence (carry-over session 9, reasoning exercise)
**Question**: What does the name AsyncSequence tell you, what would you relate it to? Reason without definition.
**Answer category**: Could Be Better
**Notes**:
- **Improvement over the session 9 focus**: when he doesn't know a topic, he reasoned by the name instead of asking to skip or saying "I don't know". Got to "asynchronous sequence → information stream" — directionally correct.
- Vague comparison with other languages: said "it also exists in Java" without naming Flow/Reactive Streams/RxJava or explaining the conceptual parallel.
- Did not mention: Swift protocol iterable with `for try await`, modern successor to Combine for one-by-one cases, typical examples (`URL.lines`, `NotificationCenter.notifications`).
- **Positive pattern**: worked the reflex of reasoning without complete info. Small win from the next-session focus of session 9.

### Q10 — System Design (mobile) / Offline-first sync (carry-over)
**Question**: Offline-first sync layer for real-time tracking. Components, persistence, conflicts, trade-off discarded.
**Answer category**: Could Be Better
**Notes**:
- Good elements: feature flag upfront (engineering hygiene), cache layer, local SQLite, retry loop, send on reconnect, delegate conflict resolution to the server.
- **Missing Semi-Senior depth**:
  - **Ordering**: did not mention that points must be sent in chronological order (FIFO queue) nor how that's guaranteed with monotonic local timestamps.
  - **Batching vs streaming**: battery/network trade-off not mentioned.
  - **Backoff**: said "retry every x time" — did not mention exponential backoff with jitter.
  - **Retry trigger**: fixed timer or reachability (`NWPathMonitor`)? Reachability is the idiomatic iOS choice.
  - **Background execution**: did not mention `BGTaskScheduler` nor that backgrounded apps have limited windows to upload data.
  - **Idempotency / ACK**: how does the client know the server received it so it can delete local? Idempotency key to avoid duplicates on retry.
  - **Why SQLite and not Core Data / SwiftData / file**: did not justify the choice.
- **Did not describe a discarded trade-off**: the question asked for it explicitly. Server-side conflict resolution isn't a discarded trade-off, it's the decision taken.

---

## Final Feedback (session close)

### Verdict

**Does Not Qualify as Semi-Senior (yet, borderline)** — Joan is at the edge between Semi-Senior junior and Semi-Senior consolidated. He has 8+ years of experience and shows solid criteria for making architecture decisions, but technical depth in fundamentals is below the expected level. The gap is not about experience but about **underlying mental model**: he uses APIs every day (property wrappers, Observation, Keychain) without internalizing how they work underneath, and that shows the moment the interviewer asks the "why/how" instead of the "what".

### Strengths

- **Architecture criteria**: navigation with Router for testability + deeplink (Q8), MVVM + Clean in the migration (Q1), recognizes scalability as a criterion.
- **Cross-session internalization**: corrected Singleton vs EnvironmentObject (Q5) and Optional vs throws in findBook (Q4) — patterns he failed in session 9, now solid.
- **Reasoning without information**: AsyncSequence (Q9) — got to "stream" by the name. Worked the reflex we asked for in session 9.
- **Honesty without bullshit**: when he doesn't know he says so ("nothing comes to mind", "I don't remember"). In a real interview this adds up — the interviewer prefers "I don't know" over making things up.
- **Autonomy**: in Q1 says "I proposed" (not "the lead decided"). In Q8 mentions feature flag and deeplink proactively.

### Areas to improve

- **Mechanics/internals of everyday APIs**:
  - Property wrappers (Q7/Q7b): did not explain what `wrappedValue`, `projectedValue` are, nor what `_x` represents. Vague + Don't Know.
  - Observation vs ObservableObject (Q2): answered ergonomics, not performance. The "why" of the change (tracking by property access vs global `objectWillChange`) is the point.
- **Patterns as a name**:
  - Strategy (Q6/Q6b): weak definition, only gave the canonical example (PaymentProcessor — the same one we used in session 4), could not generate his own. Don't Know on the second example.
- **Depth in mobile security**:
  - Token storage (Q3): chose Keychain but hedged with "we're in a spike", did not articulate ACL (`kSecAttrAccessible*`), Secure Enclave, nor distinguish access vs refresh token. For a job that requires MFA, this should be canonical.
- **System design depth** (Q10): macro correct, missed several components (backoff, reachability, BGTaskScheduler, idempotency, ordering). Did not describe a discarded trade-off despite the question asking for it.

### Per-topic breakdown (dominant category)

| Topic | Dominant category |
|---|---|
| Architecture (real exp + navigation) | Could Be Better |
| SwiftUI / Observation | Vague → Could Be Better (post-follow-up) |
| Security / token storage | Could Be Better |
| Error handling | **On Point** |
| Design patterns / Singleton | **On Point** |
| Design patterns / Strategy | Vague → Don't Know |
| Property wrappers under the hood | Vague + Don't Know |
| Swift Concurrency / AsyncSequence | Could Be Better |
| System design / offline-first | Could Be Better |

### STAR

In Q1 (the only real-experience question) the structure was partial: S and T clear, A enumerated, but **R weak** — "solid and scalable application" without metrics or concrete impact. Pattern already observed in session 9: closes without a quantified Result. For a real interview, the "Result" is what differentiates a story from anecdote: think metrics (crash-free %, release time, regressions, coverage, performance, adoption).

### Concrete recommendations for next session

1. **Property wrappers under the hood**: read proposal SE-0258 + 30 min building your own wrapper (`@Clamped`, `@UserDefault`). Practice verbalizing the difference between `wrappedValue`, `projectedValue`, `_var`.
2. **Observation framework deep dive**: understand the `@Observable` macro from the inside — `_$observationRegistrar`, tracking by property access. Compare with `objectWillChange` mechanically.
3. **Strategy as a name**: build yourself mentally 3-4 non-payment iOS examples (sorting strategies, cache eviction, retry strategies, JSON encoding strategies). Repeat until they come out without thinking.
4. **Security / canonical Keychain**: `kSecAttrAccessible*`, Secure Enclave, `SecAccessControl`, biometric gating, access vs refresh token storage. For the MFA-bound job, this is not optional.
5. **Mental system design checklist** for offline-first type questions: ordering, batching, backoff, retry trigger (reachability), background execution, idempotency/ACK, conflict resolution, persistence choice + justification.
6. **STAR-R**: in every experience-based answer, before closing ask yourself "what metric or impact do I close with?".

`progress.md` updated with session 10.

---

# Interview — 2026-05-18 (session 11, "fresh start, skip the green" mode)

- **Role**: Semi-Senior iOS Swift Developer
- **Level**: Semi-Senior
- **Candidate**: Joan Silva
- **Mode**: realistic simulation (no feedback during). Already-validated topics are marked 🟢 and skipped.

## 🟢 Already validated (not asked again this session)

From `progress.md` (sessions 1–10):

- Swift: value vs reference, weak vs unowned, error handling (signature choice)
- Swift Concurrency: async let, continuations, actors / `@MainActor`, Task cancellation
- SwiftUI: `@StateObject` vs `@ObservedObject`, view identity (`id` in ForEach)
- Architecture: MVVM (structure), MVVM testing, MVI macro, Coordinator navigation, Repository vs Service vs UseCase, Clean use case boundaries
- SOLID: SRP, OCP, LSP, ISP, DIP (all)
- Design patterns: Singleton (post-correction session 10), Factory, Decorator, TDD red-green-refactor
- Code quality: cyclomatic complexity

## 🎯 Topics to cover today (gaps)

1. Property wrappers internals (conceptual)
3. Strategy — own iOS examples
4. Observer / Adapter (weak patterns)
5. Token storage / canonical Keychain
6. SwiftUI List performance
7. MVP vs MVVM (unknown)
8. TDD — what to test and what not (unknown)
9. System design — new scenario (not tracking)
10. `some` / `any` applied

## Q&A

### Q3 — Design patterns / Strategy own examples (carry-over session 10)
**Question**: Two non-payment iOS examples, distinct areas.
**Answer category**: Could Be Better (partial — gave one of two)
**Notes**:
- Definition: better articulated than in session 10 ("eliminate switch by behaviors, protocol + implementations"). Progress.
- Example: Repository with multiple data sources (server / local / Firebase). Borderline Strategy — defensible (the "strategy" is how to fetch) but closer to the classic Repository pattern with composition.
- **Only gave ONE example of the TWO requested**, same as session 10.
**Follow-up**: Q3b asking for the second from a different area.

### Q3b — Strategy second example
**Question**: Second example, not data sources.
**Answer category**: Don't Know
**Notes**:
- "Nothing else comes to mind" — same outcome as Q6b session 10. Confirms: Strategy is not fluid as a name/mental tool.
- Possible examples he could have given: configurable sort comparators, cache eviction policies, image processing pipelines, retry policies, interchangeable formatters.
- Skill rule: 2 consecutive failures on same subtopic → skip and move on.

### Q4 — Security / Keychain — accessibility access vs refresh
**Question**: Which `kSecAttrAccessible*` for each + biometrics?
**Answer category**: Could Be Better
**Notes**:
- **Confused OAuth2 semantics with MFA flow**: described that the "access token" is just the intermediate challenge to request the second factor, and that the refresh is the only one persisted. In standard OAuth2: access = used on every API call (15 min), refresh = mints new access tokens (30 days). What he describes looks more like an "MFA challenge token" + final token.
- **Did not answer the concrete question**: did not name any `kSecAttrAccessible*` value. Expected:
  - Access token: `kSecAttrAccessibleWhenUnlocked` (or `AfterFirstUnlock` if used in background).
  - Refresh token: `kSecAttrAccessibleWhenUnlockedThisDeviceOnly` (never iCloud sync).
- **Biometrics for refresh**: yes, mentioned it — good. Standard pattern is `SecAccessControl` with `.biometryCurrentSet` or `.userPresence`.
- "I don't store the access token" — debatable. In real apps the access IS persisted to survive foreground/background without re-login during its TTL.
- Known pattern: confuses details when importing work context (Planifi-K MFA-bound) instead of reasoning about the canonical case.

### Q5 — Swift / some vs any applied (carry-over session 9)
**Question**: `makeAnimal()` → `some Animal` vs `any Animal`. When each one.
**Answer category**: On Point
**Notes**:
- Correct distinction with good example:
  - `some`: compiler knows the concrete type, consistent return (a single type).
  - `any`: existential, runtime, different types per branch (switch returning multiple).
- **Clear internalization from session 9** — he didn't know `some/any` in session 9, today he applies it with his own example. Notable improvement.
- Did not mention performance (no boxing in `some`, existential container in `any`) nor the iOS 16+ nuance for the `any` keyword. Optional details, not critical.

### Q6 — SwiftUI / List performance (weak since session 5)
**Question**: List with 5000 items lags on scroll, 4 things to check/change in priority.
**Answer category**: Could Be Better (3 of 4)
**Notes**:
- **3 solid points**:
  1. Optimize ItemView (Date formatter instantiated per render, AsyncImage for thumbnails with caching).
  2. **Improvement vs session 5**: detected the "giant VStack with ForEach inside" anti-pattern that breaks the laziness of List/LazyVStack. Real experience, sharp criterion.
  3. **Stable ID vs `.self`**: identified the animation bug when deleting an item by using `.self` with indices. Carry-over from session 5 internalized.
- **Missed 1 (the 4th)**: did not mention `.equatable()` or the Equatable-View pattern for skipping re-render (this was the specific gap from session 5). Also did not mention closures as inputs breaking the diff.
- Clear improvement vs session 5 where he had mixed threading with laziness ("send it to a Task"). Today he reasoned SwiftUI-native.

### Q7 — Testing / TDD — what NOT to test (previously unknown)
**Question**: What classes or parts wouldn't you unit-test and why? Criterion.
**Answer category**: Could Be Better
**Notes**:
- Answered in STAR-flavor format centered on Planifi-K: started by testing critical UseCases and VMs, left out E2E, snapshot tests, external SDKs and "internal state". Defensible decision at the project level.
- **Inconsistency with `joan_stories.md`**: gave "60% coverage in 10 months" — that metric corresponds to **Comdata** (Java→Kotlin migration). In Planifi-K the canonical stories say ~80% coverage. He mixed the two stories. In a real interview this shows and the interviewer could push back.
- **Did not answer the canonical question**: the question was "what kinds of code do NOT warrant unit tests" (general criterion), not "what did we leave out in my project" (particular decision). Expected answers: pure DTOs / data classes, framework code, generated code (Codable synth), trivialities (getters), declarative SwiftUI view code, glue/composition roots.
- Already-known pattern: imports work context instead of reasoning about the canonical case. Same observation as Q4.
- "Internal state" — vague. If he meant "implementation details", the criterion is "test behavior not implementation" — he didn't name it.

### Q8 — System Design / E-commerce push notifications
**Question**: iOS design of a multi-type, multi-channel push notification system. Components + flow.
**Answer category**: Skip (at candidate's request)
**Notes**:
- "Skip" — asked to pass. Since in a real interview you can't skip, flag at close as a topic to work on.
- Pattern already observed in session 9: he asks to skip when he doesn't know the topic (3 times that day). Came back.

### Q9 — Design patterns / Observer (weak since session 5)
**Question**: Pattern behind ObservableObject + `@Published` — which one and publisher/subscribers role.
**Answer category**: Could Be Better
**Notes**:
- **Correction retained vs session 5**: correctly named Observer. In session 5 he had confused it with "Observation" (framework). Today he separated them well.
- Shallow description: said "someone observes" without elaborating publisher/subscriber dynamics. Missing:
  - Subject = ObservableObject, exposes `objectWillChange` publisher.
  - Subscribers = views/any subscriber (`.sink`, SwiftUI observation).
  - Notification before mutation (will/did).
- Correct name + macro idea — enough for Semi-Senior in this subtopic. The rest is detail.

### Q10 — What If / Autonomy — critical bug in production Friday 5pm
**Question**: Checkout overcharge bug, lead on vacation, PO not answering. Step-by-step plan.
**Answer category**: Could Be Better
**Notes**:
- **Solid autonomy**: decides, does not retreat to "I ask the lead". Good for the job.
- **Correct mitigation**: feature flag off as first reflex — faster, less risk than a hotfix without QA.
- **Cross-functional criterion**: contact QA to validate bug and coverage. Good.
- **Missing concrete stepwise**: the question asked for "step by step 2 hours". Answered in principles, not in executive sequence:
  - Who's the real escalation path (manager, on-call, incident channel)
  - Estimate blast radius (how many users affected since when? Crashlytics / analytics / SQL)
  - Document the incident for postmortem
  - Communicate to stakeholders proactively, don't wait for them to ask
- **Plan B not addressed**: what if there is NO feature flag? Assumed it exists.

---

## Final Feedback (session 11 close)

### Verdict

**Qualifies as Semi-Senior (borderline, lower-end)**. Change vs session 10 (which gave "Does Not Qualify"): today there was clear internalization of several key points from previous sessions — `some`/`any` applied, Observer correctly named, List performance reasoned SwiftUI-native, stable ID identified. Autonomy and mitigation criterion in real scenarios are solid. There are still specific gaps but the operational baseline is enough for Semi-Senior. Not senior — the delta is still depth in internals and narrative consistency.

### Strengths

- **Cross-session internalization**: `some`/`any` (Q5), Observer (Q9), List performance with stable ID (Q6) — all points he failed before and came out clean today.
- **Autonomy and operational criterion** (Q10): feature flag as instinct, cross-functional QA, avoids patches without testing.
- **Detection of real anti-patterns** (Q6): giant VStack-ForEach breaking laziness — that's prod experience.
- **Honesty**: asks to skip when he doesn't know, doesn't make things up.

### Areas to improve

- **Strategy as a name/mental tool** (Q3/Q3b): second consecutive failure giving two distinct examples. Not internalized.
- **Canonical Keychain** (Q4): did not name any `kSecAttrAccessible*` value. Confused OAuth2 semantics with MFA flow. For the MFA-bound job, this remains a critical gap.
- **TDD what NOT to test** (Q7): answered "what we left out in my project" instead of the canonical criterion (DTOs, framework code, generated code, declarative view code).
- **Narrative consistency of stories** (Q7): mixed metrics — gave Comdata's "60% coverage in 10 months" as if it were Planifi-K's. In a real interview this shows. **Reread `joan_stories.md`** to lock in numbers per company.
- **System design**: asked to skip (Q8). Same pattern as session 9. Pending topic.
- **Stepwise in "what do you do" scenarios** (Q10): tends to answer principles, not actionable sequences.

### Per-topic breakdown (dominant category)

| Topic | Category |
|---|---|
| MVP vs MVVM | Could Be Better |
| Strategy own examples | Vague → Don't Know |
| Keychain access vs refresh | Could Be Better |
| `some` vs `any` applied | **On Point** |
| SwiftUI List performance | Could Be Better (3/4) |
| TDD what not to test | Could Be Better |
| System design push | Skip |
| Observer | Could Be Better |
| Autonomy what-if | Could Be Better |

### STAR

In Q7 he structured STAR but **R inconsistent** with `joan_stories.md` (mixed Comdata metric with Planifi-K). In Q10 STAR didn't apply (hypothetical) and he answered reasonably without it. Progress vs session 10: included a metric this time, even if from the wrong project.

### Recommendations for next session

1. **Reread `joan_stories.md`** before the next — lock in metrics per company (Comdata 60% / 10 months, Planifi-K 80% coverage / 200+ devices / 20 releases per year).
2. **Mental iOS Strategy playbook**: get yourself 3 non-data-source examples — sort comparators, retry policies, formatters. Until they come out automatic.
3. **Keychain cheat sheet**: `kSecAttrAccessible*` values, `SecAccessControl` with biometrics, rule "access = WhenUnlocked, refresh = WhenUnlockedThisDeviceOnly + biometry". Memorize for MFA job.
4. **TDD canonical criterion**: separate "what I don't test in my project" (particular decision) from "what kind of code doesn't warrant unit tests" (principle).
5. **Mental system design checklist**: push him to not skip. When he doesn't know, reason minimum components (receiving layer, dispatcher, queue, UI). Same focus as session 9.
6. **Stepwise in what-if**: when asked "what do you do step by step", answer with numbered sequence (1. I verify X. 2. I measure Y. 3. I communicate Z), not with principles.

`progress.md` updates now with session 11.

---

# Interview — 2026-05-18 (session 12, "refresh old + gaps" mode)

- **Role**: Semi-Senior iOS Swift Developer
- **Level**: Semi-Senior
- **Candidate**: Joan Silva
- **Mode**: realistic simulation. Explicit request: refresh old topics (not touched in 3-5 sessions) to verify retention + cover gaps from session 11.

## Plan for today

- **Refresh old** (validated ≥3 sessions ago, erosion risk):
  - Swift / weak vs unowned + Timer gotcha (session 1-2)
  - Swift Concurrency / cooperative cancellation (session 1)
  - SOLID LSP (crystallized session 7)
  - Repository vs Service vs UseCase (session 6)
  - Conceptual continuations (session 2)
- **Carry-overs from session 11**:
  - Canonical Keychain (recently explained in class, verify lock-in)
  - TDD canonical criterion (what's not tested by principle)
  - iOS Strategy playbook (3rd attempt)
  - What-if stepwise (numbered sequence)
  - System design no-skip

## Q&A

### Q1 — Refresh: weak vs unowned + Timer gotcha (session 1-2)
**Question**: VM with `Timer.scheduledTimer` + closure using `self`. Retain cycle? Chain and fix.
**Answer category**: On Point
**Notes**:
- Identified the correct chain: VM → Timer → closure → VM.
- Fix 1: `[weak self]` in the closure. Correct.
- Fix 2: invalidate the Timer in the VM's `deinit`. Correct concept, did not remember the exact name (`invalidate()`) and admitted it. OK honesty.
- **Retention confirmed** — 6 days after session 1, the gotcha is still locked in.

### Q2 — Refresh: Swift Concurrency / cooperative cancellation (session 1)
**Question**: Does cancelling a Task stop the code immediately?
**Answer category**: On Point
**Notes**:
- "It's not automatic, a signal is sent, if the function doesn't ask it keeps going until done." Correct.
- Mentioned the cost: wasted processing. Correct.
- Did not mention: async URLSession respects cancellation automatically, `Task.isCancelled` flag vs `try Task.checkCancellation()` which throws `CancellationError`. Optional details.
- **Retention confirmed** since session 1.

### Q3 — Carry-over: canonical Keychain access vs refresh (post-explanation between sessions)
**Question**: Specific `kSecAttrAccessible*` values for access and refresh + biometrics.
**Answer category**: Could Be Better
**Notes**:
- **Internalized the access/refresh distinction** (15 min vs long life, refresh → mint new access). Well explained — the cross-session lesson worked.
- **Only named 2 of the 4 canonical values**: `WhenUnlockedThisDeviceOnly` and `AfterFirstUnlock`. Without mapping them to access/refresh nor justifying why.
- **Did not answer biometrics** — explicit question ignored. The cheat sheet was: refresh with `SecAccessControl` + `.userPresence` (biometrics with passcode fallback); access without biometrics (unjustified friction for 15 min TTL).
- **Partial retention** of just-taught material. Next session re-ask to validate real lock-in (not immediate recall).

### Q4 — Refresh: SOLID / LSP (crystallized session 7, 3 days ago)
**Question**: Define LSP + violation example.
**Answer category**: On Point
**Notes**:
- Clear definition with the key phrase: "they must comply with the protocol, not just compile". The insight that crystallized in session 7 is locked in.
- Example: the canonical `SilentBrokenStorage` (save does nothing, load always returns the same). Same example as session 7 — deep retention.
- Closed with the correct consequence: "it compiles but the behavior is inconsistent with what the app expects".
- **Retention confirmed** — 3 days post-crystallization, still solid.

### Q5 — Refresh: UseCase vs Repository vs Service (session 3/6)
**Question**: Responsibilities of each + login scenario with MFA + token.
**Answer category**: Could Be Better
**Notes**:
- **UseCase**: correct description — orchestrates the flow's logic, calls the layers below. Applied the MFA flow learned between sessions (mfa_token, second step, token saving). Out-of-band internalization of the class working.
- **Repository**: borderline description — said "hit the server directly or wrapper against a library". That's closer to **Service** than to **Repository**.
- **Service**: **did not mention it as a separate layer**. The question asked for the three. Partial erosion vs session 6 where the Repo/Service separation was clear.
- Canonical missing:
  - Repository = abstracts **where from** (local, remote, mixed). Returns domain entities.
  - Service = puts the bytes on the wire. HTTP, parsing, network retries. Transport detail.
- Token storage: said "ask the repo to save it" — conventionally separated in a dedicated `TokenStorage` (Keychain abstraction), not mixed with the AuthRepository. Detail.
- **Partial erosion detected** — the Repo vs Service line (which crystallized in session 3, confirmed in session 6) blurred. Re-ask next session.

### Q6 — Strategy own examples (3rd attempt)
**Question**: Two iOS examples, no payments, no data sources.
**Answer category**: Could Be Better (1 of 2, but original example)
**Notes**:
- **New example**: map/filter with function — higher-order function as strategy. **Conceptually correct and original** (not canonical from previous ones). Progress vs session 10 and 11.
- Second example: cut off with "another example" without completing. Third consecutive failure giving 2 examples.
- Qualitative change anyway: no longer repeats PaymentProcessor / data sources. Starting to generate own examples. Next time should reach 2 without a hint.

### Q7 — Carry-over: TDD canonical criterion for what NOT to test
**Question**: Types of code that don't warrant unit tests, by principle.
**Answer category**: Could Be Better
**Notes**:
- **Improvement vs session 11**: now answers with **categories** ("libraries", "internal states", "enums") instead of "what we left out in my project". Correct framing change.
- Incomplete and somewhat imprecise list:
  - "Libraries" → OK (third-party code).
  - "Internal states" → if he meant "implementation details", correct. Vague.
  - "Enums" → OK if they're data enums without logic; but enums with computed properties do warrant tests.
  - "Queues" → ambiguous. If referring to DispatchQueue, OK (framework). If to data structures, no.
- **Canonical missing**: pure DTOs / data classes, generated code (Codable synth, macros), framework code (Apple APIs), declarative SwiftUI view code, glue / composition roots, trivial getters/setters.
- Partial progress — internalized the framing change but the canonical list is not mentally assembled yet.

### Q8 — What-if with numbered stepwise (carry-over session 11)
**Question**: Crash 0.5% users iOS 17.0 exact. Step-by-step plan, 4 hours.
**Answer category**: Could Be Better
**Notes**:
- **Correct format**: gave 4 numbered steps. Clear change vs session 11 where he answered with principles. Internalization of the focus.
- Shallow content:
  1. "I check logs" — without specifying what (stack trace, breadcrumbs, custom keys).
  2. "Identified the screen" — redundant, was already in the prompt.
  3. "Reproduce the error" — without naming the key angle (iOS 17.0 exact → simulator/device setup on that specific version).
  4. "Check memory usage" — premature without evidence pointing to memory.
- **Missing**: read symbolicated stack trace, identify what changed API-wise between 17.0 and 17.1+, estimate blast radius in absolute numbers (0.5% × total users), communicate to stakeholders, decide mitigation (FF off / hotfix / waiting room), regression test on iOS 17.0 before release.
- Progress in form, content still feels more reflex than executive plan.

### Q9 — System design in-app inbox (no-skip carry-over)
**Question**: In-app notification inbox, iOS components + where the badge state lives.
**Answer category**: Could Be Better
**Notes**:
- **Did not skip** — clear change vs Q8 session 11 and session 9. Progress on the "reason even if you don't know" focus.
- 4 reasonable components: VM, NotificationManager (~ UseCase/Repository), NotificationService (HTTP), local persistence. Defensible structure.
- **"Room service"** — slip from his Android background (Room is Kotlin's ORM). On iOS it would be Core Data / SwiftData / SQLite. Minor detail but fatigue indicator.
- Badge in VM — defensible but limited: if the badge lives in the VM, it only updates when that screen is mounted. For a global tab bar badge, better a central store/observable that the VM consumes.
- **Missing**: how the badge UPDATES (Combine / Observation / NotificationCenter), mark-as-read flow (optimistic? server-first?), pagination.
- Important qualitative change: broke the "skip" reflex.

### Q10 — Refresh: continuations (session 2)
**Question**: Bridge an old-callback-style SDK to async/await. What tool + what does it do?
**Answer category**: On Point
**Notes**:
- Named `withCheckedThrowingContinuation` (written "cotinuesWithCheckedThrow" — name slightly off, idea correct).
- Explained the mechanics: wrap the callback, wait for the callback, expose `try await` to the caller. Correct.
- Applied with a mini-STAR from his El Comercio experience.
- **Attention**: the El Comercio story is NOT in `joan_stories.md`. Risk of narrative inconsistency if he uses it in another interview.
- **Retention confirmed** since session 2 — 7 days later, still solid.

---

## Final Feedback (session 12 close)

### Verdict

**Qualifies as Semi-Senior (mid-range)** — up vs session 11 (lower-end borderline) and session 10 (Does Not Qualify). Today there was clear confirmation of **long retention** on old topics (Timer, cooperative cancellation, LSP, continuations) and **progress in format** on carry-overs (canonical TDD, what-if stepwise, no-skip in system design). Some gaps remain open but the progression track is validated.

### Strengths

- **Long retention confirmed** (Q1, Q2, Q4, Q10): four topics marked "ok" 5-7 days ago came out On Point. The session-feedback-retention loop works.
- **Broke the skip reflex** (Q9): for the first time in 3 sessions, tackled a system design without asking to skip. Reasoned components.
- **Changed framing in TDD** (Q7): moved from "what we leave out in my project" (session 11) to "what kinds of code by principle". Partial list but the mental shift occurred.
- **What-if with numbered format** (Q8): followed the stepwise request. Correct form even though content still shallow.
- **Keychain internalization between sessions** (Q3): correctly applied the mfa_token / access_token / refresh_token in Q5 without being prompted.

### Areas to improve

- **Keychain — partial recall** (Q3): named 2 of 4 `kSecAttrAccessible*` values, did not map them to access/refresh, did not answer biometrics. Recently-taught material, requires active review.
- **Repo vs Service erosion** (Q5): the separation that crystallized in session 3 blurred — he described Repo as "hit the server" (which is Service). Service not mentioned as a separate layer.
- **Strategy — 3rd failure giving 2 examples** (Q6): although the 1st was original (map/filter), got stuck without a 2nd.
- **What-if — shallow content** (Q8): correct format but the steps were generic ("review logs"). Missing the specific content of an incident investigator: read stack trace, blast radius in absolute numbers, mitigation decision.
- **System design depth** (Q9): did not skip but missing how the badge UPDATES reactively, mark-as-read flow, pagination.
- **"Room service"** (Q9): Android slip. Mind cross-platform nomenclature in iOS interviews.
- **El Comercio story outside `joan_stories.md`** (Q10): invented an experience. In a real interview, stick to the canonical ones.

### Per-topic breakdown

| Topic | Category | Comment |
|---|---|---|
| Timer + retain cycle | **On Point** | retention 7 days |
| Cooperative cancellation | **On Point** | retention 7 days |
| Keychain access vs refresh | Could Be Better | partial post-class recall |
| SOLID / LSP | **On Point** | retention 3 days, crystallized |
| UseCase / Repo / Service | Could Be Better | partial Repo↔Service erosion |
| Strategy 2 examples | Could Be Better | 1 of 2, first example original |
| TDD canonical criterion | Could Be Better | framing corrected, list incomplete |
| What-if stepwise | Could Be Better | form OK, content shallow |
| System design inbox | Could Be Better | no-skip, reasonable structure |
| Continuations | **On Point** | retention 7 days |

### Recommendations for next session

1. **Re-attack Keychain**: in 2-3 sessions re-ask the concrete mapping (`access → AfterFirstUnlockThisDeviceOnly`, `refresh → WhenUnlockedThisDeviceOnly + SecAccessControl.userPresence`). That's the only thing to memorize — 4 values and a mental rule.
2. **Refresh Repo vs Service**: the line that crystallized in session 3 ("Repo abstracts **where**, Service does the HTTP") is blurring. Re-ask.
3. **Strategy — assemble 2-3 closed examples**: map/filter (today's 1st, keep it) + retry policy + sort comparator. Memorize the triad.
4. **What-if: fill in the stepwise content**: practice with concrete scenarios. Each step must name ONE specific action with ONE artifact (stack trace, incident ticket, FF off, stakeholder message).
5. **System design lite**: build mental checklist of 5-6 elements to avoid falling short — components, global vs local state, sync mechanism, pagination, edge cases, persistence.
6. **Reread `joan_stories.md`** before each practice to avoid inventing experiences that aren't saved.

`progress.md` updating now.

### Q1 — Architecture / MVP vs MVVM (previously unknown)
**Question**: When MVP over MVVM and the other way around? Justify.
**Answer category**: Could Be Better
**Notes**:
- MVVM justified by testability (VM doesn't import SwiftUI). Correct idea but confusing verbalization ("test the View without mocking the view" — he meant test the VM without instantiating the View).
- **Superficial MVP dismissal**: "only if I have old versions without Observation". Weak premise — MVVM existed long before Observation (closures, KVO, Combine, RxSwift). The criterion is not Observation, it's the UI paradigm.
- **Real trade-offs not mentioned**:
  - MVP: Presenter owns the View via a protocol, explicit invocations (`view.showSpinner()`, `view.showError(_:)`). Strict UI state enumeration. More boilerplate, more predictable. Fits UIKit (imperative).
  - MVVM: VM exposes state, View derives. Less coupling, but "smart" View when the binding grows. Fits SwiftUI (declarative).
- "MVP is handled with callbacks" — imprecise. MVP uses direct invocations to a View protocol, not callbacks.




---

# Interview — 2026-06-03 (session 13)

- **Role**: Semi-Senior iOS Swift Developer
- **Level**: Semi-Senior
- **Candidate**: Joan Silva
- **Mode**: realistic simulation, no feedback during.
- **Topics to cover today** (from `progress.md` → Next session focus session 12 + open gaps):
  1. Repo vs Service (erosion check session 12)
  2. Keychain mapping access/refresh + biometrics (re-attack for lock-in)
  3. Strategy — 2 own iOS examples (round 4)
  4. Swift Testing — full LoginViewModel test (carry-over since session 7)
  5. System design — new scenario, no-skip
  6. What-if stepwise with specific content (action + artifact per step)
  7. Property wrappers under the hood (applied drill if time remains)

## Q&A

### Q1 — Architecture / Repository vs Service
**Question**: You're building a login feature with MFA. Who makes the HTTP call to the auth endpoint — the Repository or the Service? Explain the responsibility of each.
**Answer category**: 
**Notes**: 
