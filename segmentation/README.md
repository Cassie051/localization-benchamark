# Trajectory segmentation

This folder contains the segmentation of the two Oxford Spires sequences used in the paper into
**Indoor**, **Outdoor**, and **Transition** (indoor–outdoor) segments.

| File | Content |
|---|---|
| `crossings.csv` | The annotated threshold crossings $b_k$ (doorways/passages), numbered per sequence as in the paper (Appendix B, Fig. B1), with the transition window each one belongs to. |
| `timestamps/<sequence>_timestamps.csv` | Start and end time (ns and UTC) of every segment, i.e. of every ROS 2 bag used in the evaluation. |

All times are ROS bag receive times of the original Oxford Spires recordings.

## Segmentation rule

1. **Crossings.** The crossing timestamps $b_k$ were labelled manually as the moments when the sensor rig passes the
   threshold of a doorway or passage, identified from the camera images and from the change of the LiDAR scan
   between an enclosed and an open structure. This is the only manual step.
2. **Pure Indoor/Outdoor segments** span $[b_k + g,\; b_{k+1} - g]$ with a guard band $g = 3$ s.
   Ambiguous zones that could not be labelled as indoor or outdoor (e.g. roofed passages) are not used.
3. **Transition windows** span $[b_k - w,\; b_k + w]$ with $w = 6$ s, i.e. they overlap the neighbouring pure
   segments by $w - g = 3$ s. Crossings that follow each other in quick succession are merged into one window
   $[b_{first} - w,\; b_{last} + w]$ (Seq 02 Transition 2: $b_2$–$b_5$; Seq 02 Transition 3: $b_6$–$b_7$;
   Seq 05 Transition 3: $b_3$–$b_7$).
4. **Exceptions.** In Seq 05 the end of Transition 1 is extended by 10 s and the end of Transition 4 by 6 s to include
   the whole doorway area.

Each segment was cut into a separate ROS 2 bag and processed by an independently initialised run of every algorithm.

## Bag names and labels used in the paper

| Sequence | Bag | Label in the paper | Duration [s] |
|---|---|---|---|
| Seq 02 | `oxford_outdoor_bag_1` | Outdoor 1 | 250.4 |
| Seq 02 | `oxford_doorway_bag_0` | Transition 1 | 12.0 |
| Seq 02 | `oxford_indoor_bag_2` | Indoor 1 | 172.8 |
| Seq 02 | `oxford_doorway_bag_1` | Transition 2 | 98.4 |
| Seq 02 | `oxford_outdoor_bag_2` | Outdoor 2 | 7.6 |
| Seq 02 | `oxford_outdoor_bag_3` | Outdoor 3 | 21.4 |
| Seq 02 | `oxford_indoor_bag_3` | Indoor 2 | 27.7 |
| Seq 02 | `oxford_doorway_bag_2` | Transition 3 (ground truth covers the first 11.9 s) | 32.7 |
| Seq 02 | `oxford_outdoor_bag_4` | Outdoor 4 (ground truth covers only 2.9 s; not evaluated) | 14.7 |
| Seq 02 | `oxford_indoor_bag_5` | — (after the end of the ground truth; not evaluated) | 12.6 |
| Seq 05 | `oxford_indoor_bag_1` | Indoor 1 | 124.5 |
| Seq 05 | `oxford_doorway_bag_0` | Transition 1 | 22.0 |
| Seq 05 | `oxford_outdoor_bag_2` | Outdoor 1 | 209.8 |
| Seq 05 | `oxford_doorway_bag_1` | Transition 2 | 12.0 |
| Seq 05 | `oxford_indoor_bag_3` | Indoor 2 | 271.2 |
| Seq 05 | `oxford_doorway_bag_2` | Transition 3 | 112.2 |
| Seq 05 | `oxford_outdoor_bag_5` | Outdoor 2 | 12.0 |
| Seq 05 | `oxford_outdoor_bag_7` | Outdoor 3 | 17.0 |
| Seq 05 | `oxford_indoor_bag_8` | Indoor 3 | 49.2 |
| Seq 05 | `oxford_doorway_bag_3` | Transition 4 | 18.0 |
| Seq 05 | `oxford_outdoor_bag_9` | Outdoor 4 | 18.1 |

Seq 02 = `2024-03-18-christ-church-02`, Seq 05 = `2024-03-20-christ-church-05`.
The ground truth (Oxford Spires) ends at 09:37:30.8 UTC in Seq 02, so the last Seq 02 segments are only partly covered.

## Recreating the segments

The bags can be cut from the original Oxford Spires ROS 2 recordings with any bag-filtering tool, keeping the
messages whose receive time lies in `[start_time_ns, end_time_ns]` of the corresponding row of the timestamp file.

## License

The files in this folder are derived from the [Oxford Spires Dataset](https://dynamic.robots.ox.ac.uk/datasets/oxford-spires/)
and are provided under the same license as the dataset,
[CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/). Please cite the Oxford Spires Dataset when using them.
