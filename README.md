# festinaepaper
## Just another e-Paper weather station in a watch case.

Got the sample code from here: https://github.com/waveshare/e-Paper
Probably should have forked it, but I had no idea how github works. I still don't.

### Instructions (probably incomplete)
- Check the paths under /examples/getweathertoscreen.sh
- Check the paths under /examples/get_weather.py
- Install the fonts that you can find under "pic" if you wish to see them in the code. They will still render in the screen if not installed.
- Provide your api key for darksky in file /examples/getweathertoscreen.sh
- Provide your api key for Pushbullet in file /examples/get_weather.py - I believe this needs fixing, but it has worked in the past. It's configured to send an alert if strong wind is coming.
- Cross fingers
- Run /examples/getweathertoscreen.sh

### notes:
- pushbullet code is a mess. There are leftovers of two different ways of triggering the push. I forgot which one is the most finished.
- Some icons aren't coherent with the rest (different thickness), even if they are the same font.
- Last two lines give the extended forecast. For some reason, the two last letters in each line aren't rendered. I don't think it's the code, but it might be the code. Or the way the screen renders the text. I don't know and I don't care.
- Some icons still need some improved alignment. Don't look too hard if you suffer from OCD.

### Currently shows:
- Time of weather forecast
- Wind direction (changes to strong wind icon when there is strong wind - You don't even need to look outside!!)
- Moon phase
- Current weather icon (big! You can see it from at least 3 meters away. Maybe more, but my room is small, so can't test)
- Current temperature, and a convenienc arrow to tell you if the temperature will rise or fall. No more guessing!
- Current weather description
- Forecast for 3, 6 and 9 hours from "now", with forecasted temperature and icon.
- Extended weather forecast. Splits the text in two, which sometimes isn't enough (proof below).

![screen](https://i.imgur.com/CXAI2i5.jpg)

