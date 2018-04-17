The Session Track released 1021 query sessions for 60 different topics.
The top 10 results from the first 100 sessions from the top
3 highest-priority submitted runs were pooled; the resulting set
of URLs were judged against the general topic. Judging was
conducted on a 6-grade scale: spam (-2), not relevant (0), relevant (1),
highly relevant (2), key (3), and navigational (4). 
Note that topics numbered 1, 11, 12, 38, 41, 43, 45, 49, and 50 received no 
judgments, as they were not represented in the first 100 sessions.

Based on the qrels provided by NIST, we evaluated runs by eight 
measures,
(a) Average Precision (average_precision)
(b) Expected Reciprocal Rank (err) -- as defined by Chapelle et al.
	at CIKM 2009,
(c) ERR@10 (err_at_k),
(d) nDCG (ndcg),
(e) nDCG@10 (ndcg_at_k),
(f) ERR normalised by the maximum ERR per query (nerr),
(g) nERR@10 (nerr_at_k), and
(h) Precision@10 (precision_at_k)

Each run was evaluated over the first 100 sessions. 
nDCG@10 (ndcg_at_k) is the official measure for the track.
