# Key Fob Direction Finder

 

This project developed a RF direction finding system to demonstrate key fob frequency identification and angle within 180 degrees.
 

## Table of Contents

 

- [Overview](#overview)  

- [Hardware Components](#hardware-components)  

- [Software and Dependencies](#software-and-dependencies)  

- [Usage](#usage)  

- [Results and Demonstration](#results-and-demonstration)  



## Overview

 

To explore course concepts, specifically RF communication in a real world application. Determining direction using radio waves involves precise timing to determine distance, and triangulation between 2 or more antennas to determine the direction of an incoming signal.
This project will develop an RF direction finding system and demonstrate key fob frequency identification and location within 90deg. Key fob direction finding will help people locate their lost keys. This project will encapsulate multiple concepts discussed during lecture. For example, antennas, wireless transmission, wireless receiving, etc. We will use a central computer and an array of antennas for receiving a signal from a key fob. The computer will also have a way to visualize direction after processing incoming data.
This project is meant to be a bit simplified compared to a robust solution. We will be using off the shelf RTL-SDRs. We will assume the antenna array and key fob have line of sight to one another, and we will not be striving for extreme accuracy. This project will determine general direction rather than a hyper specific direction. Additionally this implementation would not work as a key fob finder in practice since it requires someone to press a button on the fob to send out the signal. 

 

## Hardware Components

 

- RTL-SDR (2x)
- 315MHz omnidirectional antenna (2x)
- USB multiport hub
- Laptop
- Raspberry pi
- Touchscreen display



## Software and Dependencies

 

- GNU Radio
- Radioconda
- MatPlotLib
