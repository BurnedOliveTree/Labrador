#include "Client.h"

Client::Client(char* ip, int port){
    server_ip = ip;
    server_port = port;

    server.sin_family = AF_INET;
    server.sin_port = htons( server_port );

    if( inet_pton( AF_INET, server_ip, & server.sin_addr ) <= 0 )
    {
        throw "inet_pton didn't convert IP";
    }
   
    client_socket = socket( AF_INET, SOCK_DGRAM, 0 );
    if(( client_socket ) < 0 )
    {
        throw "Socket wasn't created";
    }
    client_len = sizeof(server);
}

Client::~Client(){
    shutdown(client_socket, SHUT_RDWR);
}

void Client::Send(std::string msg){
    strncpy( buffer, msg.c_str(), sizeof(buffer));
    if(sendto(client_socket, buffer, strlen(buffer), 0, (struct sockaddr*) &server, client_len ) < 0 )
        {
            throw "Couldn't send message to server";
        }
}

std::string Client::Receive(){
    memset(buffer, 0, sizeof(buffer));
    if( recvfrom(client_socket, buffer, sizeof(buffer), 0, (struct sockaddr*) &server, &client_len ) < 0 )
        {
            throw "Couldn't receive message from server";
        }
    std::string msg(buffer);
    std::cout << "Received message of length " << msg.length() << std::endl;
    return msg;
}