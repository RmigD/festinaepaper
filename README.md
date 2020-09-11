# festinaepaper
## Just another e-Paper weather station in a watch case.

### Instructions (probably incomplete)
- Check the paths under /examples/getweathertoscreen.sh
- Check the paths under /examples/get_weather.py
- Install the fonts that you can find under "pic" if you wish to see them in the code. They will still render in the screen if not installed.
- Provide your api key for darksky in file /examples/getweathertoscreen.sh
- Provide your api key for Pushbullet in file /examples/get_weather.py - I believe this needs fixing, but it has worked in the past. It's configured to send an alert if strong wind is coming.
- Cross fingers
- Run /examples/getweathertoscreen.sh

notes:
- pushbullet code is a mess. There are leftovers of two different ways of triggering the push. I forgot which one is the most finished.
- Some icons aren't coherent with the rest (different thickness), even if they are the same font.
- Last two lines give the extended forecast. For some reason, the two last letters in each line aren't rendered. I don't think it's the code, but it might be the code. Or the way the screen renders the text. I don't know and I don't care.


![screen](https://i.imgur.com/CXAI2i5.jpg)
