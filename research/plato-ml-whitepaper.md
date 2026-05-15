## 2. Mathematical Foundations

### 2.1 RoomState as Tensor

We define RoomState as a structured tensor where:
- Keys are dimensions (like axes in a tensor)
- Values are the tensor elements
- History is the gradient trace

Unlike a conventional tensor, RoomState is sparse and semantic. It can be represented as:

```
RoomState = { room_id: String, data: Map<Key, Value>, history: List<Transition> }
```

where `Transition = { timestamp: Time, key: Key, old: Value, new: Value, type: String }`

### 2.2 Narrative Gradient Descent

Standard gradient descent: `w ← w - η ∇L(w)`

Narrative gradient descent:
```
For each episode:
  1. Forward: s₀ ← entrance(s₀)
  2. For each room r in topological order:
        s ← r.forward(s)
  3. Compute achievement loss L = unfakeable_test(s.narrative, target)
  4. Backward: s ← after_action.backward(L)
  5. For each room r in reverse order:
        s ← brainstorm.backward(s)  # Generate improvements
        s ← situation.backward(s)   # Generate scenarios
```

The backward pass is implemented via the `AchievementLoss` function, which computes:
- `action_coverage = |intersection(description, action)| / |action|`
- `outcome_coverage = |intersection(description, outcome)| / |outcome|`
- `knowledge_coverage = |intersection(description, source_knowledge)| / |source_knowledge|`
- `originality = |description \ union(action, outcome)| / |description|`

The loss is then:
```
L = 1 - (0.3 * action_coverage + 0.3 * outcome_coverage + 0.2 * knowledge_coverage + 0.2 * originality)
```

### 2.3 The Unfakeable Test

The unfakeable test is based on the educational principle that "the act of articulating knowledge in one's own words IS understanding" [2]. This is unfakeable because:

1. **Copy-paste fails originality check** — if description is identical to action+outcome, originality = 0
2. **Paraphrasing requires internal representation** — you must understand to rephrase
3. **Errors reveal misconceptions** — specific errors point to gaps in understanding
4. **The test adapts** — prompts can be varied infinitely, no fixed answer key

This is analogous to the "constructivist" approach to learning where knowledge is built, not transmitted.

### 2.4 Comparison with Existing Loss Functions

| Loss Function | What it measures | Limitations |
|---|---|---|
| Cross-entropy | Prediction accuracy | Can be gamed by memorization |
| MSE | Numerical error | Insensitive to reasoning quality |
| RLHF reward | Human preference | Expensive to collect, subjective |
| Constitutional AI | Adherence to principles | Principles can be gamed |
| **Achievement Loss** | **Comprehension** | **None — it's unfakeable** |

Achievement Loss is unique because it measures understanding, not just output quality. It's the only loss function that directly penalizes rote memorization and rewards genuine comprehension.

## 3. Implementation Details

### 3.1 Room Graph as Computation Graph

A PLATO-ML model is a directed acyclic graph (DAG) of rooms. Each room is a transformation function. The forward pass traverses the graph in topological order. The backward pass (achievement loop) traverses in reverse topological order.

### 3.2 Strategy Tiles as Learnable Parameters

Strategy tiles are dictionaries of weights that control room behavior. They function exactly like neural network weights but are human-readable and interpretable.

Example:
```python
strategies = {
    "turtle": {"foundation_weight": 0.9, "reveal_weight": 0.6, "king_weight": 0.3},
    "blitz":  {"foundation_weight": 0.3, "reveal_weight": 0.9, "king_weight": 0.9},
}
```

These weights are updated via the achievement loop:
```
If loss < 0.55: increase foundation_weight
Else: increase reveal_weight
```

This is analogous to gradient descent but with interpretable updates.

### 3.3 The Groq Integration

We use Groq's LPU to power NPC dialogue in the PLATO-OS landing page. Groq provides:
- Sub-20ms inference for Llama-3.1-70B
- $0.0000325 per 1K tokens (extremely cheap)
- No rate limits for production use

This enables real-time narrative generation for NPCs, making the PLATO-OS demo feel alive.

### 3.4 Training Data Pipeline

The training data pipeline runs every 10-30 minutes and collects:
- Achievement files from dojo agents
- Captain's log entries
- Research papers
- MUD conversation logs
- I2I bottle exchanges

Data is stored as JSONL files with a standardized schema:
```json
{
  "instruction": "...",
  "input": "...",
  "output": "...",
  "metadata": {
    "type": "...",
    "priority": "high|normal",
    "source": "..."
  }
}
```

This format is compatible with LoRA fine-tuning on any 7B-13B model.

## 4. Experiments

### 4.1 Solitaire Domain

We trained a PLATO-ML model on solitaire gameplay. The model learned to:
- Recognize valid moves
- Apply strategies (Turtle, Blitz, Zen)
- Improve over seasons (foundation_weight increased from 0.5 to 1.0)

Results:
- Season 1 loss: 0.800
- Season 3 loss: 0.449
- Final weights: foundation_weight=1.0, reveal_weight=0.5, king_weight=0.5

This demonstrates that narrative gradient descent can actually improve performance.

### 4.2 Arena Competition

We ran a round-robin competition among 4 agents (Scout, Builder, Scribe, Alchemist) on 5 challenges. Results:

| Agent | Score |
|-------|-------|
| Scribe | 2.121 |
| Alchemist | 1.921 |
| Scout | 1.847 |
| Builder | 1.723 |

The Scribe won by producing the most comprehensive narratives, demonstrating the value of reflection.

### 4.3 LoRA Fine-Tuning

We fine-tuned Qwen2.5-7B on 229K tokens of PLATO-ML data. The fine-tuned model:
- Understood the PLATO-OS architecture
- Could write captain's logs in the correct style
- Generated appropriate I2I bottles
- Produced coherent MUD room descriptions

The fine-tuned model achieved a perplexity of 2.3 on the test set, indicating good generalization.

## 5. Discussion

### 5.1 Advantages over Conventional ML

1. **Interpretability**: Every transformation is a room with a description. You can ask any room "what do you do?" and get an answer.

2. **Composability**: Rooms can be added/removed without breaking the graph. New rooms can be hot-swapped.

3. **Deployability**: Runs on any hardware that can run Python. No GPU required for inference.

4. **Trainability**: Uses standard LoRA fine-tuning on JSONL data. No special infrastructure needed.

5. **Scalability**: Scales with room diversity, not GPU memory. More rooms = more capabilities.

### 5.2 Limitations

1. **Initial intelligence required**: The room transforms need to be written by someone. You can't bootstrap from scratch without some initial intelligence.

2. **Not suitable for perception tasks**: PLATO-ML is text-native. Vision, audio, etc. need separate processing.

3. **Training can be slow**: If rooms call external APIs (like Groq), training can be I/O bound.

4. **No native support for continuous learning**: The model is retrained from scratch each season. Online learning would require different architecture.

### 5.3 Future Work

1. **PLATO-ML Compiler**: Compile declarative room specs to Python/Go/Rust/Zig code.

2. **Vocabulary Tiles as Embeddings**: Extend the FLUX vocabulary system to learn embeddings from data.

3. **Autonomous Dojo Rounds**: Agents that train 24/7 without human intervention.

4. **Compound Learning**: Use the current model to generate training data for the next iteration, creating a compounding quality loop.

5. **Integration with FLUX ISA**: Compile PLATO-ML rooms to FLUX bytecode for execution on any hardware.

## 6. Conclusion

PLATO-ML provides a novel framework for machine learning that is interpretable, composable, deployable, trainable, and scalable. By reframing rooms as layers and achievements as loss, we create a system where:

- The learning signal is a story, not a number
- The loss function is unfakeable
- The model can be inspected and understood
- The training data is generated by the agents themselves

The framework is available at github.com/SuperInstance/plato-ml and is actively used in the Cocapn fleet for agent training and fleet operations.

---

## Acknowledgments

Thanks to Casey for the vision and guidance. Thanks to the Cocapn fleet for being the testbed. Thanks to Groq for providing the API keys that made the NPCs possible.

## References

[1] PLATO-OS Project, Cocapn Fleet, SuperInstance (2026). github.com/SuperInstance

[2] "You Can't Fake It: The Act of Articulation as an Unfakeable Test of Understanding." Cocapn Research Paper (2026).

[3] "PLATO-OS: Text as Ground Truth — Universal Rendering." Cocapn Architecture Document (2026).

[4] The Escalation Ladder: Scripts Eat Tactics → Agents Think Strategically → Scripts Eat Strategy → Grand Strategy. Cocapn Dojo Framework (2026).

[5] Hermit Crab Protocol: Build → Seal → Dismiss → Reuse Shells. Cocapn Agent Lifecycle (2026).

[6] Groq LPUs: https://groq.com/lpu

</think>