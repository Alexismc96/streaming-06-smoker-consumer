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


def offer_rabbitmq_admin_site(show_offer):
    """Offer to open the RabbitMQ Admin website"""
    if show_offer == True: 
        ans = input("Would you like to monitor RabbitMQ queues? y or n ")
        print()
        if ans.lower() == "y":
            webbrowser.open_new("http://localhost:15672/#/queues")
            print()
    else:
        webbrowser.open_new("http://localhost:15672/#/queues")

def send_message(host: str):
    """
    Creates and sends a message to the queue each execution.
    This process runs and finishes.

    Parameters:
        host (str): the host name or IP address of the RabbitMQ server
        queue(str): name of the queue
        file: the csv file

    """
    file_name = 'smoker-temps.csv'
    queue_1 = '01-smoker'
    queue_2 = '02-foodA'
    queue_3 = '03-foodB'

    # read file and define header row to get data 
    with open(file_name, 'r') as file:
        reader = csv.reader(file, delimiter = ',')
        header = next(reader)

        try:
            # create a blocking connection to the RabbitMQ server
            conn = pika.BlockingConnection(pika.ConnectionParameters(host))
            # use the connection to create a communication channel
            ch = conn.channel()
            #delete queues
            ch.queue_delete(queue_1)
            ch.queue_delete(queue_2)
            ch.queue_delete(queue_3)
            # use the channel to declare a durable queue
            # a durable queue will survive a RabbitMQ server restart
            # and help ensure messages are processed in order
            # messages will not be deleted until the consumer acknowledges
            ch.queue_declare(queue= queue_1, durable=True)
            ch.queue_declare(queue= queue_2, durable=True)
            ch.queue_declare(queue= queue_3, durable=True)
        
            #set column variables
            for row in reader:
                Time,Channel1,Channel2,Channel3 = row

                try:
                    #convert string to float
                    smoker_temp = float(Channel1)
                    #create message from data
                    smoker_string = f"{Time},{smoker_temp}"
                    #binary message
                    smoker_string = smoker_string.encode()
                    # use the channel to publish a message to the queue
                    # every message passes through an exchange
                    ch.basic_publish(exchange="", routing_key=queue_1,body=smoker_string)
                    print(f"[x] Sent {smoker_string}")
                except ValueError:
                    pass

                try:
                #convert string to float
                    foodA_temp = float(Channel2)
                    #create message from data
                    foodA_string = f"{Time},{foodA_temp}"
                    #binary message
                    foodA_string = foodA_string.encode()
                    # use the channel to publish a message to the queue
                    # every message passes through an exchange
                    ch.basic_publish(exchange="", routing_key=queue_2, body=foodA_string)
                    print(f"[x] Sent {foodA_string}")
                except ValueError:
                    pass
    
                try:
                    #convert string to float
                    foodB_temp = float(Channel3)
                    #create message from data
                    foodB_string = f"{Time},{foodB_temp}"
                    #binary message
                    foodB_string = foodB_string.encode()
                    # use the channel to publish a message to the queue
                    # every message passes through an exchange
                    ch.basic_publish(exchange="", routing_key=queue_3, body=foodB_string)
                    print(f"[x] Sent {foodB_string}")
                except ValueError:
                    pass

                
                #set time
                time.sleep(30)
   
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
    offer_rabbitmq_admin_site(True)
    send_message('localhost')