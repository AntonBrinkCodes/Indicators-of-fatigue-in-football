![indicatorsofplayerfatigueheader](https://user-images.githubusercontent.com/77839398/208069033-e1e0f0f2-be2e-4247-ad3f-7616db6eb188.png)
> Indicators of Player Fatigue is a project by KTH master students that aims to provide IMU-based alternatives to [PlayerLoad](https://support.catapultsports.com/hc/en-us/articles/360000510795-What-is-Player-Load-).
> The classes in this project provides ways to do both real-time tracking of parameters via streamed data.
> The parameters have been tuned for use with a Suunto Movesense device attached to a players torso, but can be changed to fit your own hardware!
> The data we can measure is:

* Jump Intensity
* Posture Pitch

# Table of Contents
* [Team Members](https://github.com/AntonBrinkCodes/Indicators-of-fatigue-in-football#team-members)
# Indicators-of-fatigue-in-football


## Are you tired?
#### Not me
###### actually maybe a little!

## Jump Intensity
Jump Intensity is calculated using a combination of flight time and flight frequency. A jump is identified using a weighted sum of acceleration data. It's fun!

## Posture Pitch
Posture Pitch is the rotation around the x-axis, estimated using gyro and acceleration data. It is calculated using sensor fusion and a Madgwick filter. We've created a class PosturePitch, which heavily uses the Madgwick filter used by AHRS. See the file "ExamplePP.py" on how this class can be used to perform real time tracking of Posture Pitch!

![Screenshot 2022-12-16 085553](https://user-images.githubusercontent.com/77839398/208050666-c73aca96-0b99-4d21-a266-d104644e3829.png)


# TODO
- [ ] Fixa shortpaper
- [ ] Lägg upp kod för Jump Intensity
- [ ] Lägg upp kod som slår ihop Posture Pitch var 10:e minut.
- [ ] fixa en snygg readme
- [ ] Fixa övriga exempelfiler
- [x] Drick kaffe

## Team Members
* Anton Brink:  [Email me](antonbri@kth.se) , [My github](https://github.com/AntonBrinkCodes/)
* Alice Engvall:  [Email me](@kth.se) , [My github](https://github.com//)
* Elsa Netz:  [Email me](@kth.se) , [My github](https://github.com//)
* Tim Wimmelbacher: [Email me](@kth.se) , [My github](https://github.com//)

[PosturePitch_validationMovie](https://user-images.githubusercontent.com/77839398/207816735-72cb9726-2ea1-4f70-a782-3faa92263c2d.gif)
