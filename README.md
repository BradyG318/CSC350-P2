LINK:
https://quinnipiacuniversity-my.sharepoint.com/:f:/g/personal/bmgalligan_quinnipiac_edu/IgD6VNO7BE3VQ5YiWRxuocSvAQRnrm4q-MKmy2FnP1qKniY?e=wgAZ3o


1a. What are the assumptions that the k-means algorithm makes of the input data?
The assumptions that the k-means algorithm makes are that the clusters are almost spherical, have similar size/density, each data point belongs to the nearest centroid, and the number of clusters(k) is known. 
1b. Each input file has the original generating clusters in the filename before the “.dat” extension. For example, bullseye2.dat was generated with 2 clusters. For each input file provided, run k-means 3 times with the k value indicated by the filename. 
Record the WCSS of each run in the Columns B-D of the given p2-results.xlsx Excel file. Be sure to visualize the results for each run. For which files does k-means clustering appear to succeed always/sometimes/never in your sample of 3 runs?
Always succeeds: diffdensity2, diffstddev2, easygaussian1, easygaussian2, hardgaussian1, hardgaussian2, stretched2 (All produce identical or similar WCSS across the 3 tests, meaning the algorithm is reliably finds the correct cluster.
Sometimes succeeds: easygaussian3 through easygaussian9, and hardgaussian3 through hardgaussian9(For these, the WCSS varies across the 3 tests. I found that higher values of K led to a greater amount of variation in the tests.
Never succeeds: bullseye2(While the WCSS’s are close in value, the images depict rings, which violates the assumption that the clusters are almost spherical. 
1c. For those problems where k-means appears to always fail, which assumptions (if any) of the k-means algorithm are violated?
As stated earlier, in Bullseye2, the clusters are shaped rings rather than spherical. This means that the clusters are not spherical and separable by proximity to a centroid. The nearest centroid assignment cannot correctly recover ring shaped clusters, as a point in the inner ring may be closer to the centroid in the outer ring.
1d. Is it possible for k-means to fail if no assumptions are violated? Why or why not?
K-means can still fail even when no assumptions are violated because k-means uses random initialization to converge to a local minimum rather than the global optimum.

	EXERCISE 1				
Data File	Run #1 WCSS	Run #2 WCSS	Run #3 WCSS	Median	Minimum
bullseye2	23.43100186	22.38462018	22.54196633	22.54196633	22.38462018
diffdensity2	9.797249415	9.797249415	9.797249415	9.797249415	9.797249415
diffstddev2	1.12140865	1.12140865	1.12140865	1.12140865	1.12140865
easygaussian1	0.506134593	0.506134593	0.506134593	0.506134593	0.506134593
easygaussian2	0.559716829	0.559716829	0.559716829	0.559716829	0.559716829
easygaussian3	6.312707143	0.51026754	0.51026754	0.51026754	0.51026754
easygaussian4	0.470062065	4.651798372	0.470062065	0.470062065	0.470062065
easygaussian5	0.510571882	2.240101455	2.392562037	2.240101455	0.510571882
easygaussian6	1.457665523	0.463040617	0.463040617	0.463040617	0.463040617
easygaussian7	1.14254456	0.453674848	1.127864164	1.127864164	0.453674848
easygaussian8	0.725215106	0.353514084	1.286750853	0.725215106	0.353514084
easygaussian9	0.824871755	0.874922038	0.413312759	0.824871755	0.413312759
hardgaussian1	0.461020096	0.461020096	0.461020096	0.461020096	0.461020096
hardgaussian2	0.542170273	0.542170273	0.542170273	0.542170273	0.542170273
hardgaussian3	0.429880227	0.427194009	0.427194009	0.427194009	0.427194009
hardgaussian4	0.440394468	0.395915872	0.39005732	0.395915872	0.39005732
hardgaussian5	0.578032875	0.566094006	0.430960196	0.566094006	0.430960196
hardgaussian6	0.534559009	0.549605898	0.43472164	0.534559009	0.43472164
hardgaussian7	0.399882059	0.390715654	0.386440471	0.390715654	0.386440471
hardgaussian8	0.631237519	0.35932551	0.369341757	0.369341757	0.35932551
hardgaussian9	0.358723416	0.395898009	0.351926584	0.358723416	0.351926584
stretched2	1.258313243	1.258313243	1.258313243	1.258313243	1.258313243
