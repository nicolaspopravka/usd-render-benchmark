# USD Render Benchmark

| Scene \ Renderer | Arnold | Cycles | Embree | GL | Karma CPU | Karma XPU | Moonray | Prman | RenderMan RIS | RenderMan XPU | RenderMan XPU - CPU | RenderMan XPU - GPU |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| McUsd | Success<br>0:25.62<br>1485568KB | Success<br>0:52.15<br>1148748KB | Success<br>0:07.60<br>291452KB | Success<br>0:04.04<br>423972KB | Success<br>0:35.53<br>2760948KB | Success<br>0:30.50<br>1885180KB | Success<br>3:49.08<br>1684372KB | Success<br>0:29.82<br>1717528KB | Failure<br>0:35.70<br>2359716KB | Failure<br>0:59.08<br>1766564KB | Failure<br>0:30.19<br>1251696KB | Failure<br>0:41.42<br>1678820KB |
| chess_set | Success<br>0:22.42<br>2000288KB | Success<br>0:10.46<br>951836KB | Success<br>0:04.02<br>465436KB | Success<br>0:05.13<br>1424428KB | Success<br>0:15.58<br>2733672KB | Success<br>0:22.62<br>2230916KB | Success<br>0:07.50<br>1746384KB | Success<br>0:13.36<br>2016408KB | Failure<br>0:24.53<br>2496332KB | Failure<br>0:44.54<br>1933604KB | Failure<br>0:22.12<br>1697304KB | Failure<br>0:25.76<br>1923624KB |
| entry | Success<br>7:01.83<br>8005408KB | N/A<br>N/A<br>N/A | Success<br>0:18.26<br>3482756KB | Failure<br>0:22.08<br>9403480KB | Success<br>3:37.48<br>17390112KB | Success<br>4:33.22<br>27241296KB | Success<br>11:47.25<br>20974680KB | Failure<br>1:19.36<br>14736392KB | Failure<br>1:32.08<br>14324416KB | Failure<br>3:02.99<br>20276684KB | Failure<br>1:15.57<br>10894680KB | Failure<br>3:12.26<br>20106728KB |
| island | N/A<br>N/A<br>N/A | N/A<br>N/A<br>N/A | Success<br>3:37.19<br>41786964KB | Failure<br>1:26.30<br>16152528KB | Success<br>5:39.35<br>38774460KB | Success<br>5:10.12<br>49066136KB | N/A<br>N/A<br>N/A | Success<br>18:04.98<br>62175844KB | Failure<br>16:33.72<br>61906312KB | Failure<br>21:33.45<br>61858560KB | Failure<br>8:09.06<br>62165672KB | Failure<br>22:18.73<br>61967188KB |
## System Specs
2 x Intel(R) Xeon(R) CPU E5-2686 v4 @ 2.30GHz (36 cores, 72 logical) with 64125MB
NVIDIA driver version 535.113
GPU 0: NVIDIA RTX A4000 @ 1560MHz (compute 8.6) with 16108MB (13922MB available) (NVLink:0)
