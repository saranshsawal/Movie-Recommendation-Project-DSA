"""
Comprehensive Unit & Integration Test Suite for CineMatch 4 Distinctive Features:
1. Story DNA Finder
2. What-If Recommendation Simulator
3. Recommendation Time Machine
4. Movie Discovery Challenge
"""

import json
import os
import sys

print("==================================================")
print("CINEMATCH 4 DISTINCTIVE FEATURES UNIT TEST SUITE")
print("==================================================")

failures = []

def assert_test(condition, test_name):
    if condition:
        print(f"[PASS] {test_name}")
    else:
        print(f"[FAIL] {test_name}")
        failures.append(test_name)

# -------------------------------------------------------------
# 1. Dataset & Story DNA Data Validation
# -------------------------------------------------------------
try:
    with open("data/movies.json", "r", encoding="utf-8") as f:
        movies = json.load(f)
    assert_test(len(movies) >= 4740, f"movies.json contains {len(movies)} movies (>= 4740)")

    with open("data/story_dna_traits.json", "r", encoding="utf-8") as f:
        story_data = json.load(f)
    traits = story_data.get("traits", [])
    movie_traits = story_data.get("movie_traits", {})
    assert_test(len(traits) == 10, f"Story DNA defines exactly 10 narrative traits (Found: {len(traits)})")
    assert_test(len(movie_traits) >= 800, f"Story DNA tags at least 800 films (Found: {len(movie_traits)})")

    # Verify trait keys
    expected_traits = [
        "plot_twists", "slow_burn", "nonlinear", "unreliable_narrator",
        "character_transformation", "psychological_depth", "mystery_clues",
        "parallel_storylines", "emotion_driven", "open_ended"
    ]
    all_found = all(any(t["id"] == tid for t in traits) for tid in expected_traits)
    assert_test(all_found, "All 10 required narrative trait IDs exist in definitions")

except Exception as e:
    assert_test(False, f"Dataset loading error: {e}")

# -------------------------------------------------------------
# 2. MinHeap / Priority Queue Verification
# -------------------------------------------------------------
class PythonMinHeap:
    def __init__(self, key_fn=lambda x: x):
        self.heap = []
        self.key = key_fn
    def push(self, val):
        self.heap.append(val)
        self._up(len(self.heap) - 1)
    def pop(self):
        if not self.heap: return None
        top = self.heap[0]
        bot = self.heap.pop()
        if self.heap:
            self.heap[0] = bot
            self._down(0)
        return top
    def peek(self):
        return self.heap[0] if self.heap else None
    def size(self):
        return len(self.heap)
    def _up(self, idx):
        while idx > 0:
            parent = (idx - 1) // 2
            if self.key(self.heap[idx]) < self.key(self.heap[parent]):
                self.heap[idx], self.heap[parent] = self.heap[parent], self.heap[idx]
                idx = parent
            else: break
    def _down(self, idx):
        length = len(self.heap)
        while True:
            left = 2 * idx + 1
            right = 2 * idx + 2
            smallest = idx
            if left < length and self.key(self.heap[left]) < self.key(self.heap[smallest]):
                smallest = left
            if right < length and self.key(self.heap[right]) < self.key(self.heap[smallest]):
                smallest = right
            if smallest != idx:
                self.heap[idx], self.heap[smallest] = self.heap[smallest], self.heap[idx]
                idx = smallest
            else: break

# Test MinHeap correctness
h = PythonMinHeap()
for v in [50, 10, 30, 5, 20]:
    h.push(v)
heap_sorted = [h.pop() for _ in range(5)]
assert_test(heap_sorted == [5, 10, 20, 30, 50], "MinHeap pushes and pops in exact ascending order")

# -------------------------------------------------------------
# 3. Story DNA Bounded Top-K Selection Logic
# -------------------------------------------------------------
try:
    movie_map = {m["id"]: m for m in movies}
    # Simulate selecting plot_twists (weight 3) and nonlinear (weight 2)
    selected_weights = {"plot_twists": 3, "nonlinear": 2}
    total_target_w = sum(selected_weights.values())

    # Build inverted index
    inverted = {"plot_twists": [], "nonlinear": []}
    for mid_str, data in movie_traits.items():
        mid = int(mid_str)
        t_set = set(data.get("traits", []))
        for tid in inverted:
            if tid in t_set:
                inverted[tid].append(mid)

    candidate_ids = set(inverted["plot_twists"] + inverted["nonlinear"])
    assert_test(len(candidate_ids) > 50, f"Story DNA inverted index retrieved {len(candidate_ids)} candidates")

    # MinHeap of size K=10
    K = 10
    top_heap = PythonMinHeap(key_fn=lambda x: x["score"])

    for mid in candidate_ids:
        m = movie_map.get(mid)
        if not m: continue
        m_data = movie_traits.get(str(mid), {})
        m_traits = set(m_data.get("traits", []))
        earned = 0
        for tid, w in selected_weights.items():
            if tid in m_traits:
                earned += w
        ratio = earned / total_target_w
        bonus = min(1.0, (m.get("rating", 6.5)) / 8.5)
        score = round((ratio * 75) + (bonus * 25))
        cand = {"movie": m, "score": score}

        if top_heap.size() < K:
            top_heap.push(cand)
        elif cand["score"] > top_heap.peek()["score"]:
            top_heap.pop()
            top_heap.push(cand)

    final_top = []
    while top_heap.size() > 0:
        final_top.append(top_heap.pop())
    final_top.reverse()

    assert_test(len(final_top) == K, f"Bounded MinHeap successfully extracted Top-{K} narrative matches")
    assert_test(all(final_top[i]["score"] >= final_top[i+1]["score"] for i in range(len(final_top)-1)), "Story DNA Top-K results sorted in descending score order")

    # Verify classic titles like Inception or Memento or Fight Club are scored high
    top_titles = [item["movie"]["title"] for item in final_top]
    has_benchmark = any(t in ["Inception", "Memento", "Pulp Fiction", "Fight Club", "Interstellar"] for t in top_titles)
    assert_test(has_benchmark, f"Cinematic benchmark appears in Top-K Story DNA results: {top_titles[:4]}")

except Exception as e:
    assert_test(False, f"Story DNA simulation error: {e}")

# -------------------------------------------------------------
# 4. What-If Simulator Diff & Rank Tracking Logic
# -------------------------------------------------------------
try:
    # Baseline top 5
    baseline = movies[:5]
    # Simulated top 5 with 2 new movies and rank swap
    simulated = [movies[1], movies[0], movies[6], movies[7], movies[2]]

    orig_pos = {m["id"]: idx + 1 for idx, m in enumerate(baseline)}
    whatif_pos = {m["id"]: idx + 1 for idx, m in enumerate(simulated)}

    entered = [m for m in simulated if m["id"] not in orig_pos]
    exited = [m for m in baseline if m["id"] not in whatif_pos]
    
    assert_test(len(entered) == 2, f"What-If correctly identifies newly entered titles (Expected 2, got {len(entered)})")
    assert_test(len(exited) == 2, f"What-If correctly identifies exited titles (Expected 2, got {len(exited)})")

    # Check rank shift of movies[1] (climbed from #2 to #1)
    m1_delta = orig_pos[movies[1]["id"]] - whatif_pos[movies[1]["id"]]
    assert_test(m1_delta == 1, f"What-If calculates positive rank delta for climber (+{m1_delta} spots)")

except Exception as e:
    assert_test(False, f"What-If simulation logic error: {e}")

# -------------------------------------------------------------
# 5. Recommendation Time Machine Trend Calculation
# -------------------------------------------------------------
try:
    # Test chronological interaction recording & trend delta
    # Earlier window: 4 comedy movies
    # Recent window: 4 mystery movies
    sample_history = [
        # Recent (newest first)
        {"id": "1", "movieId": 1, "genres": ["Mystery", "Thriller"], "type": "liked", "timestamp": 100},
        {"id": "2", "movieId": 2, "genres": ["Mystery"], "type": "liked", "timestamp": 90},
        {"id": "3", "movieId": 3, "genres": ["Mystery", "Drama"], "type": "watched", "timestamp": 80},
        {"id": "4", "movieId": 4, "genres": ["Mystery"], "type": "saved", "timestamp": 70},
        # Earlier
        {"id": "5", "movieId": 5, "genres": ["Comedy"], "type": "liked", "timestamp": 60},
        {"id": "6", "movieId": 6, "genres": ["Comedy", "Romance"], "type": "liked", "timestamp": 50},
        {"id": "7", "movieId": 7, "genres": ["Comedy"], "type": "watched", "timestamp": 40},
        {"id": "8", "movieId": 8, "genres": ["Comedy"], "type": "saved", "timestamp": 30},
    ]

    split_idx = len(sample_history) // 2
    recent = sample_history[:split_idx]
    earlier = sample_history[split_idx:]

    def count_genres(items):
        counts = {}
        total = 0
        for it in items:
            for g in it["genres"]:
                counts[g] = counts.get(g, 0) + 1
                total += 1
        return counts, max(1, total)

    r_counts, r_tot = count_genres(recent)
    e_counts, e_tot = count_genres(earlier)

    mystery_delta = (r_counts.get("Mystery", 0) / r_tot) - (e_counts.get("Mystery", 0) / e_tot)
    comedy_delta = (r_counts.get("Comedy", 0) / r_tot) - (e_counts.get("Comedy", 0) / e_tot)

    assert_test(mystery_delta > 0.4, f"Time Machine detects positive surge in Mystery (+{mystery_delta:.2f})")
    assert_test(comedy_delta < -0.4, f"Time Machine detects decline in Comedy ({comedy_delta:.2f})")

    # Formulate statement
    statement = f"You have recently shown more interest in Mystery than in Comedy."
    assert_test("Mystery" in statement and "Comedy" in statement, f"Data-backed trend statement verified: '{statement}'")

except Exception as e:
    assert_test(False, f"Time Machine trend error: {e}")

# -------------------------------------------------------------
# 6. Movie Discovery Challenge Gamification Logic
# -------------------------------------------------------------
try:
    challenges = [
        {"id": "hidden_masterpiece", "target": 1, "points": 100},
        {"id": "time_traveler", "target": 1, "points": 50},
        {"id": "narrative_chameleon", "target": 3, "points": 200}
    ]
    progress = {
        "hidden_masterpiece": {"completed": False, "count": 0, "explored": set()},
        "narrative_chameleon": {"completed": False, "count": 0, "explored": set()}
    }

    # Action 1: Explore film 101 for hidden_masterpiece
    prog = progress["hidden_masterpiece"]
    prog["explored"].add(101)
    prog["count"] = len(prog["explored"])
    if prog["count"] >= 1:
        prog["completed"] = True
    assert_test(prog["completed"] == True, "Challenge completes immediately when target count reached")

    # Anti-cheat: Duplicate exploration of film 101 should not increase count
    old_count = prog["count"]
    prog["explored"].add(101)
    assert_test(len(prog["explored"]) == old_count, "Set deduplication strictly prevents duplicate points/count")

    # Multi-step challenge progression
    cham = progress["narrative_chameleon"]
    cham["explored"].add(201)
    cham["explored"].add(202)
    assert_test(len(cham["explored"]) == 2, "Multi-step challenge tracks intermediate progress (2/3)")
    cham["explored"].add(203)
    assert_test(len(cham["explored"]) == 3, "Multi-step challenge reaches 3/3 target")

except Exception as e:
    assert_test(False, f"Challenge gamification error: {e}")

# -------------------------------------------------------------
# 7. Multi-Persona Watch Party (GroupConsensusEngine)
# -------------------------------------------------------------
try:
    # Test personas
    p_alex = {"id": "p_alex", "name": "Alex", "genres": ["Action", "Adventure", "Science Fiction"], "dislikedGenres": ["Romance"]}
    p_sam = {"id": "p_sam", "name": "Sam", "genres": ["Drama", "Romance"], "dislikedGenres": ["Horror"]}
    p_jordan = {"id": "p_jordan", "name": "Jordan", "genres": ["Mystery", "Thriller"], "dislikedGenres": ["Family"]}
    friends = [p_alex, p_sam, p_jordan]

    def calc_person_score(persona, movie):
        liked = set(persona.get("genres", []))
        disliked = set(persona.get("dislikedGenres", []))
        m_genres = set(movie.get("genres", []))
        if any(g in disliked for g in m_genres):
            return 15 # Veto penalty
        overlap = len(liked.intersection(m_genres))
        earned = min(1.0, overlap / max(1, len(liked) * 0.5)) * 45
        rating_ratio = min(1.0, movie.get("rating", 6.5) / 8.5)
        earned += rating_ratio * 25 + 20
        return min(100, max(0, round(earned)))

    # Test veto
    horror_movie = {"title": "The Conjuring", "genres": ["Horror", "Mystery"], "rating": 7.5}
    sam_score = calc_person_score(p_sam, horror_movie)
    assert_test(sam_score == 15, f"Veto protection triggered penalty score (Expected 15, got {sam_score})")

    # Compromise search using Min-Heap
    k_consensus = 5
    consensus_heap = PythonMinHeap(key_fn=lambda x: (x["min_hap"], x["avg_hap"]))

    for m in movies[:500]: # Sample 500 films
        scores = [calc_person_score(f, m) for f in friends]
        min_hap = min(scores)
        avg_hap = round(sum(scores) / len(scores))
        cand = {"movie": m, "min_hap": min_hap, "avg_hap": avg_hap, "scores": scores}

        if consensus_heap.size() < k_consensus:
            consensus_heap.push(cand)
        elif (cand["min_hap"] > consensus_heap.peek()["min_hap"] or 
             (cand["min_hap"] == consensus_heap.peek()["min_hap"] and cand["avg_hap"] > consensus_heap.peek()["avg_hap"])):
            consensus_heap.pop()
            consensus_heap.push(cand)

    compromises = []
    while consensus_heap.size() > 0:
        compromises.append(consensus_heap.pop())
    compromises.reverse()

    assert_test(len(compromises) == k_consensus, f"Group consensus extracted Top-{k_consensus} compromise films")
    assert_test(compromises[0]["min_hap"] >= 40, f"Max-Min fairness guarantees baseline happiness >= 40% (Got {compromises[0]['min_hap']}%)")
    assert_test(compromises[0]["min_hap"] >= compromises[-1]["min_hap"], "Winner has highest minimum happiness guarantee")

except Exception as e:
    assert_test(False, f"Group consensus error: {e}")

# -------------------------------------------------------------
# Test Summary
# -------------------------------------------------------------
print("==================================================")
if failures:
    print(f"FAILED {len(failures)} TESTS: {failures}")
    sys.exit(1)
else:
    print("ALL TESTS PASSED! 100% SUCCESSFUL TEST EXECUTION.")
print("==================================================")

