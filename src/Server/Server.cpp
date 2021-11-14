#include "Server.h"

Server::Server(char* ip, int port){
    server_ip = ip;
    server_port = port;
    if (std::string(ip).find('.') != std::string::npos){
        std::cout << "Using IPv4" << std::endl; 
        server_4.sin_family = AF_INET;
        server_4.sin_port = htons( server_port );

        if( inet_pton( AF_INET, server_ip, & server_4.sin_addr ) <= 0 )
        {
            throw "inet_pton didn't convert IP";
        }
    
        server_socket = socket( AF_INET, SOCK_DGRAM, 0 );
        if(( server_socket ) < 0 )
        {
            throw "Socket wasn't created";
        }
        server_len = sizeof(server_4);
        server = ( struct sockaddr * ) & server_4;
    }
    else{
        std::cout << "Using IPv6" << std::endl;
        server_6.sin6_family = AF_INET6;
        server_6.sin6_port = htons( server_port );

        if( inet_pton( AF_INET6, server_ip, & server_6.sin6_addr ) <= 0 )
        {
            throw "inet_pton didn't convert IP";
        }
    
        server_socket = socket( AF_INET6, SOCK_DGRAM, 0 );
        if(( server_socket ) < 0 )
        {
            throw "Socket wasn't created";
        }
        server_len = sizeof(server_6);
        server = ( struct sockaddr * ) & server_6;
    }

    if( bind( server_socket, server, server_len ) < 0 )
    {
        throw "Socket wasn't binded";
    }
}

Server::~Server(){
    shutdown(server_socket, SHUT_RDWR);
}

std::string Server::Receive(){
    memset(buffer, 0, sizeof(buffer));
    if( recvfrom(server_socket, buffer, sizeof(buffer), 0, ( struct sockaddr * ) &curr_client, &server_len ) < 0 )
        {
            throw "Couldn't receive message from client";
        }
    std::string msg(buffer);
    std::cout << "Received message of length " << msg.length() << std::endl;
    return msg;
}

void Server::Send(std::string msg){
    strncpy( buffer, msg.c_str(), sizeof(buffer));
    if(sendto(server_socket, buffer, strlen(buffer), 0, ( struct sockaddr * ) &curr_client, server_len ) < 0 )
        {
            throw "Couldn't send message to client";
        }
}

bool Server::CheckQuit(std::string msg){
    if (msg == "QUIT"){
        return true;
    }
    return false;
}

