# simso-gui

Graphical user interface of SimSo: https://github.com/MaximeCheramy/simso

## Contributions

<em> This in linked to these [contributions](https://github.com/StanaAndrei/simso#contributions) from backend. </em> <br>

Added a button which opens a dialog where you customize the new task type you will create in tasks tab.<br>
It includes: naming it, choosing its fields and defining it's behaviour by injecting custom python code in its execute method.<br>
The newly created task persists by default(they are saved as json files in the current directory and you can load them).<br>
Also added the posibility to use all existing fields of a task.<br>
Added the posibility to generate random sets of the newly created task types.
![image](https://github.com/user-attachments/assets/9e37dc07-ff37-40bc-8184-497e132242b6)
![image](https://github.com/user-attachments/assets/2eb47e66-ef96-4919-8adf-442fa01375f5)



Added a dropdown menu with which you can select the heurisitc you want to use with a P_EDF or P_RM schedulers in the scheduler tab at runtime.<br>
You can choose from: decreasing_worst_fit, decreasing_best_fit, decreasing_next_fit, decreasing_first_fit, first_fit, next_fit, worst_fit, best_fit <br>
![image](https://github.com/user-attachments/assets/97e28d4d-6e16-4889-b7ff-258bcce8a1e9)

To setup this locally follow [this tutorial](https://youtu.be/lAYVX5WsBMU).
