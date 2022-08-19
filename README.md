# Raspberry Pi Rotary Phone Replica Audio Recorder/Player with Dropbox API integration.

### Background

This is a project made while working at the Chapel Hill Public Library on the [Community History team](https://chapelhillhistory.org/). There has been an ongoing discussion on the team about how to remove barriers to collecting audio from the public for things like oral history projects, exhibit reflections, or crowdsourcing people's experiences on a certain topic. We asked:

1. How can we use as little signage as possible while ensuring that no one from toddlers to elders are excluded?
2. How can we bring together the experiences of listening to others' stories and recording your own?
3. How can we incorporate joy and whimsy?
4. How can we make this budget friendly, easy to use, and easy to replicate?

After a few different prototypes that included [door knobs](https://en.wikipedia.org/wiki/Door_handle), [Arduinos](https://www.arduino.cc/), and a [wooden box](https://en.wikipedia.org/wiki/Box), I finally decided to try using a [Raspberry Pi](https://www.raspberrypi.com/).

Thanks to Casey Connor's [Magic Telephone video](https://www.youtube.com/watch?v=31IkwhLGN3g) and [Python script](http://caseyconnor.org/pub/mtp/mtp), I had a huge head start. The mainRecorder.py script is an adaptation of Casey's.

If you've got some experience working with Raspberry Pis, you can refer to the video from Casey Connor above to give you a general overview of how to set this up. If you have no experience with Raspberry Pi and don't have the time to dive deep into it right now, I will be adding a step-by-step visual guide soon, so either check back in or get in touch.

### Materials
I used two different rotary phone replica models (unfortunately from Amazon), and also tested out some different hardware for the inside of the phone. I am absolutely not an engineer, so I am sure there is still so much that could be done to improve this and would love to hear from anyone that does so. But with the materials listed below, I've got this thing to work pretty much without fail.

(prices as of August 19, 2022)

- (Rotary phone replica)[https://www.amazon.com/Dododuck-Vintage-Seniors-Impaired-Adjustable/dp/B09PVFQPSX/ref=sr_1_3?crid=303LOPTYOFPE8&keywords=retro+phone+dododuck&qid=1659037000&s=electronics&sprefix=retro+phone+dododuck%2Celectronics%2C49&sr=1-3] ($44.90)
- [Raspberry Pi](https://www.raspberrypi.com/products/) Zero 2 W, Zero W, 3 Model A+, 4 Model B ($15.00 - $45.00)
- [MicroSD Card](https://www.amazon.com/gp/product/B07FCMBLV6/?th=1) ($12.73)
- [Raspberry Pi power cord](https://www.adafruit.com/product/1995) ($8.25)
*make sure you're getting the right one, will be either USB-C or MicroUSB*
- [USB Audio Adapter](https://www.adafruit.com/product/1475) ($4.95)
- *if using RPi Zero W or Zero 2 W*: [USB-MicroUSB adapter](https://www.adafruit.com/product/2910?gclid=Cj0KCQjwvLOTBhCJARIsACVldV1MEGmYeWCq1kNNj3xoVaeGX8XVjNDCszNfSYFf9KfpMis_NjXPPNcaAntuEALw_wcB) ($2.95)
- [Three terminal microswithc](https://www.adafruit.com/product/819) ($1.95)
- [Female-Female jumper wires](https://www.adafruit.com/product/794) ($3.95)
- [Tactile button for power button](https://www.adafruit.com/product/367) ($2.50)
- [TRRS Audio Cable Connector](https://www.amazon.com/Ancable-Replacement-Connector-Headphones-Headset/dp/B077XVDQ5R/ref=pd_ybh_a_sccl_67/141-9411584-6111866?pd_rd_w=sp1om&content-id=amzn1.sym.67f8cf21-ade4-4299-b433-69e404eeecf1&pf_rd_p=67f8cf21-ade4-4299-b433-69e404eeecf1&pf_rd_r=1AD6RKS1Q3QN51SMWNA5&pd_rd_wg=FYchA&pd_rd_r=c1a4b326-2466-4e16-88d8-494bf03b3f26&pd_rd_i=B077XVDQ5R&th=1) ($6.99)
*there are lots of options for these, but I recommend just using this exact product so you don't have to spend a bunch of time getting the audio recording and playing to work.

The total price will vary depending on what Raspberry Pi you buy, and also price fluctuations, but the overall cost will end up between $100 and $150. Not bad considering the alternatives. For example, the phone that [This American Life used on this episode](https://www.thisamericanlife.org/672/transcript) costs $250 to rent for a few days and allows almost no customization and certainly doesn't include Dropbox integration. Also, many of these materials come in packs of multiples, so if you're making more than one, some of those costs will be lower per phone.

Ideally, you'll also get materials to solder your wires together. Soldering really isn't too hard. Watch a few YouTube videos, be safe, and you'll be fine. It's worth it to make more sturdy connections between your wires. Those materials:
- [Soldering Iron](https://www.adafruit.com/product/3685) ($19.95)
- [Solder wick](https://www.adafruit.com/product/149) ($3.00)
- [Helping hand](https://www.adafruit.com/product/291) ($6.00)
- [Heat shrink](https://www.adafruit.com/product/344) ($4.95)
- [Wire strippers](https://www.adafruit.com/product/147) ($6.95)

These materials come out to around $40.
