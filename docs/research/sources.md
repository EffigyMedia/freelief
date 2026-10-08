# Research sources

The published research behind each exercise and activity in Freelief (REQ-024). This file is the
written record behind `data/research.json`, which the Standards and research page shows. **Keep the
two in step:** every source in `data/research.json` has an entry here, under its source id and with
its DOI link, and `tools/tests/test_repo.py` fails when one is missing.

**The strength of the evidence is stated honestly**, because REQ-025 forbids any claim beyond these
sources. Each entry says what was tested, on whom, and what it found, and the date it was checked.
The sections follow the techniques in `data/research.json`. A source that backs two techniques has
its full note in the first section and a pointer in the second.

These sources support the *techniques*. No study has tested Freelief itself.

**How the 2026-10-08 checks were made.** In UNT-049 (RLG-018) a research agent confirmed every
citation through Crossref, Europe PMC, PMC or the paper itself, and the session re-checked
pallavicini2021, engelhard2010 and koo2020 on Crossref. On 2026-10-08 (AUD-063) the abstracts of
pallavicini2021, engelhard2010, lee2013, holmes2009, james2015 and koo2020 were read again on Europe
PMC to write these notes. No abstract of white2010 or vandervennet2012 was available from Crossref
or Europe PMC; their notes come from the UNT-049 check, and they say so.

## Breathing (technique `breathing`: Breathe)

- **[balban2023]** Balban, M. Y., Neri, E., Kogon, M. M., et al. (2023). Brief structured
  respiration practices enhance mood and reduce physiological arousal. *Cell Reports Medicine*,
  4(1), 100895. https://doi.org/10.1016/j.xcrm.2022.100895 — checked 2026-10-08 (PMC9873947).
  *Evidence:* a remote randomized controlled trial of daily 5-minute practices for a month. The
  exhale-focused practice (cyclic sighing: a double breath in, then a long breath out) improved
  mood and lowered respiratory rate significantly more than mindfulness meditation. Box breathing
  was one of the arms; it and cyclic hyperventilation were also higher than mindfulness, but not
  significantly. The breathing methods were not compared with each other, so the trial does not
  show that cyclic sighing did better than box breathing. No arm used a plain long out-breath such
  as 4 in, 6 out. Healthy adults, not people with panic disorder. The app's text
  (`standards.evidence.breathing`) says no more than this.
- **[zaccaro2018]** Zaccaro, A., Piarulli, A., Laurino, M., et al. (2018). How breath-control can
  change your life: A systematic review on psycho-physiological correlates of slow breathing.
  *Frontiers in Human Neuroscience*, 12, 353. https://doi.org/10.3389/fnhum.2018.00353 — checked
  2026-10-08.
  *Evidence:* a systematic review. Slow breathing (under 10 breaths a minute) is linked with more
  parasympathetic activity and with emotional control, in healthy people. Every Freelief rhythm is
  under 10 breaths a minute.
- **[meuret2010]** Meuret, A. E., Rosenfield, D., Seidel, A., Bhaskara, L., & Hofmann, S. G. (2010).
  Respiratory and cognitive mediators of treatment change in panic disorder: Evidence for
  intervention specificity. *Journal of Consulting and Clinical Psychology*, 78(5), 691–704.
  https://doi.org/10.1037/a0019552 — checked 2026-10-08.
  *Evidence:* a randomized trial in 41 people with panic disorder. A four-week breathing training
  reduced panic symptom severity, comparably to cognitive training. It used a CO2 monitor for
  feedback, which Freelief does not have, and Freelief does not copy the training.

## Pop bubbles (technique `bubbles`)

- **[webb2012]** Webb, T. L., Miles, E., & Sheeran, P. (2012). Dealing with feeling: A meta-analysis
  of the effectiveness of strategies derived from the process model of emotion regulation.
  *Psychological Bulletin*, 138(4), 775–808. https://doi.org/10.1037/a0027600 — checked 2026-10-08.
  *Evidence:* a meta-analysis of experiments on emotion-regulation strategies. Turning attention to
  something else (attentional deployment, which includes distraction) changed emotional outcomes,
  with a small effect overall. Short-term regulation in experiments, not a treatment, and not a
  study of popping bubbles.
- **[pallavicini2021]** Pallavicini, F., Pepe, A., & Mantovani, F. (2021). Commercial off-the-shelf
  video games for reducing stress and anxiety: Systematic review. *JMIR Mental Health*, 8(8),
  e28150. https://doi.org/10.2196/28150 — checked 2026-10-08.
  *Evidence:* a systematic review of 28 studies published from 2006 to 2021. Ordinary commercial
  video games, including casual games and exergames, reduced stress and anxiety in children, adults
  and older adults; most studies recruited young adults. The effects depended on the game. It is a
  review of whole games, not of a bubble field, and not of a panic attack. **No study has tested
  this activity itself.**

## Trace a shape (technique `trace`)

- **[engelhard2010]** Engelhard, I. M., van den Hout, M. A., Janssen, W. C., & van der Beek, J.
  (2010). Eye movements reduce vividness and emotionality of "flashforwards". *Behaviour Research
  and Therapy*, 48(5), 442–447. https://doi.org/10.1016/j.brat.2010.01.003 — checked 2026-10-08.
  *Evidence:* a laboratory experiment with a non-clinical sample. People held images of feared
  future events in mind while they made eye movements, or with no second task. With eye movements,
  they rated the images as less vivid and less emotional. The authors explain this as the two
  tasks competing for working memory. It tested eye movements, not tracing a shape with a finger.
- **[lee2013]** Lee, C. W., & Cuijpers, P. (2013). A meta-analysis of the contribution of eye
  movements in processing emotional memories. *Journal of Behavior Therapy and Experimental
  Psychiatry*, 44(2), 231–239. https://doi.org/10.1016/j.jbtep.2012.11.001 — checked 2026-10-08.
  *Evidence:* a meta-analysis of 15 clinical trials (EMDR with and without eye movements) and 11
  laboratory studies, 849 participants in all. Eye movements added a moderate effect in therapy
  (d = 0.41) and a large one in the laboratory (d = 0.74), strongest on vividness. It is about
  distressing memories and eye movements, not about panic or a tracing task. **No study has tested
  this activity itself.**

## Sort colors (technique `sort`)

- **[holmes2009]** Holmes, E. A., James, E. L., Coode-Bate, T., & Deeprose, C. (2009). Can playing
  the computer game "Tetris" reduce the build-up of flashbacks for trauma? A proposal from cognitive
  science. *PLoS ONE*, 4(1), e4153. https://doi.org/10.1371/journal.pone.0004153 — checked
  2026-10-08.
  *Evidence:* a laboratory experiment with volunteers. Everyone watched a distressing film of real
  injury and death; 30 minutes later they played Tetris for 10 minutes or had no task. The Tetris group had
  significantly fewer flashbacks over the next week. The idea is that a visuospatial task competes
  with mental images. It is about memories of a film, not about panic.
- **[james2015]** James, E. L., Bonsall, M. B., Hoppitt, L., et al. (2015). Computer game play
  reduces intrusive memories of experimental trauma via reconsolidation-update mechanisms.
  *Psychological Science*, 26(8), 1201–1215. https://doi.org/10.1177/0956797615583071 — checked
  2026-10-08.
  *Evidence:* two laboratory experiments with volunteers and a distressing film. A memory
  reminder followed by Tetris, 24 hours after the film, greatly reduced intrusive memories; the
  second experiment showed that both the reminder and the game were needed. Again about memories,
  not panic. **No study has tested this activity itself.**

## Ripple pond (technique `ripple`)

- **[white2010]** White, M., Smith, A., Humphryes, K., Pahl, S., Snelling, D., & Depledge, M.
  (2010). Blue space: The importance of water for preference, affect, and restorativeness ratings of
  natural and built scenes. *Journal of Environmental Psychology*, 30(4), 482–493.
  https://doi.org/10.1016/j.jenvp.2010.04.004 — checked 2026-10-08.
  *Evidence:* adults rated photographs of natural and built scenes. Scenes that held water were
  rated as more preferred, more pleasant and more restful. Ratings of photographs, not a measure of
  stress or anxiety, and not an interactive pond. (Note from the UNT-049 check; no abstract was
  available to re-read on 2026-10-08.)
- **[alvarsson2010]** — the full note is under the Visualizer, below. For the pond it is indirect:
  the pond plays soft water drops, not a nature recording. **No study has tested this activity
  itself.**

## Color a mandala (technique `mandala`)

- **[curry2005]** Curry, N. A., & Kasser, T. (2005). Can coloring mandalas reduce anxiety? *Art
  Therapy*, 22(2), 81–85. https://doi.org/10.1080/07421656.2005.10129441 — checked 2026-10-08.
  *Evidence:* a randomized experiment with 84 students after a mild anxiety induction. Twenty
  minutes of coloring a mandala, or a plaid pattern, reduced anxiety more than free drawing; the
  plaid worked as well as the mandala.
- **[vandervennet2012]** van der Vennet, R., & Serice, S. (2012). Can coloring mandalas reduce
  anxiety? A replication study. *Art Therapy*, 29(2), 87–92.
  https://doi.org/10.1080/07421656.2012.680047 — checked 2026-10-08.
  *Evidence:* a small replication of Curry and Kasser with adults after a mild anxiety induction.
  Coloring a mandala reduced anxiety more than coloring a plaid pattern or free drawing. (Note from
  the UNT-049 check; no abstract was available to re-read on 2026-10-08.)
- **[koo2020]** Koo, M., Chen, H.-P., & Yeh, Y.-C. (2020). Coloring activities for anxiety reduction
  and mood improvement in Taiwanese community-dwelling older adults: A randomized controlled study.
  *Evidence-Based Complementary and Alternative Medicine*, 2020, 6964737.
  https://doi.org/10.1155/2020/6964737 — checked 2026-10-08.
  *Evidence:* a randomized controlled study of 120 adults aged 55 to 75 in Taiwan, after a brief
  anxiety induction. Twenty minutes of mandala coloring, plaid coloring, free drawing or reading.
  Only the mandala group had significantly lower anxiety than the reading group.
  Short-term, small, and none of these studies was about a panic attack.

## Visualizer: music and rain (technique `calm`)

- **[dewitte2020]** de Witte, M., Spruit, A., van Hooren, S., Moonen, X., & Stams, G.-J. (2020).
  Effects of music interventions on stress-related outcomes: A systematic review and two
  meta-analyses. *Health Psychology Review*, 14(2), 294–324.
  https://doi.org/10.1080/17437199.2019.1627897 — checked 2026-10-08.
  *Evidence:* two meta-analyses of 104 randomized trials (9,617 participants). Music interventions
  reduced physiological stress (d = 0.38) and psychological stress (d = 0.55). The trials used many
  kinds of music; Freelief's generated pads were not studied.
- **[alvarsson2010]** Alvarsson, J. J., Wiens, S., & Nilsson, M. E. (2010). Stress recovery during
  exposure to nature sound and environmental noise. *International Journal of Environmental
  Research and Public Health*, 7(3), 1036–1046. https://doi.org/10.3390/ijerph7031036 — checked
  2026-10-08.
  *Evidence:* **weak.** One experiment with 40 people after a stressful task. Skin conductance
  tended to recover faster during nature sound (a fountain and birds) than during road noise;
  heart-rate variability showed no effect. Freelief's rain is synthesized noise, not a nature
  recording, so the link is indirect, and the app says so. The Visualizer itself has not been
  studied.

## About all the activities (technique `distraction`)

- **[webb2012]** — the full note is under Pop bubbles, above: distraction eases strong feelings a
  little, for a short time.
- **[helbiglang2010]** Helbig-Lang, S., & Petermann, F. (2010). Tolerate or eliminate? A systematic
  review on the effects of safety behavior across anxiety disorders. *Clinical Psychology: Science
  and Practice*, 17(3), 218–233. https://doi.org/10.1111/j.1468-2850.2010.01213.x — checked
  2026-10-08.
  *Evidence and caveat:* a systematic review. Behaviors used to escape anxiety, which can include
  distraction, may keep an anxiety disorder going in the long term, though the evidence is mixed.
  **This is why Freelief offers distraction for the moment and never presents it as a way to
  overcome panic.** A person with frequent attacks is better served by a professional, and the
  Standards and research page says so.

## Removed 2026-10-08 (UNT-032)

The owner removed 5-4-3-2-1 grounding and calming statements on 2026-10-07 (UNT-032), because their
research was weak. This file kept their sections until 2026-10-08 (AUD-063). They are kept here as a
record only. No screen uses them, and `data/research.json` does not cite them.

### 5-4-3-2-1 grounding

- Scott, K. M., & Duncan, K. (2025). Ground yourself: Using five senses technique to cope with test
  anxiety among nursing students. *Teaching and Learning in Nursing* (Elsevier).
  https://www.sciencedirect.com/science/article/pii/S1557308725002999 — checked 2026-10-07
  (abstract and conference poster; the full text is behind a paywall).
  *Evidence:* **weak.** One group, before and after, no control group, 48 students who completed
  both surveys. Test anxiety scores fell after training in the 5-4-3-2-1 technique. No randomized
  trial of the 5-4-3-2-1 sequence itself was found.

### Calming statements (coping self-statements)

- Saunders, T., Driskell, J. E., Johnston, J. H., & Salas, E. (1996). The effect of stress
  inoculation training on anxiety and performance. *Journal of Occupational Health Psychology*,
  1(2), 170–186. https://doi.org/10.1037/1076-8998.1.2.170 — checked 2026-10-07.
  *Evidence:* a meta-analysis of 37 studies (1,837 participants). Stress inoculation training,
  whose core is rehearsed coping self-statements, reduced state and performance anxiety. The
  statements were part of a trained programme, not read alone in a moment of panic.
- Clark, D. M. (1986). A cognitive approach to panic. *Behaviour Research and Therapy*, 24(4),
  461–470. https://doi.org/10.1016/0005-7967(86)90011-2 — checked 2026-10-07.
  *Evidence:* the founding cognitive model of panic: panic grows from a catastrophic reading of
  body sensations. A theory paper, not a trial.
