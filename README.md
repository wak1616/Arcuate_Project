# De Rojas AI Calc

## Setup
1. Create virtual environment:   ```bash
   python -m venv venv   ```

2. Activate virtual environment:   ```bash
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate   ```

3. Install dependencies:   ```bash
   pip install -r requirements.txt   ```


## Video Demo:  <[URL HERE](https://youtu.be/1WNCb5swXqw?si=JPf2HWXy9DbEge_M)>

## Description:

*What are arcuate incisions and why are they used?*

Arcuate incisions of the cornea (aka arcuate keratotomies) are used in ophthalmic surgery to treat astigmatism during cataract surgery and lens exchange procedures. They are a powerful tool, but there is little medical consensus on how to best employ them, how to create them (via a femtosecond laser? manual blades?), or how to fine-tune them for specific levels of astigmatism and/or patient biometrics or demographics. The author Joaquin De Rojas, MD (creator of this website) has extensive experience in employing these "arcuate keratotomies" to improve visual outcomes for his patients.

There have been multiple published models or "nomograms" to help guide surgeons in how to best make these incisions (i.e. how long do you make them? how far from the center of the cornea? How deep?) There are links to these prior published models under "Links" in the navigation bar at the top of the webage.

*The purpose of De Rojas AI Calc:*

The current nomogram (De Rojas AI Calc) has been developed using insights gained from the Donnenfeld limbal relaxing incisions nomogram as well as the Wortz-Gupta Calculator (both available online) with the purpose of creating a more user-friendly and, eventually, more accurate nomogram. The hope of the author is to create future versions of this nomogram that will leverage even larger data sets and artificial intelligence (on the back-end Python side) to further increase its accuracy.

*Design and development decisions (programming)*

The goal of this project was to create a simple web-based application that would allow users to input case/patient data (patient ID, age, left vs right eye, astigmatism amount, location of steep axis in standard ophthalmic/optometric notation) for analysis via an HTML form.  This data would then be transferred to a Javascript program which would parse out the data, convert to JSON, and transfer to the back-end / Python via @app.route('/calculate', methods=['POST']) once the submit button is clicked. The function "calculate" would then use patient eye, laterality, astigmatism, and steep axis data to produce arcuate incision recommendations that could then be sent back to the javascript script.  The script will then use the CANVAS element to render an image of an eye that would show how the arcuate incision(s) would appear on the eye.  It would also transfer the specifcations of the arcuate incision(s) as text/strings so that they can be displayed on the web page adjacent to the canvas element. Finally, the website should include some additional information in the "About" link and some links to external website with related content.  

*A few notes on calcuations for arcuate incisions (Python code)*

After initial data values are obtained, the steep axis and orientation of the cornea is determined.  This usually corresponds to the inital steep axis but may change to 180 degrees away if original steep axis is near main incision.  Next, the location of the steep axis (if needed) is taken as is or flipped to 180 degrees away depending if it is near the main corneal incision (used for cataract surgery) so it doesn't interfere with it.  A series of rules are then used to determine if 1 or 2 arcuates will be used, and furthermore, how long/big they should be.  These rules are based on personal experience of the author with similar cases, as well as on recommendations of prior nomograms (Wortz Gupta and Donnenfeld, see "Links" on website).  Age adjustments are also made to the arucate incision lengths , with decreases to total lengths made for older patients (since the cornea is stiffer and more sensitive to keratotomies at older age).  Similarly, if the axes of arcuates are at or near 180 degrees (aka against-the-rule astigmatism) then itthis requires and INCREASE in incision length by a few degrees because this axis of the cornea requires MORE treatment.

The next part of the code deals with creating the starting and ending points for the arcuate incisions in a format that CANVAS' ctx.arc will be able to draw correctly on a canvas image of an eye.  The center point (in pixels) and radius of the circle from which the arcuates will be based was determined using the chosen eye photo (that happens to be a photo of my wife's eye) in Photoshop.  In order for javascript to be able to draw the arcuates, the starting and ending points of the arcuates would need to be determined (arc1start, arc1end, arc2start, arc2end) based on the lengths and locations of the arcuate incisions previously determined in the function "calculate" within app.py.  aLSO, the data points of the arcuates would need to be changed to the proper orientation for javascript Canvas.ctx use: from counter-clockwise to clockwise notation of degrees around as circle and from degrees to radians notation. The function "arcuatesstartend" (imported into appy.py from helpers.py) was created for this purpose.


*Functions of javascript/front-end portion:*
1. When the user hits "submit" on the webpage, collect data from the html form (user input)
2. transfer data to Python (/calculate) to determine arcuate incision recommendations
3. Wait for data to be analyzed, then bring in the results from "/calculate" back into Javascript. 
4. Render a canvas element on the webpage and draw on it to create the arcaute incisions in the correct orientation and magnitude
5. Describe, in text form, the arcuate incisions and publishes this description on the wepbage adjacent to the CANVAS drawing.
6. Reload the form and clear the canvas and output when the website is reloaded.  Update the canvas and output in text form if any of the input entries have been changed and the user has clicked submit again.


*Nomogram assumptions (surgical)*

The nomogram does make a series of assumptions that are as follows:
1. The ALLY® Adaptive Cataract Treatment System (LensAR, Inc)is used to make laser arcuate incisions.
2. Arcuate incisions are made at 80% depth.
3. Arcuate incisions are made at at 4.5mm radius (9.0mm diamter) from the visual center.
4. All acruate incisions were opened at the time of surgery with a BSS irrigation cannula.
5. Low levels of astigmatism (.3) will not be treated and higher levels of astigmatism (greater than 1.25) will not be treated with arcuates (because the author believes such high amounts of astigmatism are best treated with toric lenses instead).
6. "Against-the-rule astigmatism" (i.e. steep axis at 180 degrees) will be treated more aggressively that "With-the-rule astigmatism" (i.e. steep axis at 090 degrees).
7. Surgically induced astigmatism (SIA) from the surgeon's main incision will be minimal.

*Disclaimer for use*

IN IT'S CURRENT FORM, THIS WEBSITE/NOMOGRAM IS ONLY INTENDED FOR EDUCATIONAL PURPOSES AND TO FULFULL A FINAL PROJECT REQUIREMENT FOR A COMPUTER SCIENCE COURSE: CS50's Introduction to Computer Science . IT IS NOT INTENDED FOR REAL PATIENT USE OR TO GUIDE SURGICAL CORRECTION OF ASTIGMATISM IN HUMANS OR ANIMALS.