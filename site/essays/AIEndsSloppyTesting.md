---
title: "Will AI end sloppy testing?"
date: "Nov 2026"
---

I have fond memories of chemistry lab from high school. In one experiment, we would pipette oxalic acid into a conical flask, add a drop of phenolphthalein, and drip sodium hydroxide from a burette until the liquid turned pink. The first run was always a rough one, to find out where the endpoint lay. We would then repeat the experiment, slowing down to single drops near the end point, and reading the meniscus at eye level. We weren't allowed to conclude the experiment until we had three readings within 0.1 ml of each other. 

Experimentation is at the core of quality engineering. However, while testing software, I've rarely seen this level of rigour applied. This isn't a high bar – I am talking about high school science. But I sense that this is about to change. Testing an AI system made me deeply unsure of my results. Writing a test for an LLM is hard. If a test passed once, I couldn't be sure it would pass again. If it passed twice, I still wasn't sure if that was good enough.

This dilemma reminded me of the concept of statistical validity, that I had also picked up during my education. While calibrating and LLM judge with a human domain expert, for pass / fail judgements, my LLM judge has a 50% probability of returning the same answer as a domain expert by sheer chance. How can I keep the role of chance within bounds? These are problems to which statisticians offer solutions. A [binomial distribution](https://en.wikipedia.org/wiki/Binomial_distribution) quantifies the confidence we can derive from pass / fail test results. [Cohen's Kappa ](https://en.wikipedia.org/wiki/Cohen%27s_kappa) quantifies inter-rater reliability. Testing AI systems will require us to adopt these concepts into our processes.

This realization has made an uncomfortable truth hard to ignore – sloppy practices are widespread in software testing today. Software testing could have always benefitted from more rigourous approaches grounded in sound experimental design and statistical methods. Such methods are already well established in industrial and manufacturing quality (think six-sigma). With conventional software, most quality engineers (me included) got away with not applying this level of rigour. The software industry didn't encourage this level of rigour either. This is why so much software we use today sucks. 

AI software turns dangerous quickly in the absence of rigorous, and dare I say, scientific testing. Consider an [AI medical transcription tool that mistypes or hallucinates](https://futurism.com/the-byte/whisper-nabla-hospital-ai-details-patients), or an [AI criminal sentencing tool that is biased](https://incidentdatabase.ai/reports/36/). With widespread AI adoption, I foresee the harm done by such sloppily tested systems multiplying past the point where we can keep ignoring them. 

I hold out hope that the rise of AI will infuse much needed rigour to the software testing discipline. 