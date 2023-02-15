"""
    This program sends a message to a queue on the RabbitMQ server.
    Sending the temperatures from the smart smoker

    Author: Alexis Clinton
    Date: 14 February 2023

"""

import pika
import sys
import webbrowser
import csv
import time


def offer_rabbitmq_admin_site():
    """Offer to open the RabbitMQ Admin website"""
    ans = input("Would you like to monitor RabbitMQ queues? y or n ")
    print()
    if ans.lower() == "y":
        webbrowser.open_new("http://localhost:15672/#/queues")
        print()

def send_message(host: str, queue_name: str, message: str):
    """
    Creates and sends a message to the queue each execution.
    This process runs and finishes.

    Parameters:
        host (str): the host name or IP address of the RabbitMQ server
        queue_name (str): the name of the queue
        message (str): the message to be sent to the queue
    """

    try:
        # create a blocking connection to the RabbitMQ server
        conn = pika.BlockingConnection(pika.ConnectionParameters(host))
        # use the connection to create a communication channel
        ch = conn.channel()
        #delete queue
        ch.queue_delete(queue=queue_name)
        # use the channel to declare a durable queue
        # a durable queue will survive a RabbitMQ server restart
        # and help ensure messages are processed in order
        # messages will not be deleted until the consumer acknowledges
        ch.queue_declare(queue=queue_name, durable=True)
        # use the channel to publish a message to the queue
        # every message passes through an exchange
        ch.basic_publish(exchange="", routing_key=queue_name, body=message)
        # print a message to the console for the user
        print(f" [x] Sent to queue", queue_name, message)
    except pika.exceptions.AMQPConnectionError as e:
        print(f"Error: Connection to RabbitMQ server failed: {e}")
        sys.exit(1)
    finally:
        # close the connection to the server
        conn.close()

# Standard Python idiom to indicate main program entry point
# This allows us to import this module and use its functions
# without executing the code below.
# If this is the program being run, then execute the code below
if __name__ == "__main__":  
    # ask the user if they'd like to open the RabbitMQ Admin site
    show_offer = "False"

    if show_offer == "True":
        offer_rabbitmq_admin_site()
    else:
        webbrowser.open_new("http://localhost:15672/#/queues")
        print()
#Define variables for reading file

    file_name = "smoker-temps.csv"
    input_file = open(file_name, "r")
    reader = csv.reader(input_file, delimiter=",")
    header = next(reader)
    header_list = ["message"]

    #Define messages
    for row in reader:
        Time, Smoker_Temp, Food_A_Temp, Food_B_Temp = row

        message_queue1 = (Time, Smoker_Temp)
        smoker_message = ",".join(message_queue1)
        
        message_queue2 = (Time, Food_A_Temp)
        A_message = ",".join(message_queue2)

        message_queue3 = (Time, Food_B_Temp)
        B_message = ",".join(message_queue3)

        #send messages to queues
        send_message("localhost", "01-smoker", smoker_message)
        send_message("localhost", "02-food-A", A_message)
        send_message("localhost", "03-food-B", B_message)

        #set time
        time.sleep(30)

    input_file.close()

