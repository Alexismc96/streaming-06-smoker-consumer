# streaming-05-smart-smoker
> Design and implement a producer for the smart smoker. 

# Name: Alexis Clinton
## Date: 14Feb23


## Before You Begin
1. In GitHub, create a new repo for the smart smoker project- name it streaming-05-smart-smoker
2. Add a README.md 
3. Clone your repo down to your machine. 
4. In VS Code, add a .gitignore (use one from an earlier module), start working on the README.md
5. Add the csv data file to your repo. 
6. Create a file for your bbq producer. 

## Use a Barbeque Smoker
> When running a barbeque smoker, we monitor the temperatures of the smoker and the food to ensure everything turns out tasty. Over long cooks, the following events can happen:
>> 1. The smoker temperature can suddenly decline. 
>> 2. The food temperature doesn't change. At some point, the food will hit a temperature where moisture evaporates. It will stay close to this temperature for an extended period of time while the moisture evaporates. We say the temperature has stalled. 

## Sensors
> We have temperature sensors track temperatures and record them to generate a history of both (a) the smoker and (b) the food over time. These readings are an example of time-series data, and are considered streaming data or data in motion.

## Significant Events
> We want to know if:
>> 1. The smoker temperature decreases by more than 15 degrees F in 2.5 minutes (smoker alert!)
>> 2. Any food temperature changes less than 1 degree F in 10 minutes (food stall!) 

## Smart System 
> We will use Python to:
>> 1. Simulate a streaming series of temperature readings from our smart smoker and two foods.
>> 2. Create a producer to send these temperature readings to RabbitMQ.
>> 3. Create three consumer processes, each one monitoring one of the temperature streams. 
>> 4. Perform calculations to determine if a significant event has occurred.