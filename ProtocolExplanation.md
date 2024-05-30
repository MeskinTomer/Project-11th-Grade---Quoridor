# Protocol Explanation
A simple protocol designed to send and receive messages from a client to a server and vice versa. Each message is made  
of a command, which represents the intended action, and the content needed to be sent in order for the action or  
the response.

# Protocol Diagram
Diagram of how the protocol shapes the message in order to be sent:  

Command Length + End Mark + Command + Payload Length + End Mark + Payload  

Command Length: The length needed in order to receive the command - the length of the command  
Command: The command itself  
Payload Length: The length needed in order to receive the payload - the length of the payload  
Payload: The payload itself  
End Mark: A simple char used to alert when the process of receiving the length of the command/payload needs to be stopped  