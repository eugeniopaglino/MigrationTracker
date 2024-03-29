# MigrationTracker
This repository aims at creating a python package to monitor the stock of migrants (with different origins) in different destinations countries (i.e. the stock of immigrants of Mexican origin in the United States) leveraging Facebook Marketing API.

My goal is twofold. On the one hand I want to produce a global monthly migration stock dataset that covers a long period of time and a wide set of destination-origin pairs. On the other, I want to give to other researchers a simple tool they may use to perform migration studies using Facebook data without having to dive to deep in how the api works. Be aware that I am not a programmer thus my code may be inefficient or contain occasional mistakes, I apologise in advance.

I've added two new functions to obtain the age-sex structure of a given population (e.g. Moroccan expats in Italy). This feature should be helpfull when comparing the estimates obtained through Faebook to official statistics.

I am planning to add the possibility to segment the migrants' stock by gender, age classes, and income. However, the main challenge here, rather than interacting with the api, is the tight limit Facebook imposes on the number of api calls in a given period of time. If you aim to conduct an analysis over a large number of destinations or origins I advice you to drop the demographic characteristics.
