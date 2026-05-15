# Chapter 5: Methodology
> **Status:** DRAFT

> **Key Finding:** Two-study design: (1) controlled lab study with 40 commercial fishermen, within-subjects spatial vs non-spatial condition; (2) six-month field deployment on 4 commercial vessels running actual fishing operations. RQ1 tests spatial organization effect. RQ2 tests delta vs continuous recording.

This chapter describes the research methodology for evaluating the four research questions posed in Chapter 1. The methodology consists of two complementary studies: a controlled lab study and a six-month field deployment on commercial fishing vessels.

The lab study provides controlled conditions for measuring performance differences between spatial and non-spatial knowledge systems. The field study provides ecological validity — testing PLATO in the conditions where it will actually be used.

---

## 5.2 Study 1: Controlled Lab Study

### 5.2.1 Objective

**RQ1:** Does explicit spatial organization through rooms improve agent performance on spatially-grounded tasks?

**RQ2:** Does change-based recording produce more efficient and accurate knowledge representations?

### 5.2.2 Design

**Within-subjects design.** Each participant completes the same tasks in both conditions:

1. **Spatial condition:** PLATO rooms with voice input
2. **Non-spatial condition:** Flat database with manual text entry

Task order is counterbalanced. Participants are randomly assigned to starting condition.

### 5.2.3 Participants

- **N = 40** commercial fishermen
- Recruitment: through fishing cooperative partnerships
- Inclusion: currently active commercial fishing, no prior PLATO experience
- Exclusion: unable to use voice interface (hearing impairment)

### 5.2.4 Task Scenario

Participants complete a simulated fishing scenario in a controlled lab setting:

**Scenario:** You are on a boat in unfamiliar waters. You need to:
1. Locate productive fishing grounds based on historical reports
2. Monitor changing conditions during a fishing operation
3. Coordinate with other simulated vessels
4. Make decisions about where to go next

The scenario is delivered via a simulated bridge interface with:
- Simulated depth sounder readings
- Simulated weather updates
- Simulated radio reports from other vessels
- Historical PLATO data (in spatial condition) or historical text database (in non-spatial condition)

### 5.2.5 Measures

| Construct | Measure | Method |
|-----------|---------|--------|
| Task performance | Time to locate productive grounds | Simulation log |
| Decision quality | Expert rating of decision appropriateness | Blind review by 3 captains |
| Knowledge accuracy | Post-scenario quiz on conditions encountered | 20-item quiz |
| System usability | System Usability Scale (SUS) | Likert questionnaire |
| Cognitive load | NASA-TLX | Likert questionnaire |
| Satisfaction | Custom 10-point scale | Likert questionnaire |

### 5.2.6 Analysis Plan

**Primary analysis:** Paired t-test (spatial vs non-spatial) on task performance and decision quality.

**Secondary analysis:** Regression of task performance on cognitive load, usability, and knowledge accuracy.

**Sample size justification:** With N=40 and alpha=0.05, we have 80% power to detect a medium effect size (d=0.5) in a paired design.

---

## 5.3 Study 2: Field Deployment

### 5.3.1 Objective

**RQ3:** Can agents develop effective presence in spaces through accumulated change records?

**RQ4:** Can fishermen with no software experience effectively use voice-driven spatial knowledge systems in maritime conditions?

### 5.3.2 Design

**Longitudinal observational study.** Six-month deployment on commercial fishing vessels with pre/post assessments.

### 5.3.3 Participants

- **N = 20** commercial fishing vessels
- **Partners:** Bering Sea fishing cooperative (TBD partnership)
- Vessels include: salmon trollers, longliners, pot coders
- Crew sizes: 1-4 per vessel

### 5.3.4 Deployment Package

Each participating vessel receives:
1. **PLATO Voice tablet** — ruggedized tablet with PLATO Voice interface
2. **PLATO room access** — dedicated rooms for vessel and captain
3. **Fleet rooms** — shared rooms with other participating vessels
4. **Training** — 2-hour onboarding session

### 5.3.5 Procedure

**Month 1-2:** Baseline recording + initial use
- Voice interface only, no agent responses
- Record all voice entries, measure engagement
- Assess usability and barriers

**Month 3-4:** Agent responses enabled
- Fleet agents begin responding to queries
- Monitor usage patterns and satisfaction
- Collect qualitative feedback

**Month 5-6:** Full deployment
- All features active
- Continued monitoring
- Exit interviews with captains

### 5.3.6 Measures

| Construct | Measure | Timing |
|-----------|---------|--------|
| Usage | Voice entries per week | Weekly |
| Engagement | Rooms visited, time in app | Weekly |
| Knowledge growth | Unique observations accumulated | Monthly |
| System reliability | Uptime, error rate | Continuous |
| Task completion | Captain-reported usefulness (1-5) | Monthly |
| Adoption | Continued use vs abandonment | End of study |
| Qualitative feedback | Semi-structured interviews | Months 2 and 6 |

### 5.3.7 Hypotheses for RQ3

**H3a:** Agents with 6 months of presence in rooms will demonstrate measurable familiarity with room history, as evidenced by relevant responses to novel queries.

**H3b:** The relevance of agent responses will increase with presence duration (presence → familiarity → relevance).

**Measurement:** Blind review of agent responses by expert captains, rated 1-5 for relevance and accuracy.

### 5.3.8 Hypotheses for RQ4

**H4a:** Fishermen will generate more observations via voice than via manual entry in comparable systems.

**H4b:** Voice entry quality (measured by completeness and accuracy) will be higher than manual entry quality.

**H4c:** System abandonment rate will be lower than comparable software tools in maritime settings (<20% at 6 months).

---

## 5.4 Presence Measurement

### 5.4.1 Defining Presence for Measurement

Presence is difficult to measure directly — it is a subjective experience. We use three proxy measures:

1. **Behavioral presence:** Time spent in rooms, frequency of contribution, responsiveness to room events
2. **Declarative presence:** Self-reported sense of "the system knowing what I'm seeing"
3. **Performance presence:** Task performance improvement attributable to system knowledge

### 5.4.2 Behavioral Measures

```python
presence_metrics = {
    "time_in_rooms": total_seconds_connected,
    "tiles_submitted": count_of_contributions,
    "tiles_received": count_of_observations,
    "active_rooms": count_of_distinct_rooms,
    "cross_room_patterns": count_of_multi_room_observations,
    "session_frequency": sessions_per_week
}
```

### 5.4.3 Declarative Measures

Semi-structured interview prompts:
- "When you're on the water, do you feel like the system understands what you're seeing?"
- "Does the system ever surprise you by knowing something you didn't expect it to know?"
- "Do you trust the system's knowledge about these waters?"

Responses coded for: presence, trust, surprise, accuracy

---

## 5.5 Data Management

### 5.5.1 Privacy

All data is collected with informed consent. Participants can withdraw at any time. Data is anonymized for analysis.

Voice recordings are transcribed and the recordings are deleted after transcription verification.

### 5.5.2 Storage

- PLATO server stores tiles with author identifiers
- Analytics stored separately, linked only by anonymous participant ID
- Interview recordings stored encrypted, deleted after analysis

### 5.5.3 Security

- All data transmitted over HTTPS
- Vessel-to-fleet communication uses mutual TLS
- Captains can delete their own tiles

---

## 5.6 Ethical Considerations

### 5.6.1 Informed Consent

Participants are informed of:
- What data is collected
- How it will be used
- Who will have access
- Their right to withdraw

### 5.6.2 Risk Mitigation

The system is not used for navigation or safety-critical decisions. Participants are explicitly told:
- PLATO is for knowledge sharing, not navigation
- Always use official charts and safety equipment
- The system may contain errors

### 5.6.3 Benefit Sharing

Participants receive:
- Access to the fleet's shared knowledge
- Summary reports of their contribution
- Early access to findings

### 5.6.4 Data Sovereignty

Fishing data is culturally and economically sensitive. Participating captains retain ownership of their observations. Any use of data beyond this study requires explicit consent.

---

## 5.7 Timeline

| Phase | Duration | Activities |
|-------|----------|------------|
| Recruitment | 2 months | Partner recruitment, participant enrollment |
| Lab study | 1 month | Controlled experiments, data collection |
| Field deployment Month 1-2 | 2 months | Baseline recording, initial use |
| Field deployment Month 3-4 | 2 months | Agent responses enabled |
| Field deployment Month 5-6 | 2 months | Full deployment |
| Exit interviews | 1 month | Final data collection |
| Analysis | 2 months | Data analysis |
| Writing | 3 months | Dissertation writing |

**Total:** 14 months

---

## 5.8 Limitations

1. **Lab study ecological validity:** Simulated conditions differ from real fishing
2. **Field study lack of control:** Cannot isolate causal factors
3. **Self-selection:** Participants who volunteer may differ from typical fishermen
4. ** Hawthorne effects:** Awareness of being studied may change behavior
5. **Single fishery:** Bering Sea salmon may not generalize to other fisheries

---

## 5.9 Summary

The methodology combines controlled experimentation with longitudinal field deployment:

- **Study 1:** Lab study measuring spatial vs non-spatial performance (RQ1, RQ2)
- **Study 2:** Field deployment measuring presence development and usability (RQ3, RQ4)

Together, these studies provide both internal validity (controlled) and external validity (ecologically real) for the findings.

---

**Keywords:** methodology, lab study, field deployment, longitudinal study, presence measurement, maritime AI
