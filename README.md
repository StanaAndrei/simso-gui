# simso-gui

Graphical user interface of [SimSo](https://github.com/MaximeCheramy/simso)

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


## Examples:

###  Decreasing 1st fit
<img width="1043" height="577" alt="ss_decr_1st_fit" src="https://github.com/user-attachments/assets/a631fdb9-3555-42dd-8a72-3d6cac2b0f23" />

### Decreasing best fit
<img width="1072" height="704" alt="ss_decr_best_fit" src="https://github.com/user-attachments/assets/de8f46aa-e789-4e76-85f8-ad42f28a93aa" />

### Worst fit
<img width="1051" height="588" alt="ss_worst_fit" src="https://github.com/user-attachments/assets/57e084eb-8c9f-429f-83f3-c316703b668e" />
<img width="1055" height="590" alt="ss_worst_fit2" src="https://github.com/user-attachments/assets/3c3f9006-9599-4876-a859-2b766234b470" />

### Multi-proc WF EDF
<img width="1078" height="593" alt="ss_multiproc_WF_EDF-WD" src="https://github.com/user-attachments/assets/58b0be6d-2d5d-4016-8024-80c8f5c7d1a7" />

### EDZ
<img width="1732" height="232" alt="ss_multiproc_WF_EDF-WD_settings" src="https://github.com/user-attachments/assets/e2665362-afb9-4c9b-a50f-ac46b1a3491a" />
<img width="1237" height="753" alt="ss_edzl" src="https://github.com/user-attachments/assets/3333c099-3845-49da-ab8b-90fbe146a7f9" />

