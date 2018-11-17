---
comments: true
date: 2012-08-20 00:39:23+00:00
layout: post
title: The fuel efficiency of bicycling
tags: energy
---

In the past I had always assumed biking was more fuel efficient than driving –
that any time I took a bicycle in lieu of a car I was saving money. A few years
ago I used to joke with my friends that riding my BMX bike to social gatherings
was totally worth putting up with their ridicule since I got 100 miles per
cheeseburger.

After recently picking up a road bike for commuting, I thought back about my
miles per cheeseburger (MPCB) claims, and as a more practical venture, wanted to
come up with an estimate for how the fuel efficiency of biking compared with
that of driving a car; to see how much money I could save by riding. In essence
I wanted to come up with some sort of MPG equivalent for biking.

The equivalent miles per gallon $\mathrm{MPG}_e$ formula is simply the
number of miles I could bike with a dollar’s worth of food multiplied by the
price of a gallon of automotive fuel. In other words, if you sold a gallon of
gas and bought some food, how far would the energy in that food allow you bike?
In symbolic form:

$$
\mathrm{MPG}_e = \left( \frac{\$}{\mathrm{gallon}} \right)_{\mathrm{fuel}}  
\left( \frac{\mathrm{cal}}{\mathrm{mile}}
\right)_{\mathrm{bike}}^{-1}  \left( \frac{\$}{\mathrm{cal}}
\right)_{\mathrm{food}}^{-1} .
$$

The first factor on the right hand side of the equation is the cost of fuel.
Though I drive a diesel car, most people drive gasoline cars so I used the
average price per gallon of gasoline in the US over the last 6 months:
approximately \$3.66 [1].

The next factor to find was how many calories per mile it takes to bike.
Everydayhealth.com calculated that 50 calories per mile should be close for my
weight and 13--15 mph average speeds [2]. Using this number, it turned out
that my joke-estimate of 100 MPCB was way high. I only get a measly 7 MPCB (from
a 350 calorie junior cheeseburger)!

To calculate dollars per calorie for various foods, I used grocery store
receipts and nutrition facts labels. The cost of extra energy input for
preparation of foods that required boiling water was estimated using a 100%
efficient electric stove operating at the average price for electricity I’d been
paying for the past 11 months, \$0.18/kWh, which includes all service charges,
etc. Assuming a constant specific heat and neglecting energy lost to the room, a
cup of water takes about 76.13 kJ to boil starting from 23° C at 1 atmosphere
[4], and therefore costs about 4 cents per cup to boil. Instructions on the
packaging were used to determine how much water was necessary for each food.
Surprisingly, this added cost is relatively low. For example, for spaghetti, the
most fuel efficient food I found, cooking heat was only 6% of the total cost of
the food. For rice, the second most efficient food, cooking heat contributed
0.9% to the total food cost.

It should be noted that the equivalent MPG calculation ignores maintenance,
which seemed a fair assumption since I'm also ignoring all non-energy
nutritional content in food. It also lumps in a bunch of other factors like
government subsidies, thermal and metabolic efficiencies, cost of refining,
packaging, transport, etc. Initial investment for the purchase of the car or
bike is ignored as well, but assuming one owns both, this method---relying on
price of fuel (automotive or human) alone---seemed to be a fair balance between
accuracy and complexity.

After tabulating the data (available for download
[here](https://docs.google.com/spreadsheet/ccc?key=0AgMVIAlxIxfZdHZVU09DX2FjaXhkdkZwQVk3clpqNFE&usp=sharing)
as a Google Sheet if you care to do this yourself), it was possible
to directly compare biking and driving through the equivalent MPG metric.

The chart below shows the calculated MPG equivalent values for various foods,
and the horizontal dashed red line represents the 33.8 MPG average fuel
efficiency for passenger cars in the US for the year 2011 [3]. Unsurprisingly,
the foods with the highest MPGe were mostly complex carbohydrates, with the
exceptions pure cane sugar and eggs---eggs being the only low carb food to beat
the car's efficiency. Note the difference between regular eggs and the cage free
organic (CFO) eggs. The energy content is the same, but the higher price of the
CFO eggs drives their equivalent MPG way down.

Meats all worked out to be fairly inefficient, as expected, since creating meat
requires at least another energy conversion process after photosynthesis.
However, apples didn’t fair very well either, only hitting about 12 $\mathrm{MPG}_e$.
Carrots were almost as bad as chicken, though it could be argued that meat and
vegetables are more used for maintenance than energy.

Another interesting result was the huge drop in $\mathrm{MPG}_e$ when tomato sauce was added
to spaghetti; a 79% drop, putting it below the car's efficiency.

{% include figure.html src="/images/mpge-foods.png" caption="Comparing MPG equivalent for various foods. Dashed red line is the 2011 US national average fuel efficiency for passenger cars [3]." width="90%" %}

Overall, it's interesting how energy inefficient most of these foods are; plenty
with lower MPGe than an average car's. For a typical diet, it seems that the
fuel cost for biking is roughly the same order of magnitude as driving, but
could easily rise significantly above if foods are not chosen carefully. For
example, eating cheeseburgers as bike fuel will cost approximately 36% more than
driving.

Of course there are many other reasons to commute by bike besides fuel savings.
There are the obvious health and environmental benefits. There's the fact that
riding a bike can use up extra energy stored away as fat (the human analogue to
carrying around a can of gas in the car and never pouring it in the tank).
Commuting by bike can also save time that would normally be devoted to "useless"
exercising---exercising for the sake of getting exercise.

The simple calculations presented here show that bike commuting won't
necessarily save on fuel costs, but the equivalent MPG measure can help create
meals that will.


## References

[1] Bloomberg, "Daily National Average Gasoline Prices Regular Unleaded". <https://www.bloomberg.com/quote/3AGSREG:IND/chart>

[2] everydayhealth.com, "Calories Burned Biking". <https://www.everydayhealth.com/Calories-Burned-Biking.htm>

[3] US Bureau of Transportation Statistics, "Average Fuel Efficiency of U.S. Light Duty Vehicles". <https://www.bts.gov/publications/national_transportation_statistics/html/table_04_23.html>

[4] Moran, Shapiro, 2004. _Fundamentals of Engineering Thermodynamics_. Jon Wiley and Sons, Hoboken.
