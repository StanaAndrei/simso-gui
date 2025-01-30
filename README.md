# simso-gui

Graphical user interface of SimSo: https://github.com/MaximeCheramy/simso

## Contributions

<em> This in linked to these [contributions](https://github.com/StanaAndrei/simso#contributions) from backend. </em> <br>

Added a button which opens a dialog where you customize the new task type you will create in tasks tab.<br>
It includes: naming it, choosing its fields and defining it's behaviour by injecting custom python code in its execute method.<br>
The newly created task persists by default(they are saved as json files in the current directory and you can load them).<br>
Also added the posibility to use all existing fields of a task.<br>

Added a dropdown menu with which you can select the heurisitc you want to use with a P_EDF or P_RM schedulers in the scheduler tab at runtime.<br>
You can choose from: decreasing_worst_fit, decreasing_best_fit, decreasing_next_fit, decreasing_first_fit, first_fit, next_fit, worst_fit, best_fit <br>

Added the posibility to generate random sets of the newly created task types.

## Examples
