# 🎬 Saransh's Movie Recommendation Platform

> **College Project Submission**  
> A 100% offline, client-side movie recommendation system utilizing multi-factor dynamic weighting, content similarity, and seed-movie matching across 4,740+ curated films.

---

## 🌟 Key Features

### Baseline Core Engines
1. **Multi-Factor Explorer**:
   - Filter and rank movies across **7 custom factors**:
     - 🔮 **Mood / Vibe**: 6 curated emotional categories (*Mind-Bending*, *High Adrenaline*, *Feel-Good*, *Dark & Gritty*, *Deep & Emotional*, *Epic & Imaginative*).
     - 🎭 **Genres**: Multi-select across 20 distinct film genres.
     - ⏳ **Decade / Era**: Classics (<1970) through 2020s.
     - ⏱️ **Runtime Profile**: Quick (<90m), Standard (90–120m), Epic (>120m).
     - ⭐ **Rating Quality**: Real-time slider threshold with TMDB/IMDb vote scoring.
     - 🎬 **Director & Star Cast**: Filter by renowned filmmakers and lead actors.
2. **Dynamic Weight Normalization**:
   - The user can pick **any 1, 2, or more factors**.
   - The algorithm automatically normalizes active factor weights to **100%**, generating accurate match percentage badges.
3. **"More Like This" Seed Recommender**:
   - Search any reference film (e.g., *Inception*, *Interstellar*, *Pulp Fiction*).
   - Toggle individual factors on/off (`[✓] Same Mood`, `[✓] Same Director`, `[✓] Shared Genres`, `[✓] Plot Themes`) to customize what makes another movie "similar".
4. **Local Watchlist & Instant Offline Search**:
   - Zero external API dependencies; 100% offline dataset loaded in client memory.

---

### 🚀 The 4 Distinctive Advanced Features

#### 🧬 Feature 1: Story DNA Finder (Narrative Architecture Engine)
* **Concept**: Recommends movies based on narrative structure, chronological flow, and storytelling characteristics rather than metadata alone.
* **10 Curated Narrative Traits**:
  1. *Plot Twists & Revelations* (🌀)
  2. *Slow-Burn Storytelling* (🕯️)
  3. *Nonlinear Timelines* (⏳)
  4. *Unreliable Narrators* (🎭)
  5. *Character Transformation* (🦋)
  6. *Psychological Depth* (🧠)
  7. *Mystery & Hidden Clues* (🔎)
  8. *Parallel Storylines* (🔀)
  9. *Emotion-Driven Storytelling* (💧)
  10. *Open-Ended Conclusions* (❓)
* **Custom Importance Weighting**: Assign 1x (Low), 2x (Medium), or 3x (High) weight to any trait, or toggle presets.
* **Transparent Explanations**: Every recommendation provides a tailored reason (e.g., *"Recommended because you prioritized Nonlinear Timelines and Plot Twists (Verified cinematic benchmark)"*).
* **DSA Implementation**:
  - **Inverted Index Hash Map** (`traitToMoviesMap`): $O(1)$ candidate retrieval.
  - **Set Intersection**: $O(|T|)$ narrative trait overlap calculation.
  - **Bounded Min-Heap** (`MinHeap`): $O(N \log K)$ Top-K selection where $K=24$, bypassing expensive $O(N \log N)$ sorting.

#### ⚡ Feature 2: What-If Recommendation Simulator
* **Concept**: Interactive sandbox allowing cinephiles to adjust hypothetical tastes and observe real-time recommendation shifts.
* **Preset Scenarios**:
  - *"What if I want more suspense?"*
  - *"What if I prefer shorter movies?"*
  - *"What if I want highly rated hidden gems?"*
  - *"What if I want something completely different from my usual choices?"*
* **Side-by-Side Live Comparison**:
  - **Left**: Original Top 10 (Current preferences)
  - **Right**: What-If Top 10 (Simulated projection)
* **Rank Differential Engine**:
  - Highlights newly entered titles (`🆕 Entered Top 10`), climbed titles (`▲ Rose N Spots`), dropped titles (`▼ Dropped N Spots`), and held rank (`= Held Rank`).
  - Dedicated drawer displaying displaced titles that exited the Top 10 along with specific exit reasons.
* **State Isolation**: Zero mutations to saved user preferences until explicitly clicking *"Apply to Explorer"*.

#### ⏳ Feature 3: Recommendation Time Machine
* **Concept**: Tracks the chronological evolution of a user's movie taste and leverages dated interaction history to power personalized hybrid recommendations.
* **Interaction Capture**: Record 👍 *Liked*, 👁️ *Watched*, 👎 *Disliked*, and 🔖 *Saved* films directly from cards and detail modals.
* **Honest Temporal Trend Analysis**:
  - Compares earlier window activity vs recent window activity.
  - Generates verified statements: e.g., *"You have recently shown more interest in Mystery (+40%) than in Comedy (-40%)."* (Only displayed when statistically supported by real stored data).
* **Taste Radar & Affinity Progress Bars**: Visualizes genre affinities and positive vs negative interaction distributions.
* **Personalized Hybrid Recommendations**: Blends current filter goals with historical genre affinity weights while strictly excluding disliked and watched titles.
* **Privacy & Architecture**: Versioned `localStorage` (`v1`) with corrupt storage fallback. 100% private in browser with "Clear Stored History" control.

#### 🏆 Feature 4: Movie Discovery Challenge
* **Concept**: Gamified cinephile exploration dashboard turning film discovery into an engaging personal adventure.
* **6 Curated Challenges**:
  1. *The Hidden Masterpiece* (Rating $\ge 8.0$, Votes $\ge 800$, +100 XP)
  2. *Genre Frontier Pioneer* (Explore outside top 3 most-interacted genres, +150 XP)
  3. *Time Traveler Classic* (Pre-1980 classic film, +50 XP)
  4. *Underrated Indie Treasure* (Rating $\ge 7.3$, votes between 50 and 2,000, +150 XP)
  5. *Uncharted Territory* (Foreign, Documentary, Western, or Animation, +100 XP)
  6. *Narrative Chameleon* (3 distinct storytelling characteristics, +200 XP)
* **Gamification & Level Progression**:
  - Level 1: *Cinema Novice* (0-99 XP)
  - Level 2: *Film Explorer* (100-249 XP)
  - Level 3: *Genre Pioneer* (250-449 XP)
  - Level 4: *Cinephile Connoisseur* (450-699 XP)
  - Level 5: *Grand Film Auteur* (700+ XP)
* **Balanced Discovery Algorithm**:
  - Score $= 0.6 \times \text{Quality} + 0.4 \times \text{Novelty}$.
  - Uses session Sets to strictly prevent repetitive recommendations.
  - Points awarded only for explicit exploration/marking watched.

#### 👥 Feature 5: Multi-Persona Watch Party (Group Consensus Engine)
* **Concept**: Solves the classic "what should we watch together?" movie night argument when multiple people with diverse tastes gather in the room.
* **Persona Selection & Creation**:
  - Pre-configured personas: 🍿 Alex (*Action/Sci-Fi*), 🎭 Sam (*Drama/Romance*), 🧠 Jordan (*Mystery/Thriller*), 🧸 Taylor (*Comedy/Family*), 😱 Morgan (*Horror/Gritty*), 🚀 Riley (*Sci-Fi/Fantasy*).
  - Ability to add **Custom Friends** with personalized names, emoji avatars, favorite genres, and **dealbreaker vetoes** (e.g. *"Never show Horror"*).
  - Pre-set combos: *Date Night*, *Roommates*, *Family Movie Night*, and *Whole Squad*.
* **Compromise Presentation**:
  - 🏆 **#1 Common Compromise Movie Spotlight**: Top movie with poster, synopsis, group harmony rating, and individual happiness progress bars.
  - 🛡️ **Fairness Guarantee Banner**: Explains why the movie works for everyone and proves zero vetoes were triggered.
  - 🥈 **Top 4 Alternative Compromises**: Pareto-optimal runners-up with mini per-person satisfaction tags.
* **DSA Implementation**:
  - **Max-Min Fairness Algorithm**: $\max_{m} \left( \min_{p \in \text{People}} \text{Score}(p, m) \right)$ — maximizes the happiness of the least satisfied person so nobody feels left out.
  - **Bounded Min-Heap ($K=5$)**: Efficiently maintains the Top 5 compromise candidates in $O(N \cdot F + N \log K)$ time.
  - **Strict Veto Filtering**: Sets identify dealbreaker genres in $O(1)$ time and apply severe penalty weights.

---

## 📐 Mathematical Formulation (For Project Viva / Presentation)

### 1. Factor Explorer Scoring with Dynamic Normalization
When a user selects a subset of factors $F_{\text{active}} \subseteq \{ \text{mood}, \text{genre}, \text{era}, \text{runtime}, \text{rating}, \text{director}, \text{actor} \}$:

$$\text{Final Score}(M) = \frac{\sum_{f \in F_{\text{active}}} S_f(M) \cdot W_f}{\sum_{f \in F_{\text{active}}} W_f} \times 100\%$$

Where:
* $S_{\text{mood}}(M) = \frac{|\text{Moods}(M) \cap \text{Moods}_{\text{user}}|}{|\text{Moods}_{\text{user}}|}$
* $S_{\text{genre}}(M) = \frac{|\text{Genres}(M) \cap \text{Genres}_{\text{user}}|}{|\text{Genres}_{\text{user}}|}$ (Jaccard Overlap)
* $S_{\text{era}}(M) = \mathbb{I}(\text{Decade}(M) == \text{Decade}_{\text{user}})$
* $S_{\text{runtime}}(M) = \mathbb{I}(\text{RuntimeBucket}(M) == \text{RuntimeBucket}_{\text{user}})$
* $S_{\text{rating}}(M) = \min\left(1.0, \frac{\text{Rating}(M)}{8.5}\right)$
* $S_{\text{director}}(M) = \mathbb{I}(\text{Director}(M) == \text{Director}_{\text{user}})$
* $S_{\text{actor}}(M) = \mathbb{I}(\text{Actor}_{\text{user}} \in \text{Cast}(M))$

---

### 2. Seed Movie Similarity
Given a seed movie $S$ and candidate movie $M$:

$$\text{Similarity}(S, M) = \sum_{k \in \text{Toggled}} W_k \cdot \text{Overlap}_k(S, M)$$

Matches are ranked by descending similarity percentage, excluding the seed movie itself ($M \ne S$).

---

## 🗂️ Project Structure

```
├── .github/
│   └── workflows/
│       └── deploy.yml          # Automated GitHub Pages CI/CD workflow
├── data/
│   ├── movies.json             # 4,740 preprocessed movies (3.0 MB)
│   ├── metadata_summary.json   # Aggregated genres, moods, top directors/actors
│   └── story_dna_traits.json   # 10 narrative traits mapped across 834 films (170 KB)
├── movieDataset/
│   ├── tmdb_5000_movies.csv    # Raw dataset (5.7 MB)
│   └── tmdb_5000_credits.csv   # Raw credits & cast dataset (40 MB)
├── tests/
│   ├── test_features.py        # Automated test suite (18 unit tests, 100% passing)
│   └── final_audit.py          # Static syntax, integrity & consistency audit (8/8 passing)
├── index.html                  # Semantic responsive UI layout with 4 feature tabs
├── styles.css                  # Modern cinematic dark mode design system
├── dsa.js                      # Core DSA Engines: MinHeap, StoryDNA, WhatIf, TimeMachine, Challenge
├── app.js                      # Client-side recommendation engine, UI controllers & state manager
├── preprocess.py               # One-time data cleaning & feature extraction script
└── README.md                   # Project documentation & viva guide
```

---

## 🚀 How to Run Locally

1. Open a terminal in the project folder:
   ```bash
   cd "movie recommender system dsa project/movieRecommendationPlatform-main"
   ```
2. Start Python's built-in local web server:
   ```bash
   python -m http.server 8000 --bind 127.0.0.1
   ```
3. Open your browser and navigate to:
   ```
   http://localhost:8000
   ```

---

## 🧪 Testing and Verification Suite

Run the automated test suites from the project root:

```bash
# 1. Run the comprehensive unit test suite (Min-Heap, Hash Maps, Sets, Trends, Gamification)
python tests/test_features.py

# 2. Run the project integrity and syntax audit
python tests/final_audit.py
```

Both test suites execute offline and verify algorithmic correctness, data integrity, and error boundaries.

---

## 🌐 Deploy to GitHub Pages (Automated via GitHub Actions)

1. Create a new repository on your GitHub account (e.g. `cinematch-recommender`).
2. Push this folder to your repository:
   ```bash
   git init
   git add .
   git commit -m "feat: upgrade CineMatch with 4 distinctive DSA features"
   git branch -M main
   git remote add origin https://github.com/saranshsawal/movieRecommendationPlatform.git
   git push -u origin main
   ```
3. In your GitHub repository:
   * Go to **Settings** $\rightarrow$ **Pages**.
   * Under **Build and deployment** $\rightarrow$ **Source**, choose **GitHub Actions**.
4. The workflow in `.github/workflows/deploy.yml` will automatically build and publish your website live to:
   ```
   https://saranshsawal.github.io/movieRecommendationPlatform/
   ```

---

## 🎓 Viva & Presentation Q&A Preparation

| Question | Recommended Answer |
| :--- | :--- |
| **Why use a client-side architecture instead of a backend server?** | For a curated catalog of ~5,000 movies, loading a preprocessed 3.0 MB JSON file delivers **instant sub-millisecond filtering and recommendation** with **zero server costs**, **zero latency**, and **100% offline availability** on GitHub Pages. |
| **How does Story DNA Finder achieve $O(N \log K)$ retrieval?** | Rather than sorting all $N$ scored candidates in $O(N \log N)$, it uses a **bounded Min-Heap of size $K$** ($K=24$). The root stores the minimum score in the current Top-$K$. When a candidate exceeds the root, the root is popped and replaced in $O(\log K)$ time. It also uses an **Inverted Index Hash Map** to prune non-matching films in $O(1)$ time. |
| **How does the What-If Simulator isolate user state?** | The simulator clones the active preference state into an ephemeral sandbox object. Sliders and toggles mutate only the sandbox model. Differential metrics (`entered`, `exited`, `rose`, `dropped`, `held`) are calculated by joining the original and simulated arrays via a film ID Hash Map. Saved preferences are only modified if the user explicitly clicks *"Apply to Explorer"*. |
| **How does the Time Machine calculate temporal preference shifts honestly?** | Interaction events (`liked`, `disliked`, `watched`, `saved`) are stored in an array of timestamped objects in `localStorage`. The engine splits events into two temporal halves (earlier vs recent) using a median timestamp or event count window. Normalized genre affinity vectors are computed for both windows. Comparative claims (e.g., *"more interested in Mystery than Comedy"*) are **only rendered when the percentage delta $\Delta \ge 10\%$ is statistically backed by stored data**. |
| **How does the Movie Discovery Challenge prevent duplicate recommendations?** | A JavaScript `Set` of movie IDs (`sessionExploredIds`) persists throughout the active session. When a user requests hints or discoveries for a challenge, candidate films are filtered against this `Set` in $O(1)$ time, guaranteeing that films are not repeatedly presented during exploration. |
| **What happens if a user selects only 1 or 2 factors in the Explorer?** | The engine uses **Dynamic Weight Normalization**. It computes the sum of only the selected factor weights and normalizes the final score to 100%, preventing skewed or suppressed percentages. |
| **What dataset was used?** | The **TMDB 5,000 Movie Dataset**, joined with cast and crew credits to extract genres, director, lead actors, plot overviews, release dates, and story keywords. Story DNA traits are verified against explicit keyword/overview signal traces in `data/story_dna_traits.json`. |
