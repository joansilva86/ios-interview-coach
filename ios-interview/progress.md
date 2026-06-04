# iOS Interview Progress — Joan Silva

Target level: **semi-senior** Mobile/iOS Developer.
Stack per CV: Swift, SwiftUI, Core Data, Concurrency, MVVM/Clean, XCTest, Kotlin/Compose (secondary).

## Topic Mastery

| Topic / Subtopic | Confidence | Last Practiced | Notes |
|------------------|------------|----------------|-------|
| Swift / value vs reference types | ok | 2026-05-11 | Gets the result right but struggles to articulate the *why*. Confused "polymorphism = class" (classical OOP mindset); corrected to protocol-oriented. |
| Swift / weak vs unowned | ok | 2026-05-12 | Review: Timer gotcha correctly locked in. Identifies VM→Timer→closure→VM cycle and understands that closure self-invalidation prevents permanent leak. Still writes chained `self?.` instead of idiomatic `guard let self else { return }` — corrected this session. |
| Swift Concurrency / async let vs TaskGroup | ok | 2026-05-11 | Identifies sequential awaits problem and understands parallelism conceptually. Couldn't write the fix code without hints — didn't know `async let` syntax. Did understand "await wrongly positioned" trap. |
| Swift Concurrency / continuations | ok | 2026-05-12 | Knows the name `withCheckedContinuation` and general idea (suspend until old API finishes). Didn't know exact syntax. Never used in real code. Lacked use-case context (permissions, CLLocationManager, legacy SDKs) — covered this session. One-shot vs multi-shot callback distinction (continuation vs AsyncStream) was new. |
| Swift Concurrency / actors & @MainActor | ok | 2026-05-11 | Knows `Task { }` inherits context and `Task.detached` doesn't. Didn't mention effect on structured cancellation or task-locals (cover next session). |
| Swift Concurrency / Task cancellation | ok | 2026-05-11 | Identifies cancellation as cooperative, not automatic. Didn't know the mechanism (cancel() only sets flag, URLSession respects cancellation automatically, sync code requires explicit `try Task.checkCancellation()` in loops). |
| SwiftUI / @StateObject vs @ObservedObject | ok | 2026-05-12 | Correctly distinguished ownership: StateObject = view owner, ObservedObject = borrowed. Missed the nuance of "first init wins" — that `StateObject(wrappedValue:)` closure only evaluates once. Covered with `userId` changing scenario. |
| SwiftUI / view identity | ok | 2026-05-12 | Got the fix right (`id: \.id` in ForEach) and explained animation deletion bug reasonably. Did NOT see the stuck `@State` bug on its own — understood key phrase ("`@State` associates to SwiftUI-assigned identity") only after walking through code step-by-step. Reinforce with own scenario to lock in. |
| SwiftUI / List performance | weak | 2026-05-12 | Identified `LazyVStack`/`List` as main fix (good). Confused "don't block main" with "don't instantiate all" — wanted to move rendering to another thread (doesn't apply in SwiftUI). Suggested Task for parseMarkdown in body — incorrect (launches task per render). Didn't see `DateFormatter()` instantiated per render. Didn't know `.equatable()` or Equatable-View pattern; new to him that **closures as input** break SwiftUI auto-diff → all cells re-render. |
| Architecture / MVVM — structure and responsibilities | ok | 2026-05-12 | Correctly identified View / VM / Repository / DependencyContainer. **Failed to separate domain entities**: put email, password, attempts, and token in single `LoginModel` struct — SRP violation, concrete security problem (password in memory post-login), serialization issue. Confused Repository (abstracts *where* data comes from, domain contract) with Service/API (makes HTTP, parses JSON). Didn't decide who navigates (VM vs Coordinator vs view). Covered this session. |
| Architecture / MVVM testing | ok | 2026-05-12 | Has correct structural idea (Arrange/Act/Assert, configurable result mock, asserts on VM state). **Swift Testing syntax weak**: didn't remember `@Test` is attribute (wrote `test("name")` as function), didn't mark method `async`, **couldn't handle `@MainActor`** (was explicit part of question). Initial mock with `Bool withError` — rigid, showed him configurable `Result<...>` pattern. Knows Swift Testing by name, not by use. |
| Architecture / MVP | unknown | — | compare vs MVVM (binding vs explicit invocation), trade-offs |
| Architecture / MVI | ok | 2026-05-13 | Identified macro difference with MVVM (no reducer, View calls VM methods directly). Missed 2 key nuances: (a) state **immutable and single** that gets replaced, not `@Published` per field; (b) **strict unidirectional flow** via single `dispatch(intent)`. Trade-offs: more boilerplate but determinism and traceability. More natural in Kotlin/Compose; in Swift seen in TCA. |
| Architecture / Navigation in MVVM | ok | 2026-05-13 | Chose Coordinator and defended with testability. **Rejected VM for wrong reason**: said "VM coupled to UI can't be tested", but idiomatic SwiftUI pattern is VM exposes `@Published var route: Route?` and View observes with `.navigationDestination` — VM doesn't know SwiftUI, still testable. Showed him matrix: VM with flag (default SwiftUI), Coordinator (scalable, more UIKit), View direct (trivial). |
| Architecture / Repository vs Service vs UseCase | ok | 2026-05-13 | Offline-first scenario: correctly chose Repository with correct reasoning ("abstracts where data comes from"). **Applied Repository vs Service difference that cost him prior session** — good, it stuck. UseCase not mentioned (Clean concept), re-ask next session. |
| Architecture / Clean — use case boundaries | ok | 2026-05-13 | Correctly placed UseCase between presentation and data. Missed **specific responsibility**: one class per business action (`LoginUseCase`, `FetchUserUseCase`), coordinates repos, applies domain rules. Trade-off vs pure MVVM: more boilerplate but VM only orchestrates UI. Showed him code example. |
| Principles / SOLID — SRP | ok | 2026-05-13 | Correct concept ("one class, one reason to change"). In code review correctly identified violation (UserService with login + uploadAvatar + analytics). But struggled to give **concrete iOS example** without pre-built scenario. Still asks interviewer to provide context instead of generating it. Already violated SRP today with `LoginModel` (4 responsibilities) — good to reconnect. |
| Principles / SOLID — OCP | ok | 2026-05-13 | Identified PaymentProcessor switch violation and proposed protocol + polymorphism correctly. Wrote code but with loose details: poor naming (`processMethod(decimal:)`), inverted `if` logic, `Bool` as payment return (should be `Result`/`throws`). Applied Strategy without recognizing pattern name (see Design patterns). |
| Principles / SOLID — LSP | ok | 2026-06-03 | **Session 13**: Got right answer (silently failing violates LSP), but reasoning soft. "We discover in tests" vs post-condition violation. Strong intuition, articulation weak. From strong → ok (15-day retention, reasoning degraded). |
| Swift / whiteboard basic syntax | weak | 2026-05-13 | **New and critical pattern detected in session 6 writing code from memory**: (1) lowercase types (`protocol storage`, `class StorageImp1: storage`) repeated 4 times; (2) `let x: Tipo()` instead of `=`; (3) `let` for mock properties that need mutation from tests; (4) `throw` in functions without `throws` in signature (won't compile); (5) `try await` in functions that are NOT `throws` (VM catches internally). Knows theory, fails at typing. In whiteboard interview this costs several points. |
| Testing / Swift Testing syntax | weak | 2026-06-03 | **Session 13, carry-over from session 7**: Defaulted to pseudo-code ("I can't write, here are the steps"). AAA macro structure correct, syntax wrong: `expected()` vs `#expect()`, no `@Test` attribute. Mock as struct (value type). From ok (session 7) → weak (real execution fails, avoids code writing). **Long carry-over, critical fix.** |
| Principles / SOLID — ISP | ok | 2026-05-13 | Correct concept ("don't force client to implement what it doesn't use") and macro solution (split protocol). But when asked for "concrete problem" stayed abstract. Missed: bloated mocks, irrelevant changes breaking clients, implicit coupling. Showed him 3 concrete problems + fix with small protocols and multiple conformance. |
| Principles / SOLID — DIP | ok | 2026-05-12 | Understood concept (depend on abstractions, not concretes; inject protocols) and applied to VM. **Important: confused the name — called it "principle L"** instead of D. Classic memorization error. Corrected in session: L = Liskov (subtype substitution without breaking behavior), D = Dependency Inversion. Re-validate next session to confirm correction stuck. |
| Design patterns / Singleton anti-pattern | ok | 2026-05-13 | Got testability right (couples to concrete, violates DIP). Mentioned race conditions hesitantly — valid but secondary. **Didn't see bigger problem: hidden dependencies** (using `.shared` inside methods makes grep/init not show real module dependencies). Re-ask next session to confirm he internalized "hidden dependencies". |
| Design patterns / Strategy | ok | 2026-05-13 | Session 5 re-asked: got the when (avoid switch in `PaymentProcess`) but NOT the what (definition). Completed for him: family of interchangeable algorithms behind common interface. Still weak at formulating definitions; very strong at applying. |
| Design patterns / Observer | weak | 2026-05-13 | Session 5 said **"Observation"** when asked for pattern behind `@Published` + `ObservableObject`. Confused **framework** (Observation, iOS 17 with `@Observable`) with **classic pattern** (Observer). Clarified difference. Useful he knows both names but don't confuse them. |
| Design patterns / Factory | ok | 2026-05-13 | Got applied example right (DependencyContainer creates VMs with their deps). Missed the abstract "what". Completed for him: encapsulate object creation behind method/class so caller doesn't know construction details. |
| Design patterns / Decorator | ok | 2026-05-13 | Correct definition ("adds/modifies behavior without modifying class"). Gave him iOS examples: SwiftUI modifiers, repos with logging. Difference with Adapter: Decorator keeps same interface, Adapter changes it. |
| Design patterns / Adapter | weak | 2026-05-13 | Definition too generic ("adapt one type to another") — applies to Decorator and Wrapper. Clarified for him: translate existing class interface to what client expects. iOS example: wrapper adapting legacy callback-based SDK to `HTTPClient` async. |
| Design patterns / Builder, Abstract Factory, Command, State, Coordinator, Facade, Composite | unknown | — | — |
| Design patterns / Strategy (round 2) | weak | 2026-06-03 | **4th attempt session 13**: Hypothetical AspectFit/AspectFill → got it. Real project → "no". Persistent pattern: recognizes with frame, doesn't generate without guidance. Sessions 5/9/10/13 confirm weak. |
| Design patterns / Singleton (round 2) | ok | 2026-05-18 | **Corrected vs session 9**: identified EnvObj is not Singleton, linked with DI. Singleton definition acceptable at idea level. Lacks technical precision (private init, .shared static). |
| SwiftUI / Observation vs ObservableObject | 🟢 skip | 2026-05-18 | **User requested not to ask this topic again.** Don't include in future sessions. |
| Swift / Property wrappers under the hood | weak | 2026-06-03 | **Session 13**: Mechanism: answered "pointer" (Improvised). Code: "I don't remember" (Don't Know). Knows $x/_x symbols, not wrappedValue/projectedValue struct model. Critical — uses daily but no underlying model. Blocks custom wrappers. |
| Swift / Error handling — signature choice | ok | 2026-05-18 | **Corrected vs session 9**: findBook → Optional correctly. Internalized "one obvious failure reason → Optional". Result dismissal still loose ("we don't use it"). |
| Security / Token storage (Keychain) | weak | 2026-05-18 | Chose Keychain but hedged with "we're in a spike". Didn't mention ACL, Secure Enclave, access vs refresh distinction. High priority for MFA role. |
| Architecture / SwiftUI Navigation (with code) | ok | 2026-05-18 | Chose Router for testability + deeplink (good criterion). Missed concrete: NavigationStack(path:), Route enum with associated, where exactly decision lives. |
| System Design / Offline-first sync | weak | 2026-05-18 | Macro OK (cache, SQLite, retry, send on connectivity). Missed: ordering, backoff with jitter, reachability, BGTaskScheduler, idempotency, ACK. Didn't describe discarded trade-off despite explicit question. |
| Architecture / MVP vs MVVM | ok | 2026-05-18 | Macro correct (MVVM for SwiftUI by View/VM decoupling). MVP dismissal superficial ("only if no Observation"). Didn't mention real trade-offs (Presenter owns View via protocol, explicit invocations, fits UIKit). |
| Design patterns / Strategy own examples | weak | 2026-05-18 | **2nd consecutive failure (session 10+11)**. Definition OK but only gives one example (Repository/data sources today, Payments before). Don't Know on 2nd example. |
| Security / Keychain accessibility | weak | 2026-06-03 | **Session 13, 15 days post-learning**: "I don't remember" values. Recall erosion confirmed. Didn't address ACL, Secure Enclave, access/refresh distinction, biometrics. Critical for MFA role. **Needs daily drill 2 weeks.** |
| Swift / some vs any applied | ok | 2026-05-18 | **Clear internalization from session 9**: correct distinction with own example (single cat vs switch returning multiple). Missed performance (boxing) and iOS 16+. |
| SwiftUI / List performance (round 2) | ok | 2026-05-18 | 3 of 4 points solid: Date formatter, AsyncImage, VStack-ForEach anti-pattern, stable ID. Missed `.equatable()` and closures as inputs (session 5 gap persists). |
| Testing / TDD — what NOT to test | weak | 2026-05-18 | Answered project-decision (Planifi-K E2E/snapshot out) not canonical criterion (DTOs, framework, generated, view). |
| Design patterns / Observer (round 2) | ok | 2026-05-18 | **Correction retained vs session 5**: named Observer correctly, separated from Observation framework. Publisher/subscriber description shallow but adequate. |
| Autonomy / what-if critical Friday 5pm | ok | 2026-05-18 | Decides, doesn't hide. FF off as first reflex, QA cross-functional. Missed concrete stepwise and plan B without FF. |
| Swift / Timer retain cycle (refresh session 1-2) | strong | 2026-05-19 | **7-day retention confirmed**. VM→Timer→closure→VM chain correct. Fix: weak self + invalidate in deinit. |
| Swift Concurrency / cancellation (refresh session 1) | strong | 2026-06-03 | **15-day retention confirmed session 13**. "Sets a flag, task continues, need to check flag inside". Well articulated. Solid mechanism. |
| SOLID / LSP (refresh session 7) | ok | 2026-06-03 | **Session 13**: Got right answer (silently failing violates LSP), but reasoning soft. "We discover in tests" vs post-condition violation. Strong intuition, articulation weak. From strong → ok (15-day retention, reasoning degraded). |
| Swift Concurrency / continuations (refresh session 2) | strong | 2026-05-19 | **7-day retention confirmed**. Name slightly off (`continuesWithCheckedThrow`), idea and mechanics correct. |
| Architecture / Repo vs Service (session 3) | weak | 2026-06-03 | **Erosion confirmed session 13**: "repos give DTOs, service gives domain" (inverted). Retry logic in Service (partial). Doesn't articulate abstraction vs implementation. Re-ask. |
| Testing / TDD what not to test (session 11) | weak | 2026-05-19 | Shifted framing (project-decision → categories). Partial list: libs, internal state, enums, queues. Missed: DTOs, framework, generated, view, glue. |
| What-if stepwise (session 11) | ok | 2026-05-19 | **Format corrected**: 4 numbered steps. Content shallow (generic steps without specific artifacts). |
| System Design / no-skip reflex | ok | 2026-05-19 | **Broke the skip**. In-app inbox with 4 reasonable components. Slip "Room service" (Android). Missing sync mechanism, pagination, mark-as-read flow. |
| Security / Keychain mapping post-class | weak | 2026-05-19 | Partial recall: 2 of 4 values named, no access/refresh mapping, no biometrics. Re-ask in 2-3 sessions for delayed lock-in. |
| Testing / TDD — red-green-refactor | ok | 2026-05-13 | **Session 5, re-asked without hints**: got all 3 steps correct including refactor. Correction stuck. Next time force the why of refactor. |
| Testing / TDD — what to test and what not | unknown | — | balance between coverage and maintenance |
| Code quality / cyclomatic complexity | ok | 2026-05-13 | Knows what it measures (decision points: if/for/while/switch) and why it matters (testability, hidden bugs). Current project uses limit of 5 — good. **Lacked concrete techniques to lower it**: didn't name extract method or early return / guard. Explained with if-pyramid → guard cascade example. |

Confidence values: `strong` | `ok` | `weak` | `unknown`.

## Sessions

### 2026-05-11
- **Topics covered**: Swift / value vs reference types, Swift / ARC (weak vs unowned), Swift Concurrency (parallelism with async let, cooperative cancellation, Task vs Task.detached).
- **Asked / answered well**: 8 / 5 (correct results on 6, solid reasoning on ~4-5).
- **Weaknesses surfaced**:
  - **Strong pattern**: identifies concepts at high level but struggles to articulate the *mechanism* underneath. E.g.: knows cancellation is cooperative but "don't know what it does underneath"; knows sequential awaits are inefficient but can't write the `async let` fix without hints.
  - Confuses "polymorphism = class" (classical OOP). Swift is protocol-oriented. Corrected.
  - Calls any strong self capture "retain cycle", even one-shot callbacks (linear chain). Differentiate real retain cycle vs delayed deinit.
  - Didn't know `Timer` + `RunLoop` gotcha. Covered in depth this session, should lock in.
  - Never worked with timers in Swift (admitted).
  - Didn't know exact syntax of `async let` or `withTaskGroup`.
- **Patterns observed**:
  - Answers briefly. Gives correct result but rarely the why. Real interviews will push right there.
  - Good defensive heuristic ("when in doubt, weak self") — thought through, didn't memorize.
  - Excellent follow-up questions when something doesn't close (questioned if Timer was parent-child, identified await wrongly-positioned trap in async let). That's senior-level.
  - Honest when he doesn't know ("no sé"). Doesn't bullshit — helps a lot in interviews.
- **Next session focus**:
  1. **Force code-writing**: have him write Swift snippets more often, not just describe concepts. Explicitly ask "show me the code".
  2. **Deepen mechanisms**: each time he says "don't know what it does underneath", stop and explain; in next sessions re-ask to verify he internalized.
  3. **Continuations** (`withCheckedContinuation`, `withCheckedThrowingContinuation`): key for bridging old callback-based code to async/await. Never covered.
  4. **SwiftUI state** (all `unknown`): `@State` vs `@StateObject` vs `@ObservedObject` with practical scenarios.
  5. **Architecture / MVVM testing**: CV mentions TDD and XCTest — ask how he tests VM with async dependencies, protocol mocking, etc.
  6. Quick **Timer gotcha** review next session to verify it stuck.

### 2026-05-12 (second session of the day)
- **Topics covered**: SwiftUI state (`@StateObject` vs `@ObservedObject` + "first init wins" gotcha with changing params), view identity (`id:` in `ForEach`, stuck `@State` bug with indices), List performance (LazyVStack/List, cached DateFormatter, parsing outside body, `.equatable()` for re-render skip).
- **Asked / answered well**: 4 large questions with sub-questions. Correct result on ~3, articulated mechanism on only 1-2.
- **Weaknesses surfaced**:
  - **Persistent and increasingly visible pattern**: identifies the "what" intuitively, but the "why" / mechanism throws it incomplete, he invents it, or confuses with adjacent concepts. E.g.: "send it to a Task" to fix SwiftUI render issues (mixes threading with laziness/identity).
  - **Invented syntax**: `@StateObject lazy var vm = ...` — doesn't exist. Need to correct habit of inventing APIs when he doesn't remember. Better: "don't remember the syntax but the idea would be X".
  - **Didn't know `Equatable` + `.equatable()`** pattern for re-render skip, or that **closures as input break SwiftUI auto-diff**. Asked in semi-senior SwiftUI interviews.
  - Didn't identify stuck `@State` bug with `id: \.self` + indices until I walked code step-by-step. Understood phrase ("`@State` associates to SwiftUI-assigned identity") but *practical consequence* got with guidance, not alone.
  - Didn't know `DateFormatter()` instantiated per render.
- **Patterns observed**:
  - **Asks for code when stuck** — good reflex, realizes he needs concrete scenario. Real interviews he'll have to ask explicitly.
  - When explained mechanism step-by-step with code, internalizes well. Pure verbal explanation doesn't cut it.
  - Still gives short answers. More noticeable this session because topics were new — when he doesn't know, throws ONE idea and waits for feedback instead of reasoning several options.
  - "Everything fixes with async/Task" reflex — classic for people who mastered Concurrency and project it onto non-threading problems.
- **Next session focus**:
  1. **MVVM testing** (next critical unknown, has on CV with TDD and XCTest). Ask how he tests VM with async dependencies, protocol mocking, injection.
  2. **Review `.equatable()`** with different scenario to verify he internalized. Question type: "see in Instruments that `RowView` re-renders 30 times even though `Item` didn't change, what do you do".
  3. **Review view identity** with new case (force stuck `@State` bug in another scenario) to lock in.
  4. **Cut the syntax-invention habit**: when unsure, demand "tell me the idea without syntax, then we confirm the code".
  5. When he answers short, ALWAYS re-ask the "why" — that's the delta missing for senior.
  6. **Architecture / Clean** still pending.
  7. Review **Timer gotcha** (carry-over from prior session).

### 2026-05-12 (third session of the day — MVVM + DIP)
- **Topics covered**: MVVM structure (View / VM / Repository / DependencyContainer, domain entity separation, Repository vs Service), DIP (constructor injection vs environment, why VM must depend on protocol), MVVM testing (mock with `Result`, Arrange/Act/Assert, Swift Testing vs XCTest, `@MainActor` handling in tests).
- **Asked / answered well**: 4 large questions (structure, injection, mock, concrete test). Macro correct on 3, syntax/detail weak on almost all.
- **Weaknesses surfaced**:
  - **Confused L with D in SOLID** — classic error suggesting shallow memorization. Important to re-validate next session.
  - **Mixed domain model**: put `email`, `password`, `attempts`, `token` in single `LoginModel` struct. Doesn't naturally think about separating entities by **lifecycle and reason for being** (`Credentials` ephemeral vs `User` persistent vs `AuthToken`). Missed security implication (password in memory post-login).
  - **Repository vs Service**: had macro idea ("repo does server stuff") but not conceptual separation: repo abstracts source (network/cache/keychain), service does concrete HTTP.
  - **Swift Testing**: knows by name not use. Wrote `test("name")` as function instead of `@Test` attribute. Didn't mark `async` or `await`. Didn't know how to handle `@MainActor` (was explicit in question).
  - **Rigid mock with `Bool`**: first instinct. Showed him idiomatic pattern with `Result<Success, Error>` configurable + `loginCallCount` to verify interactions, not just state.
  - Still asks for code when stuck — good (honest), but also signals he doesn't think through details before starting to write. Real interview they'll say "write it on the whiteboard" and he won't have the model to build it.
- **Patterns observed**:
  - When he says "the idea would be X" instead of inventing syntax, **good signal** — that's what I explicitly asked last session and he's applying it. Internalized habit.
  - Sketches general structure well (always thinks in layers), but detail (exact syntax, SOLID names, fine separation) fails.
  - Asks for mid-validation ("analyze this, then I'll continue") — good, shows thinking in pieces. But real interview won't always give that space.
- **Next session focus**:
  1. **Re-validate SOLID — direct question "tell me the 5 principles with an iOS example for each"**. If confuses L with D again, stop and hammer with mental flashcards (full name + example + 1-line summary).
  2. **Other SOLID principles**: SRP, OCP, LSP, ISP. Especially SRP — Joan already violated it today without realizing (LoginModel with 4 responsibilities).
  3. **MVI or MVP** so he has something to compare MVVM against in interviews. MVI especially useful because growing in Kotlin/Compose (which he also touches) and good test of unidirectional state.
  4. **Concrete Swift Testing practice**: 2-3 different scenarios (success case, delay/timeout case, parametrized with `arguments:`) to internalize syntax.
  5. **Repository vs Service vs UseCase** — scenario-based: "you need to add offline-first, where do you put it". Force layer separation concretely.
  6. **MVVM Navigation**: who navigates (VM with flag, Coordinator, NavigationStack from View). Chose none explicitly this session — direct question next.
  7. Old carry-overs: Timer gotcha, `.equatable()` with new scenario.

### 2026-05-13 (fourth session — Complete SOLID + design patterns + TDD + navigation)
- **Topics covered**: All 5 SOLID with examples (SRP in code review, OCP in PaymentProcessor, LSP — pending he writes, ISP in fat UserService, DIP in VM), TDD red-green-refactor, MVI vs MVVM, MVVM navigation, Repository vs Service (offline-first), cyclomatic complexity, Singleton anti-pattern, Strategy pattern (not recognized).
- **Explicit user preference**: requested shorter questions. Applied from that question onward, answered notably better in short format.
- **Asked / answered well**: 10 short questions. Macro correct on ~8, detail/name/concrete example missing on almost all.
- **Weaknesses surfaced**:
  - **Persistent and critical pattern: NAMING ERRORS**. This session: confused Liskov with Segregation ("Lizkof Segregation"). Prior session: confused D with L. Three SOLID naming errors in two sessions → shallow memorization. Needs re-learn 5 names with iOS example *written by him* next to each.
  - **LSP understood as DIP**: his example (real repo vs cache interchangeable) describes injection, not semantic contract respect. Doesn't have clear difference. Pending: he writes LSP violation in his own repo.
  - **TDD wrong**: omitted refactor (the step that defines TDD) and mixed RED with GREEN. Only thing appearing `weak` after whole session.
  - **Strategy pattern**: applied it (in OCP) without recognizing the name. Knows techniques, not nomenclature. Dangerous in interviews asking "what patterns did you use".
  - **Singleton: missed hidden dependencies** — the bigger problem. Got testability but not implicit coupling or grep / absence in init.
  - **Missing concrete iOS examples** in SRP, OCP, ISP — still giving theory. Asked for examples, came back with definitions.
  - **MVVM Navigation**: rejected VM for wrong reason. Doesn't know idiomatic SwiftUI pattern with `@Published var route: Route?` + `.navigationDestination`.
  - **Didn't know what `grep` is** — minor detail but signals he doesn't use terminal/advanced search much. Probably relies only on Xcode Find in workflow. Good to know.
- **Patterns observed**:
  - **Answers much better in short format.** Long multi-part questions → rambles; 2-3 line questions → surgical. **Keep short format default**, move to code when topic requires grounding.
  - Applied Repository vs Service correction from prior session — good, memory between sessions works in him.
  - When he says "don't know", he's honest, but doesn't TRY reasoning first. Ideally should say "can't get the exact name but the idea is X". Force him to reason before admitting he doesn't know.
  - Still gives ONE idea and waits for feedback instead of reasoning 2-3 options.
- **Next session focus**:
  1. **CRITICAL: re-map SOLID** — direct question "tell me 5 with an iOS example written by you". If confuses names again (likely), stop and hammer with mental flashcards (full name + example + 1-line what it says).
  2. **LSP own code**: pending since this session. Write 2 protocol implementations where one violates LSP.
  3. **TDD red-green-refactor**: re-ask without hints. If omits refactor again, stop and explain why it's the key step.
  4. **Design patterns names + examples**: Strategy, Observer, Factory, Decorator, Adapter, Coordinator. Name + when you used it + 3-line example.
  5. **Singleton hidden dependencies**: re-ask with new scenario to verify he internalized.
  6. **Idiomatic MVVM Navigation SwiftUI**: show pattern with `@Published var route: Route?` + `.navigationDestination(item:)` and compare with Coordinator.
  7. **UseCase / Clean** still pending — didn't mention in offline-first when could have.
  8. **Force iOS examples written by him** — when we ask for example, don't accept "it's like Animal/Dog" or theory. Want code, even pseudo, from his head.
  9. **Concrete Swift Testing practice** still pending.
  10. Old carry-overs: Timer gotcha, `.equatable()` with new scenario.

### 2026-05-13 (fifth session — quick sweep of all pending topics)
- **Topics covered**: SOLID names (re-map), SRP iOS example, TDD re-ask, Strategy, Singleton hidden dependencies, Observer pattern (confused with Observation framework), Idiomatic SwiftUI navigation, UseCase / Clean, Factory, Decorator, `.equatable()` (carry-over), Timer (carry-over), Adapter.
- **Format**: 13 short questions (1-2 lines). Joan explicitly requested short format. **Answered notably better** — more surgical, less rambling, less confusion.
- **Asked / answered well**: 13 questions. Correct on ~9, partial on 4.
- **Weaknesses surfaced**:
  - **Still mixing "what" vs "when"**: when I ask for pattern definition, gives use case. When asking for use case, sometimes gives definition. Useful to practice separating.
  - **Confused Observer with Observation** (iOS 17 framework). Detail but relevant in senior interviews.
  - **`.equatable()`**: mixed what goes in struct (Equatable conformance + `==`) vs call site (modifier). Prior session weak, now ok partial — still not separating the two parts well.
  - **Timer**: got cycle (VM→Timer→closure→self) but missed RunLoop nuance. `weak self` prevents VM leak but Timer still runs zombie until `invalidate()`. Called method "deactive" instead of `invalidate()` — doesn't remember exact names.
  - **Adapter**: definition too generic. No clear difference vs Decorator/Wrapper crystallized.
  - **Idiomatic SwiftUI Navigation**: answered ".navigation in the view" when asked about VM. No fixed pattern of `@Published var route: Route?` + View observation. That's idiomatic SwiftUI 2023+.
- **Patterns observed**:
  - **Corrections between sessions stick well.** TDD refactor: corrected session 4, nailed session 5. Singleton hidden dependencies: corrected session 4, got alone session 5. L vs I confused session 4, not session 5. Memory between sessions works. Very good sign — means the format works.
  - **Short format fits him much better**. Long multi-part questions → rambles. Small surgical questions → on point. **Keep short as default**, move to code when topic needs grounding.
  - When giving definitions, tends to be **too generic** (Adapter: "adapt one type to another"). Tightens when I give counterexample. Force him to say "what distinguishes X from Y is..." when defining patterns.
  - Still little re-ask — answers once and waits for evaluation. Real interviews he could clarify before they ask "anything else?".
- **Next session focus**:
  1. **BACK TO CODE FORMAT** (Joan explicitly asked at session 5 close): 2-3 exercises where he writes Swift from his head. Suggestions:
     - **LSP own code**: write protocol and 2 impls where one violates semantic contract (not just "can't inject"). Pending 2 sessions.
     - **Swift Testing real**: build complete suite with success case, error case, async with delay. Practice syntax he knows by name.
     - **Complete MVVM with idiomatic navigation**: write VM with `@Published var route: Route?` + View with `.navigationDestination(item:)` to lock in pattern.
  2. **Fine differences between patterns**: ask "difference between Adapter, Decorator, and Proxy in 2 lines". Will cost him — good for senior.
  3. **Observer vs Observation framework**: direct question "what's each one and when do you use `@Observable` vs `ObservableObject`". New iOS 17 framework is relevant.
  4. **Cached repository** (real iOS decorator): write `CachedAuthRepository` wrapping another `AuthRepository` and adding cache. Joins Decorator + Repository.
  5. Old pending: Builder, Command, State, Coordinator, Composite — patterns not covered. Probably rarer in iOS interviews but cover anyway.
  6. **Concurrency revisit**: sessions 1-2 covered lots but 2 days ago. Re-ask `async let` and continuations without hints to confirm they stuck.
  7. **Mobile system design**: never touched. Paginated feed, offline-first, sync. What mid-senior gets asked in real interviews. Reserve 1 full session.

### 2026-05-13 (sixth session — REAL CODE format written by Joan)
- **Topics covered**: LSP writing Swift from head (2 attempts), Swift Testing writing real test with mock. Idiomatic SwiftUI navigation was asked but not answered — Joan cut session to prep feedback for a real interview he already had.
- **Format**: explicit request from Joan at session 5 close — back to code. Applied.
- **Asked / answered well**: 2 code exercises. Macro structure correct on both, **many detail bugs** (5+ per exercise).
- **Weaknesses surfaced**:
  - **New and critical pattern: Swift syntax fails when typing from head.** Lowercase types (repeated 4 times), `let x: Tipo()` vs `=`, `throw` without `throws` in signature, `try` in non-throwing function, `let` for props then mutate. First long code exercise and clear the muscle of writing Swift from head is rusty or never worked. **In whiteboard this costs several points** regardless of correct theory.
  - **LSP still not crystallized after 3 sessions**. Has intuition (impl doesn't meet expectation) but can't write concrete semantic contract violation — writes empty impls or always-throw. Missing canonical example: `save` silent that doesn't persist, client thinks saved, `load` fails.
  - **Mock pattern with callCount + Result configurable**: explained session 3, NOT retained session 6. Comes out rigid with `Bool`/`String` without verifying interactions. Key pattern for senior tests.
  - **Doesn't think through VM contract before typing test**: did `try await vm.login(...)` without noticing VM catches error internally (`do/catch` that sets `self.error`). In interview must read signature of what you're testing before writing.
- **Patterns observed**:
  - When writing code from head, pattern "throw ONE version quick and wait for feedback" shows more. Ideal: mentally review protocol signature, verify impl compiles, then throw.
  - Accepted feedback well and improved v2 — but v2 still had 4 different bugs. Needs to iterate more before finishing code.
  - **Fine detail corrections (naming, `throws`/`try`, mutability) don't stick as well** as conceptual corrections (TDD refactor, hidden dependencies). Reason: conceptual ones he "understands"; detail ones need mechanical repetition only gained by typing.
- **Next session focus**:
  1. **LSP own code — THIRD attempt**. Don't accept version until he writes: protocol with clear post-condition, correct impl, impl meeting signature but breaking post-condition. If doesn't work by third try, hammer with canonical `SilentStorage` example until internalized.
  2. **Swift whiteboard syntax drill**: 3-4 small exercises writing types, protocols, structs with throws. Goal: never write `class storageImp1: storage` again.
  3. **Swift Testing — second attempt same test** (can be LoginViewModel) with: configurable mock with `Error?` + `callCount` with `private(set)`, no `try` in non-throwing function. Verify retention this time.
  4. **Idiomatic SwiftUI Navigation with VM** — was asked, not answered. Carry-over next session.
  5. **Before typing code, force reading the signature**: "read aloud what this function throws and returns". Habit that's missing.
  6. When back from real interview flow (STAR), leverage to ask **mobile system design** (never touched, asked at mid-senior).

### 2026-05-15 (seventh session — LSP crystallized + Swift Testing v3)
- **Topics covered**: LSP (third attempt with own code), Swift Testing with configurable mock (`Error?` + `callCount` with `private(set)`).
- **Asked / answered well**: 2 exercises + 2 lock-in questions. LSP finally crystallized; Swift Testing improved but new bugs.
- **Weaknesses surfaced**:
  - **Mock as `struct`**: recurring bug. Joan doesn't internalize value semantics breaks `callCount` verification (test and VM have separate copies). Corrected to `class` post-feedback — but initial reflex still struct. Needs repetition.
  - **`async throws` in test function**: third session writing `try await ...` inside test not marked `async throws`. Mechanical pattern that doesn't stick — pure drill.
  - **Invalid syntax `guard let x != nil`**: mixes optional binding with comparison. Shows he doesn't have canonical patterns (`if let` / `guard let` / `guard ... == nil`) locked in.
  - **PascalCase naming in variables/functions** (`VM`, `LoginViewModelSuccess`): persistent since session 6. Noticed in whiteboard.
- **Patterns observed**:
  - **LSP finally crystallized after 3 sessions**. Key difference was showing canonical `SilentBrokenStorage` example (doesn't throw + load nil) and lock-in question "why does throwing save NOT violate LSP?". Articulated perfect answer. Memory between sessions + concrete example + lock-in = recipe that works.
  - **Conceptual corrections (LSP) stick; mechanical detail corrections (struct vs class for mocks, `async throws` in signatures) need more reps**. Confirmed session 6 pattern.
  - Knows shorthand `if let x { }` from Swift 5.7 — good, not trivial.
  - **Short session by Joan choice** (cut after second exercise).
- **Next session focus**:
  1. **Swift whiteboard syntax drill** — 3-4 small exercises focused on: `async throws` in signatures, `if let` / `guard let`, type casing vs variables. Pure repetition. Until he stops writing `class storage` or `func foo() { try await ... }` without throws.
  2. **LoginViewModel test error case** (carry-over this session, didn't do): use `errorToThrow` already set up. Short, locks in complete configurable mock pattern.
  3. **Mock as `class` — re-ask**: next session, before writing test, ask "will mock be struct or class? Why?". If says class with correct reason (value semantics breaks callCount), it's locked in.
  4. **Idiomatic SwiftUI Navigation with VM** — pending now from session 6-7. Priority.
  5. **Mobile system design** — never touched, pending.
  6. **Concurrency revisit**: `async let` and continuations without hints (4 days untouched).

### 2026-05-17 (eighth session — pure conceptual round, no code)
- **Topics covered**: MVP vs MVVM, UseCase / Clean (revisit), Coordinator + why more common in UIKit, VM-driven navigation (deep explanation on request), Deep linking (explanation on request), TDD what to test and what not, Observer pattern vs Observation iOS 17 framework (revisit session 5), `@Bindable`, `Sendable` (explanation + application exercise).
- **Format**: pure conceptual by Joan request ("evaluate concepts, not practical questions"). 8 questions + 2 explanations on request. Kept short format.
- **NEW important pattern**: Joan requested **use STAR always when applicable**. Saved as feedback memory. Applied STAR well in TDD (S/A/R complete, T implicit) anchored in Planifi-K. Other answers (UseCase, `@Bindable`) anchored in real experience but didn't close with Result.
- **Asked / answered well**: 8 conceptual questions. Macro correct on ~7, senior nuance missing on almost all.
- **Weaknesses surfaced**:
  - **Pattern vs framework confusion persists**: Observer vs Observation (session 5 already), he answered "old framework (Combine+ObservableObject) vs new framework (Observation)" — still doesn't separate **abstract pattern** (GoF concept) from **concrete framework** (iOS implementation). Gave direct answer with analogy "vehicle with wheels vs Toyota Corolla". Re-ask in 2 sessions.
  - **Confused Coordinator with VM-driven**: said "router living in the VM" describing Coordinator. Different patterns — Coordinator lives outside VM. Showed him matrix of 3 patterns (Coordinator / VM-driven / View-driven) and when each.
  - **Sendable**: didn't recall concept. Explained, answered application exercise well (problem structure + 2 correct fixes). Missed: (a) specific conditions for `class + Sendable` (final + let + Sendable properties); (b) `@unchecked Sendable` with lock option; (c) actor option. Gave him complete matrix.
  - **TDD what NOT to test**: answered layer well (no snapshots, test VMs and UseCases) but NOT the senior delta: **test behavior, not implementation details**. Over-testing cost isn't just time, it's **brittle tests that break with any refactor** → team ends up deleting tests or avoiding refactors. Covered this session.
  - **`@Bindable`**: correct idea (bidirectional with `@Observable`) but missed **why it exists**: with `ObservableObject` the property wrapper `@ObservedObject` gave `$` auto; with `@Observable` class is not wrapper → need `@Bindable` to enable `$`. Gave him both cases (received from parent vs `@Bindable var vm = vm` local in body with `@State`).
- **Patterns observed**:
  - **Without code, Joan answers much more fluent**. High count of "missing senior nuances" but macro structure solid on almost all. Real gap: has intuition → lacks precise vocabulary + nuances.
  - **STAR useful**: when anchors in experience (Planifi-K, El Comercio, Comdata), answers sound more senior. Fails closing with Result. Remind at each experience-anchored answer.
  - **Asks for explanations when unclear** ("explain VM-driven", "explain deep linking", "don't recall Sendable") — good, doesn't bullshit. Real interview can do same: "not 100% sure of X, can you explain and we pick it back up?".
  - **Pattern vs framework confusion is now recurrent** (session 5 and 8). Worth specific drill: "tell me 3 GoF patterns and for each a concrete iOS implementation".
- **Next session focus**:
  1. **Pattern vs framework/implementation drill**: 4-5 patterns, ask him concrete iOS implementation. Want him to separate "Observer = idea / Observation = one implementation" automatically.
  2. **Coordinator vs VM-driven re-ask**: new scenario, no hints. If puts "router in VM" as Coordinator again, hammer.
  3. **STAR applied**: force closing with Result when anchoring in experience. Mark each answer missing it.
  4. **Sendable re-ask** in 2-3 sessions — new concept, see if stuck.
  5. **TDD: behavior vs implementation** — scenario-based re-ask type "given this VM and test, what's wrong?". Verify he internalized delta.
  6. **MVI vs Redux/TCA**: new pending. Joan works Kotlin/Compose too, worth anchoring.
  7. **Combine vs async/await**: when each, trade-offs. Pending.
  8. **Persistent carry-overs**: LoginViewModel test error case (Swift Testing), SwiftUI Navigation with real code, mobile system design.

### 2026-05-17 (ninth session — second conceptual round same day)
- **Topics covered**: Pattern vs implementation iOS drill (Observer, Strategy, Factory, Decorator, Singleton), Combine vs async/await + Combine history (2019-2026), MVI vs Redux/TCA (Joan didn't know, explained conceptually), `some` vs `any` (didn't know, explained), 3 ways error handling (throws / Result / Optional), applied with findBook.
- **Format**: pure conceptual. 7 questions + 3 explanations on request. Joan requested to skip 3 topics (AsyncSequence, TCA/Redux applied, some/any applied) — "explain and move on" format works well for new concepts.
- **Asked / answered well**: 7 questions. Macro correct on ~4, needed correction/expansion on ~3.
- **Weaknesses surfaced**:
  - **Singleton confused with EnvironmentObject**: in pattern drill. EnvironmentObject is DI via environment tree, NOT Singleton (multiple instances possible, no `.shared` or private init). Classic iOS Singleton: `URLSession.shared`, `UserDefaults.standard`, `NotificationCenter.default`. Important because session 4 already struggled with Singleton's core problem (hidden dependencies).
  - **Strategy: skipped in drill** — recognizes when shown (session 4 PaymentProcessor) but open iOS example he didn't name. "Strategy" as name not fluent.
  - **Combine vs async/await: weak answer** — anchored in experience (backward compat) but shallow tech content. Confused "callbacks vs closures": old completion handlers are callbacks; Combine NOT callbacks (reactive streams); async/await replaces callbacks. **3 distinct paradigms**, not 2. Gave him complete table: stream-vs-one-shot, declarative-vs-imperative, cancellation, etc.
  - **Didn't know MVI vs Redux/TCA**: reasonable since used MVVM in iOS and MVI in Android (Comdata) but never TCA/Redux. Explained conceptually: Redux (3 principles single source / read-only / pure reducers), TCA (Redux for Swift with Effects). MVI ≈ Redux at screen level; Redux ≈ MVI scaled to app + composition.
  - **Didn't know `some` vs `any`**: Swift 5.7+ (2022). Critical for senior, uses daily in SwiftUI (`some View`) without knowing. Explained opaque type (compile-time, no overhead, one concrete type) vs existential (runtime, boxing, heterogeneous).
  - **Error handling: only knew `throws`**: didn't know `Result<Success, Error>` or Optional is degraded error handling. Gave him decision table with mental rule: throws (N distinct reasons) / Optional (one obvious reason) / Result (error as storable value).
  - **Applied throws to findBook (context import)**: anchored in Planifi-K experience (search history multiple failure reasons, throws OK there) but question was "search book in list by ISBN" — one possible reason → canonical is Optional. **Imported his case answer without checking context fit**. New pattern to watch.
- **Patterns observed**:
  - **Historical gaps in modern fundamentals**: `some/any`, `Result`, `AsyncSequence`, TCA — Joan doesn't know. Probable cause: Planifi-K project legacy or uses traditional fundamentals. Reinforce Swift 5.7+ and modern SwiftUI features next sessions.
  - **Pattern vs implementation: PARTIAL drill application**. Got 3/5 right (Observer, Factory, Decorator). Failed Strategy (skipped) and Singleton (confused with EnvObj). Improvement vs sessions 5 and 8 but incomplete. Re-ask.
  - **Skips when doesn't know (3 times today)**: AsyncSequence, TCA applied, some/any applied. Good he's honest but real interview can't skip. Alternative: reason aloud with what he knows ("didn't use it, but by the name I'd guess..."). Work this reflex.
  - **Imports experience answers without fit-checking**: new pattern. findBook used throws "because Planifi-K did" without noting scenario was different. Real interview gets tested on whether you change mind when counterexample is valid. Flexibility = senior; defensive rigidity = junior.
  - **STAR still closing without Result** on several (Combine migration, findBook). Needs constant reminder.
- **Next session focus**:
  1. **`some` vs `any` application**: exercise choosing one and justifying. Carry-over today.
  2. **Error handling application with 3-4 scenarios**: design function signature given context. Reinforce throws/Optional/Result decision.
  3. **Pattern drill round 2**: re-ask Singleton (what it's NOT) and Strategy (iOS examples). If confuses EnvObj=Singleton again, hammer "private init + .shared + no way to create another".
  4. **AsyncSequence**: explanation + exercise. Modern path and Joan doesn't know.
  5. **Property wrappers under the hood**: how do @State/@Published/@Binding work. Joan uses daily but probably doesn't know they're sugar for struct with `wrappedValue` and `projectedValue`.
  6. **Force reasoning when he doesn't know**: when says "don't know X", re-ask "what does the name tell you? what would you relate it to?" before explaining. Work reflex of reasoning without complete info.
  7. **STAR with Result closed**: mark each answer anchoring in experience but not closing with impact.
  8. **Old carry-overs**: LoginViewModel test error case, SwiftUI Navigation with code, mobile system design.

### 2026-05-18 (tenth session — first realistic simulation, interview mode)
- **Mode**: realistic simulation. No feedback during. Full feedback only at close with Semi-Senior yes/no veredicto.
- **Topics covered**: Real exp/architecture migration (Q1), Observation vs ObservableObject performance (Q2, Q2b), Token storage iOS (Q3), Error handling findBook (Q4), Singleton + EnvironmentObject (Q5), Strategy drill round 2 (Q6, Q6b), Property wrappers under the hood (Q7, Q7b), SwiftUI navigation (Q8), AsyncSequence reasoning (Q9), System design offline-first (Q10).
- **Asked / on-point**: 13 turns (10 main + 3 follow-ups). On Point: 2 (Q4, Q5). Could Be Better: 6. Vague: 4. Don't Know: 1+.
- **Veredicto delivered**: **Does Not Qualify as Semi-Senior (borderline)**. At limit between junior Semi-Senior and consolidated. Solid criterion, lacks fundamental depth.
- **Weaknesses surfaced**:
  - **Property wrappers internals**: can't articulate `wrappedValue`/`projectedValue`/`_var`. Uses daily without underlying mental model. Confirmed "modern fundamentals" gap from session 9.
  - **Strategy as name**: loose definition, repeats only canonical example (PaymentProcessor), doesn't generate own examples. Persistent pattern session 5/9/10.
  - **Observation inside**: answered ergonomics (less verbose) without touching mechanism (property-access tracking vs global `objectWillChange`). "Why/how" remains dominant gap.
  - **Token storage**: hedged "we're analyzing it in Planifi-K" instead of canonical answer. For MFA-bound role, should be fluent. Didn't mention ACL, Secure Enclave, access vs refresh distinction.
  - **System design depth**: macro correct, missed backoff, reachability, BGTaskScheduler, idempotency, ordering. Didn't describe discarded trade-off despite explicit question.
  - **STAR-R weak on Q1**: "solid and scalable application" without metrics. Persistent pattern since session 9.
- **Patterns observed**:
  - **Between-session internalization works**: Singleton vs EnvObj (session 9 → fixed), findBook Optional vs throws (session 9 → fixed), AsyncSequence reasoning by name (session 9 focus → applied). Feedback-close loop is effective.
  - **Within-topic internalization still loose**: Q2 → Q2b improves but only "what", not "why" of mechanism.
  - **Refuge in work context**: when doesn't have tight answer anchors in "we're analyzing at Planifi-K" or "we don't use X in project". Dodges conceptual question. Work this reflex: real interviewer doesn't accept "we don't use that" as dismissal.
  - **Honest when doesn't know (positive)**: doesn't invent APIs (improvement vs session 2 where invented `@StateObject lazy var`).
  - **Solid macro judgment, loose concrete mechanics**: structural pattern now stable. **That's the delta to consolidated Semi-Senior.**
- **Next session focus**:
  1. **Property wrappers under the hood — applied drill**: write own `@Clamped` or `@UserDefault`. Without this doesn't internalize.
  2. **Observation framework deep dive**: what does `@Observable` macro generate? `_$observationRegistrar`, selective tracking. Compare `objectWillChange` global.
  3. **Strategy own examples**: force 3 distinct iOS examples (not payments, not from progress.md). Until come without thinking.
  4. **Security — Keychain canonical**: ACL (`kSecAttrAccessible*`), Secure Enclave, `SecAccessControl`, biometric gating, access vs refresh distinction. Indispensable for MFA role.
  5. **System design mental checklist**: ordering, batching, backoff with jitter, reachability (`NWPathMonitor`), BGTaskScheduler, idempotency keys, ACK protocol, conflict resolution. Apply to another scenario (e.g.: chat offline).
  6. **STAR-R with metrics**: before closing each experience answer, mental pause "what metric/impact do I close with?".
  7. **Cut "we don't use X in work" refuge**: when appears, re-ask conceptually anyway.
  8. **Old carry-overs**: `some`/`any` applied, LoginViewModel test syntax (Swift Testing), MVP vs MVVM trade-offs.

### 2026-05-18 (session 11 — second simulation same day, mode "fresh start, skip marked topics")
- **Mode**: realistic simulation. Topics already validated (from Topic Mastery table) marked 🟢 skipped. Focus on gaps.
- **Topics covered**: MVP vs MVVM (Q1), Strategy own examples (Q3/Q3b), Keychain access vs refresh (Q4), some/any applied (Q5), SwiftUI List performance (Q6), TDD what not to test (Q7), System design push (Q8 skip), Observer (Q9), Autonomy what-if Friday 5pm (Q10).
- **Asked / on-point**: 10 questions + 1 follow-up. On Point: 1 (Q5). Could Be Better: 7. Don't Know: 1 (Q3b). Skip: 1 (Q8).
- **Veredicto delivered**: **Qualifies as Semi-Senior (borderline, lower-end)** — change vs session 10. Between-session internalization worked.
- **Weaknesses surfaced**:
  - **Strategy still weak**: second consecutive failure (session 10 + 11) on 2 distinct examples. Only data-source or payments.
  - **Keychain canonical not fluent**: didn't name any `kSecAttrAccessible*` value. Confused OAuth2 with MFA flow. Critical for MFA role.
  - **TDD what not to test**: answered project-decision instead of canonical criterion (DTOs, framework code, generated, view).
  - **Narrative inconsistency with joan_stories.md**: Q7 mixed Comdata metrics (60% / 10 months) with Planifi-K. Re-read stories before next practice.
  - **System design**: requested skip again (like session 9). Pending topic.
  - **What-if stepwise**: tends to answer principles, not actionable numbered sequence.
- **Patterns observed** (positive):
  - **Between-session internalization worked clearly this time**: some/any applied, Observer correctly named, List performance with stable ID, VStack-ForEach anti-pattern detected. Feedback-close loop is effective.
  - **Solid autonomy in real scenarios** (Q10): decides, proposes mitigation, doesn't hide behind lead.
  - **Detects production anti-patterns** (VStack-ForEach): shows genuine experience.
- **Patterns observed** (negative):
  - **Still importing work context instead of canonical reasoning** (Q4 Keychain, Q7 TDD). Persistent since session 9.
  - **Skips when doesn't want to tackle** — Q8 today, like session 9. Work reflex of reasoning with what he knows.
- **Next session focus**:
  1. **Re-read `joan_stories.md`** to lock metrics by company before any experience question.
  2. **Strategy playbook iOS**: 3 non-data-source examples memorized (sort, retry policies, formatters).
  3. **Keychain cheat sheet**: `kSecAttrAccessible*` values + `SecAccessControl` with biometrics. Indispensable for MFA role.
  4. **TDD canonical criterion** (not project-decision).
  5. **System design**: force answer, no skip. Minimal components as safety net.
  6. **What-if stepwise**: practice numbered 1/2/3 sequence instead of principles.
  7. **Carry-over**: LoginViewModel test syntax (Swift Testing) — pending since session 7.

### 2026-05-19 (session 12 — refresh old + gaps from 11)
- **Mode**: realistic simulation. Deliberate mix of refresh on topics "ok" 3-7 sessions ago + carry-overs from session 11.
- **Topics covered**: Timer retain cycle (Q1), cooperative cancellation (Q2), Keychain access vs refresh (Q3), LSP (Q4), UseCase/Repo/Service (Q5), Strategy own examples round 3 (Q6), TDD canonical (Q7), what-if stepwise crash iOS 17.0 (Q8), system design inbox (Q9), continuations (Q10).
- **Asked / on-point**: 10 questions. **On Point: 4** (Q1 Timer, Q2 cancellation, Q4 LSP, Q10 continuations — all old refreshes). Could Be Better: 6. No Don't Know, no Skip.
- **Veredicto delivered**: **Qualifies as Semi-Senior (mid-range)**. Up vs session 11.
- **Patterns observed** (positive):
  - **Long retention validated**: 4 topics marked "ok" 5-7 days ago still On Point. Session-feedback-retention loop works empirically.
  - **Broke skip reflex** on system design (Q9, first time in 3 sessions).
  - **Internalized MFA flow between sessions** (Q5): applied mfa_token / access_token correctly unprompted.
  - **TDD mental shift** (Q7): moved from "project-decision" to "canonical categories". Partial list but switch happened.
  - **Numbered stepwise** (Q8): followed format asked session 11.
- **Patterns observed** (negative):
  - **Erosion in Repo vs Service** (Q5): separation crystallized session 3 blurred. Service not mentioned as layer.
  - **Strategy — 3rd failure in 2 examples** (Q6), though first was original (map/filter).
  - **Partial Keychain recall post-class** (Q3): named 2 of 4 values without access/refresh mapping, no biometrics.
  - **What-if shallow on content** (Q8): form OK, steps generic.
  - **Invented El Comercio story Q10**: continuations real but story not canonical (not in `joan_stories.md`). Risk of narrative inconsistency.
  - **Android "Room service" slip** (Q9): watch cross-platform terminology.
- **Next session focus**:
  1. **Re-hammer Keychain mapping** in 2-3 sessions (delayed lock-in): `access → AfterFirstUnlockThisDeviceOnly`, `refresh → WhenUnlockedThisDeviceOnly + SecAccessControl.userPresence`.
  2. **Refresh Repo vs Service**: "Repo abstracts where, Service does HTTP".
  3. **Strategy closed triad**: map/filter + retry policy + sort comparator. Memorize.
  4. **What-if specific content**: each step = ONE action + ONE artifact (stack trace, blast radius in numbers, FF off, stakeholder communication).
  5. **System design checklist** 5-6 elements: components, global vs local state, sync, pagination, edge cases, persistence.
  6. **Re-read `joan_stories.md`** before each practice to not invent.
  7. **Carry-over old**: LoginViewModel test syntax (Swift Testing, pending since session 7).

### 2026-06-03 (session 13 — gaps from session 12 + retention refresh)
- **Topics covered**: Repo vs Service (Q1, Q8), Strategy own examples (Q2), Property wrappers mechanism (Q3, Q9), Keychain accessibility (Q4), Task cancellation refresh (Q5), LSP refresh (Q6), Swift Testing syntax (Q7), Real Experience Planifi-K (Q10).
- **Asked / on-point**: 10 questions. **On Point: 1** (Q5 cancellation). Could Be Better: 6. Don't Know: 3.
- **Veredicto delivered**: **Does Not Qualify as Semi-Senior (borderline, lower-end)**. Down vs session 12. Depth and execution gap.
- **Weaknesses surfaced**:
  - **Repo vs Service persistent confusion**: "repos give DTOs, service gives domain objects" (inverted). Doesn't articulate abstraction vs implementation separation. Retry logic: answered Service (partial, missed business-level retry in Repo).
  - **Strategy generation own**: 4th attempt, still no independent examples. Hypothetical AspectFit/AspectFill → got it. Real project → "no".
  - **Property wrappers underlying model**: Knows `$x` / `_x` symbols, not `wrappedValue`/`projectedValue` struct. Answered "pointer" (Improvised). Can't write custom wrapper.
  - **Keychain recall**: 15 days post-learning, doesn't remember `kSecAttrAccessible*` values. "I don't remember" admitted.
  - **Swift Testing syntax**: Defaulted to pseudo-code ("I can't write it right now, here are the steps"). Syntax wrong: `expected()` vs `#expect()`, no `@Test` attribute. Mock as struct.
  - **STAR-R weak**: "module is consumed by our app" — activity, not result. No metrics, no outcome.
  - **LSP reasoning**: Got right answer, reasoning soft ("we discover in tests" vs post-condition violation).
- **Patterns observed**:
  - **Honest when doesn't know** — doesn't invent, admits gaps. Positive for real interviews.
  - **Solid macro structure, loose execution** — confirmed structural pattern (session 6+).
  - **Keychain erosion**: 15 days without reinforcement, recall lost. Needs daily drill.
  - **Property wrappers critical**: uses daily, doesn't understand mechanism. Blocks custom wrappers or debugging.
- **Next session focus**:
  1. **Property wrappers under the hood DRILL** (1 hour): write `@Clamped`, `@UserDefault`, or `@Validated` custom. Understand `wrappedValue`/`projectedValue` struct model, not pseudo-code.
  2. **Offline-first architecture real scenario** (1.5 hours): VM → Repo → (Service + Cache). Diagram roles. Test: network fails → Repo retry → fallback cache.
  3. **Strategy closed triad memorized**: (a) map resize (AspectFit/AspectFill), (b) sort comparator, (c) retry policy. No PaymentProcessor, no data sources.
  4. **Keychain cheat sheet daily drill** (30 min + 2 weeks): `access → AfterFirstUnlockThisDeviceOnly`, `refresh → WhenUnlockedThisDeviceOnly + SecAccessControl.userPresence`. Why: refresh higher-value, biometrics. Access short-lived, unlock enough.
  5. **Swift Testing full suite** (1 hour): LoginViewModel test success + error cases. Syntax: `@Test func myTest() async throws { #expect(...) }`. Mock as class, `errorToThrow` configurable.
  6. **STAR-R metric** (ongoing): Ask "what metric?" before answering experience.
  7. **Carry-overs**: Property wrappers code (priority), Repo vs Service clarity (architecture), Strategy examples (pattern mastery).

### 2026-06-03 (session 14 — comprehensive all-topics review)
- **Mode**: realistic simulation, comprehensive all-topics review (user requested)
- **Topics covered**: Repo vs Service vs UseCase, Strategy, some vs any, Timer retain cycle, async let vs TaskGroup, Keychain tokens, Swift Testing mock, SwiftUI Navigation, Singleton, Property wrappers, Offline-first sync.
- **Asked / on-point**: 11 questions (10 main + 1 follow-up). On Point: 1 (Q2 Strategy). Could Be Better: 7. Improvised: 2. Don't Know→Reasoning: 1.
- **Veredicto delivered**: **Does Not Qualify as Semi-Senior (borderline, lower-end)** — same as session 13. Macro judgment solid, execution depth loose.
- **Strengths**:
  - **Strategy pattern finally locked in** (Q2): first time generated own example independently in 4 sessions. Named, explained, anchored in real experience. On Point.
  - **Timer cycle intuition solid** (Q4): correctly identified VM→Timer→closure→VM chain. Foundation strong, nuance (invalidate call) missing.
  - **Architecture thinking structured**: layers (VM/Repo/Service/UseCase) natural. Concept there; boundaries fuzzy.
- **Weaknesses surfaced**:
  - **Repo vs Service inverted** (Q1): "repos give DTOs, service gives domain" — backwards. Repository should abstract WHERE data comes from, Service is concrete HTTP. Fundamental gap for any role.
  - **Property wrappers mechanism missing** (Q10): "getter/setter + lifecycle" is effect, not mechanism. Doesn't know `wrappedValue`/`projectedValue` struct model. Uses daily, doesn't understand. Blocks custom wrappers.
  - **some vs any**: reasoning started (specific vs general intuition) but lacks mechanism (opaque vs existential, compile-time vs runtime).
  - **Swift Testing syntax errors** (Q7): `@test` vs `@Test`, `#expected()` vs `#expect()`, missing `async throws`. Avoids code writing under pressure.
  - **Keychain details** (Q6): chose right tool but missing access/refresh distinction and `kSecAttrAccessible*` values. 15-day erosion confirmed.
  - **System design macro only** (Q11/11b): offline-first batching right idea, missing ordering/idempotency/reachability/BGTaskScheduler/conflict-resolution.
- **Patterns observed**:
  - **Solid macro judgment, loose concrete mechanics** — persistent structural pattern. That's the delta between borderline and confident Semi-Senior.
  - **Code avoidance under pressure**: Q7 defaulted to pseudo-code. In whiteboard this costs points. Muscle of typing from memory weak.
  - **Honest when doesn't know**: doesn't invent, admits gaps. Positive for interviews.
  - **Missing "why" on mechanisms**: know effect, not mechanism (property wrappers, cancellation, navigation). Real interviews push harder here.
- **Next session focus** (priority order):
  1. **Property wrappers code drill** (1h): write custom `@Clamped` or `@UserDefault`. Force `wrappedValue`/`projectedValue` struct model understanding.
  2. **Repo vs Service clarity** (30m): hammer "Repository = abstraction of WHERE, returns domain entities. Service = concrete HTTP, returns raw responses." Code example.
  3. **Keychain daily drill** (2 weeks): memorize `access → AfterFirstUnlockThisDeviceOnly`, `refresh → WhenUnlockedThisDeviceOnly + SecAccessControl.userPresence + Secure Enclave`. Why each.
  4. **Swift Testing full suite** (1h): LoginViewModel success + error cases. Syntax: `@Test func myTest() async throws { #expect(...) }`. Mock as class, configurable `errorToThrow`.
  5. **some vs any applied**: scenario-based ("function returns one concrete View for condition, use some or any? Why?") until automatic.
  6. **System design checklist**: ordering, batching, backoff+jitter, reachability (NWPathMonitor), BGTaskScheduler, idempotency, ACK, conflict resolution.
  7. **SOLID 5 names**: flashcards with one iOS example each. SRP, OCP, LSP, ISP, DIP.
- **Mode**: realistic simulation. Focus on detected erosion (Repo/Service) + weak topics (Keychain, property wrappers, Strategy).
- **Topics covered**: Repo vs Service (Q1, Q8), Strategy own examples (Q2), Property wrappers mechanism (Q3, Q9), Keychain accessibility (Q4), Task cancellation refresh (Q5), LSP refresh (Q6), Swift Testing syntax (Q7), Real Experience Planifi-K (Q10).
- **Asked / on-point**: 10 questions. **On Point: 1** (Q5 cancellation). Could Be Better: 6. Don't Know: 3.
- **Veredicto delivered**: **Does Not Qualify as Semi-Senior (borderline, lower-end)**. Down vs session 12. Depth and execution gap.
- **Weaknesses surfaced**:
  - **Repo vs Service persistent confusion**: "repos give DTOs, service gives domain objects" (inverted). Doesn't articulate abstraction vs implementation separation. Retry logic: answered Service (partial, missed business-level retry in Repo).
  - **Strategy generation own**: 4th attempt, still no independent examples. Hypothetical AspectFit/AspectFill → got it. Real project → "no".
  - **Property wrappers underlying model**: Knows `$x` / `_x` symbols, not `wrappedValue`/`projectedValue` struct. Answered "pointer" (Improvised). Can't write custom wrapper.
  - **Keychain recall**: 15 days post-learning, doesn't remember `kSecAttrAccessible*` values. "I don't remember" admitted.
  - **Swift Testing syntax**: Defaulted to pseudo-code ("I can't write it right now, here are the steps"). Syntax wrong: `expected()` vs `#expect()`, no `@Test` attribute. Mock as struct.
  - **STAR-R weak**: "module is consumed by our app" — activity, not result. No metrics, no outcome.
  - **LSP reasoning**: Got right answer, reasoning soft ("we discover in tests" vs post-condition violation).
- **Patterns observed**:
  - **Honest when doesn't know** — doesn't invent, admits gaps. Positive for real interviews.
  - **Solid macro structure, loose execution** — confirmed structural pattern (session 6+).
  - **Keychain erosion**: 15 days without reinforcement, recall lost. Needs daily drill.
  - **Property wrappers critical**: uses daily, doesn't understand mechanism. Blocks custom wrappers or debugging.
- **Next session focus**:
  1. **Property wrappers under the hood DRILL** (1 hour): write `@Clamped`, `@UserDefault`, or `@Validated` custom. Understand `wrappedValue`/`projectedValue` struct model, not pseudo-code.
  2. **Offline-first architecture real scenario** (1.5 hours): VM → Repo → (Service + Cache). Diagram roles. Test: network fails → Repo retry → fallback cache.
  3. **Strategy closed triad memorized**: (a) map resize (AspectFit/AspectFill), (b) sort comparator, (c) retry policy. No PaymentProcessor, no data sources.
  4. **Keychain cheat sheet daily drill** (30 min + 2 weeks): `access → AfterFirstUnlockThisDeviceOnly`, `refresh → WhenUnlockedThisDeviceOnly + SecAccessControl.userPresence`. Why: refresh higher-value, biometrics. Access short-lived, unlock enough.
  5. **Swift Testing full suite** (1 hour): LoginViewModel test success + error cases. Syntax: `@Test func myTest() async throws { #expect(...) }`. Mock as class, `errorToThrow` configurable.
  6. **STAR-R metric** (ongoing): Ask "what metric?" before answering experience.
  7. **Carry-overs**: Property wrappers code (priority), Repo vs Service clarity (architecture), Strategy examples (pattern mastery).
