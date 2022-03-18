# Optimization-with-Python-docplex-Part2

This repository is an extension of the https://github.com/suresh-abeyweera/Optimization-with-Python-docplex. I have been writing on Medium on operation research and this is the second exercise of it.If you haven’t read it I would suggest first get an idea by reading below.

## Usage of the App

This is the main interface where you do the production planning.
![image](https://user-images.githubusercontent.com/61721484/158932889-a0c2e71e-5911-4f7d-9afe-66ada13ccbfe.png)

From the sidebar change the input values. And click solve button. If the OR problem finds and integer optimal solution it would notify and show the time taken to solve the model.
 
![image](https://user-images.githubusercontent.com/61721484/158933333-e98b58c6-e221-4a20-b961-c8abba0bf266.png)

If the model unable to find optimal solution it will notify as below.

![image](https://user-images.githubusercontent.com/61721484/158933551-cf643b4f-b7b0-46ba-87ec-2bcde574f34b.png)

When ever optimum solution is obtained it will show the results (Each car types production amounts/profits/ profit composition) as below.

![image](https://user-images.githubusercontent.com/61721484/158933809-b4076549-0ce7-4148-8423-3fc831c7f532.png)

From below graphs the planner can get an idea on the remaining capacity and it might help on capacity management effectively.

![image](https://user-images.githubusercontent.com/61721484/158934029-cc2a312b-9a2d-4b3c-850a-e3918320a6d9.png)

## Check the functionality from your computer

Download the repositary.I have created seperate Anaconda environment with python 3.7 as below.

![image](https://user-images.githubusercontent.com/61721484/158934300-266841c2-fc1a-4905-a484-9b94df8fe902.png)

Activate the environment and go into the relevant directory and install streamlit as below. In addition to that install docplex, cplex ,seaborn and matplotlib in similar way.
![image](https://user-images.githubusercontent.com/61721484/158934630-6c717445-2311-4bed-b745-a2359824f12d.png)

Run the python file as below.And it will open up a new tab in the browser with the web application.
![image](https://user-images.githubusercontent.com/61721484/158934903-a3963651-cf64-4f6c-ba4c-c4cdbcd3b81d.png)






