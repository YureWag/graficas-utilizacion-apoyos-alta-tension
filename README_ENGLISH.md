# High Voltage Tower Utilization Graphs

Visual Python application to calculate and generate utilization graphs for High Voltage towers.

## About this project

This program is a desktop tool designed to facilitate the calculation of High Voltage power lines. Its main objective is to automatically draw the utilization graph of a support (a transmission tower), saving time and avoiding errors. Tool made primarily for the High Voltage Electrical Installations subject at the University of Jaén, taught by Dr. Francisco José Sánchez Sutil, but usable in many contexts.

The user only has to enter the data in the input fields and the program takes care of performing all the corresponding mathematical plotting.

![Program screenshot](interfazPrograma.jpg)

## Main Features

* Interface: Main window divided by sections to enter the data and verify the resulting graph.

* Visual configuration: The X-axis limit (Span L) is set to 500 meters by default, it can be custom modified from the window itself.

* Smart plotting: The program plots the lines of the different load cases (wind, ice, etc.). These lines will be drawn on the graph as long as one (or both) calculated points are within the axis limits.

* Structural Limits: Visually marks the limit of the maximum allowable span and the restriction caused by the insulator string inclination.

* Specific Point: Allows checking an exact point of the tower on the graph by entering its L and N values.

* Equation Assistant: An extra module that mathematically calculates and solves for the variables L and N from equations of the form A*L + B*N + C = 0 (from the different load hypotheses and cases that may arise). When clicking solve, the assistant sends those results to the main window automatically.

* JPG Export: Allows saving the generated graph on the computer.

## Technologies Used

This program was created in Python and uses the following libraries:

* Tkinter
* Matplotlib
* NumPy

## How to install and use the program

1. Download the project

2. Install dependencies: Open the console in the project folder and run the following command to install the necessary libraries:
   ```bash
   pip install -r requirements.txt

3. Start the program: Run the main Python file to open the application:
   ```bash
   python graficas_apoyos.py


#### Developed by Yure Wagemann Valadares Magalhães.