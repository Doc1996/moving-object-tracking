# Tracking of Moving Objects by the Visual Servoing System

<br>

<p align="justify">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;This project makes use of a computer vision system for object localization and tracking, which consists of a camera, a Raspberry Pi control unit and a servomotor. Video record captured by the camera is processed and in the real-time reproduced on the computer screen. Computer is connected with the control unit used for driving the servomotor which starts the camera and directs it in the real-time to the specified object. The algorithms for object localization and tracking are implemented in the programming language Python, along with the open-source library OpenCV. The resulting evaluation of the algorithms is based on the set of various moving objects.</p>

<br>


## Project workflow

<br>

<b>Step 1.</b>&nbsp;&nbsp;Designing the visual servoing system
<br>
<p align="center"><img src="images%20for%20GitHub/web%20camera.jpg" width="110px">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<img src="images%20for%20GitHub/servo%20motor.jpg" width="90px"></p>
<p align="center"><img src="images%20for%20GitHub/Raspberry%20Pi%203.jpg" width="240px"></p>
<br>

<b>Step 2.</b>&nbsp;&nbsp;Implementing the color tracking algorithm
<br>
<p align="center"><img src="images%20for%20GitHub/color%20tracking.jpg" width="600px"></p>
<br>

<b>Step 3.</b>&nbsp;&nbsp;Implementing the backprojection algorithm
<br>
<p align="center"><img src="images%20for%20GitHub/backprojection.jpg" width="600px"></p>
<br>

<b>Step 4.</b>&nbsp;&nbsp;Implementing the absolute difference algorithm
<br>
<p align="center"><img src="images%20for%20GitHub/absolute%20difference.jpg" width="600px"></p>
<br>

<b>Step 5.</b>&nbsp;&nbsp;Implementing the optical flow algorithm 
<br>
<p align="center"><img src="images%20for%20GitHub/optical%20flow.jpg" width="600px"></p>
<br>

<b>Step 6.</b>&nbsp;&nbsp;Analyzing the results for different algorithms
<br>
<br>


## Run the project on Windows

<br>

<b>Step 1.</b>&nbsp;&nbsp;Clone the repository:
<pre>
cd %HOMEPATH%

git clone https://github.com/Doc1996/moving-object-tracking
</pre>
<br>

<b>Step 2.</b>&nbsp;&nbsp;Create the virtual environment and install dependencies:
<pre>
cd %HOMEPATH%\moving-object-tracking

python -m pip install --upgrade pip
python -m pip install --user virtualenv

python -m venv python-virtual-environment
.\python-virtual-environment\Scripts\activate

.\WINDOWS_INSTALLING_PACKAGES.bat
</pre>
<br>

<b>Step 3.</b>&nbsp;&nbsp;Modify the changeable variables in <i>MOT_constants.py</i>
<br>
<br>

<b>Step 4.</b>&nbsp;&nbsp;Run the program:
<pre>
cd %HOMEPATH%\moving-object-tracking

.\python-virtual-environment\Scripts\activate

.\WINDOWS_OBJECT_LOCALIZATION_APPLICATION.bat
</pre>
<br>


## Run the project on Linux

<br>

<b>Step 1.</b>&nbsp;&nbsp;Clone the repository:
<pre>
cd $HOME

git clone https://github.com/Doc1996/moving-object-tracking
</pre>
<br>

<b>Step 2.</b>&nbsp;&nbsp;Create the virtual environment and install dependencies:
<pre>
cd $HOME/moving-object-tracking

python3 -m pip install --upgrade pip
python3 -m pip install --user virtualenv

python3 -m venv python-virtual-environment
source python-virtual-environment/bin/activate

source LINUX_INSTALLING_PACKAGES.sh
</pre>
<br>

<b>Step 3.</b>&nbsp;&nbsp;Modify the changeable variables in <i>MOT_constants.py</i>
<br>
<br>

<b>Step 4.</b>&nbsp;&nbsp;Run the program:
<pre>
cd $HOME/moving-object-tracking

source python-virtual-environment/bin/activate

source LINUX_OBJECT_LOCALIZATION_APPLICATION.sh
</pre>
<br>