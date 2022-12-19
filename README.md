# Indicators of Player Fatigue
![indicatorsofplayerfatigueheader](https://user-images.githubusercontent.com/77839398/208069033-e1e0f0f2-be2e-4247-ad3f-7616db6eb188.png)
> Indicators of Player Fatigue is a project by KTH master students that aims to provide IMU-based alternatives to [PlayerLoad](https://support.catapultsports.com/hc/en-us/articles/360000510795-What-is-Player-Load-).
> The classes in this project provides ways to do both real-time tracking of parameters via streamed data and to analyse a set of data.
> The parameters have been tuned for use with a Suunto Movesense device attached to a players torso, but can be changed to fit your own hardware!
> The data we can measure is:

* Jump Intensity
* Posture Pitch

# Table of Contents
* [Jump Intensity](https://github.com/AntonBrinkCodes/Indicators-of-fatigue-in-football#jump-intensity)
* [Posture Pitch](https://github.com/AntonBrinkCodes/Indicators-of-fatigue-in-football#posture-pitch) 
* [Team Members](https://github.com/AntonBrinkCodes/Indicators-of-fatigue-in-football#team-members)


## Are you tired?
#### Not me
###### actually maybe a little!
If you were a football player, and you were tired from all those goals and headers. Probably you can't jump as intensly, and you're running with an increased tilt in your torso[^increased_trunk_and_other]<sup>,</sup>[^increased_trunk_effects]! AJ AJ AJ! 

## Jump Intensity
Jump Intensity is calculated using a combination of flight time and flight frequency. A jump is identified using a weighted sum of acceleration data. It's fun!

## Posture Pitch
<p align = "center">
    <img src="https://user-images.githubusercontent.com/77839398/207816735-72cb9726-2ea1-4f70-a782-3faa92263c2d.gif">
</p>
Posture Pitch is the rotation around the x-axis, estimated using gyro and acceleration data. It is calculated using sensor fusion and a Madgwick filter. We've created a class PosturePitch, which heavily uses the python native Madgwick filter created by AHRS. See the Python Script "ExamplePP.py" on how our PosturePitch class can be used to perform real time tracking of Posture Pitch! 
<p align="center">
  <img src="https://user-images.githubusercontent.com/77839398/208050666-c73aca96-0b99-4d21-a266-d104644e3829.png">
</p>


# TODO
- [ ] Fixa shortpaper
- [x] Lägg upp kod för Jump Intensity
- [ ] Lägg upp kod som slår ihop Posture Pitch var 10:e minut.
- [ ] fixa en snygg readme
- [ ] Fixa övriga exempelfiler
- [x] Drick kaffe

## Team Members
* Anton Brink:  [antonbri@kth.se](mailto:antonbri@kth.se) , [My github](https://github.com/AntonBrinkCodes/)
* Alice Engvall:  [Email me](@kth.se) , [My github](https://github.com//)
* Elsa Netz:  [Email me](@kth.se) , [My github](https://github.com//)
* Tim Wimmelbacher: [Email me](@kth.se) , [My github](https://github.com//)


<!--Referencerna måste ha fyra mellanslag, inte använda tab :) :) :) -->


[^increased_trunk_and_other]:
    [Winter, S., Gordon, S., & Watt, K. (2017). Effects of fatigue on kinematics and kinetics during overground running: a systematic review. The Journal of sports medicine and physical fitness, 57(6), 887–899.](https://doi.org/10.23736/S0022-4707.16.06339-8)
  

[^increased_trunk_effects]:
    [Warrener, A., Tamai, R., & Lieberman, D. E. (2021, August). The effect of trunk flexion angle on lower limb mechanics during running. Human Movement Science, 78,  102817.](https://doi.org/10.1016/j.humov.2021.102817)


