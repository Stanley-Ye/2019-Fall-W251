### Submission
- Cloud Object Storage of 3 Videos
  1. https://s3.us-east.cloud-object-storage.appdomain.cloud/hw11-sye/frame22000.mp4
  2. https://s3.us-east.cloud-object-storage.appdomain.cloud/hw11-sye/frame23000.mp4
  3. https://s3.us-east.cloud-object-storage.appdomain.cloud/hw11-sye/frame24000.mp4

- Models:
  1. Model #1 -> Original code, configured to run for 25K steps due to long 15hr runtime for 50K steps on my TX2.
     * Runtime for 25K steps: 6hr
     * Number of successful landings: 30
     
  2. Model #2 -> Model #1 + Replaced optimizer (adam) with (adamax).
     * Runtime for 25K steps: 6hr
     * Number of successful landings: 36
     * Compared to the baseline Model #1, Model #2 yields 20% more successful landings.  This is a predictable result since the AdaMax optimizer has known advantages versus the Adam optimizer.

  3. Model #3 -> Model #2 + Reduced model re-training frequency from every 1K to 5K steps.
     * Runtime for 25K steps: 5.5hr
     * Number of successful landings: 15
     * Compared to Models #1 and #2, Model #3 has much worse performance in terms of successful landings.  This reduction in successful landings is the direct result of re-training the model at large intervals of 5000 steps instead of 1000 steps.

