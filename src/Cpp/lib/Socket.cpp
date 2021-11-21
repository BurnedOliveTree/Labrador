#include "Socket.h"

Socket::Socket(char* ip, int port){
    server_ip = ip;
    server_port = port;
    if (std::string(ip).find('.') != std::string::npos){
        std::cout << "Using IPv4" << std::endl; 
        server_4.sin_family = AF_INET;
        server_4.sin_port = htons( server_port );

        if( inet_pton( AF_INET, server_ip, & server_4.sin_addr ) <= 0 )
        {
            std::cout << "inet_pton didn't convert IP";
        }
    
        client_socket = socket( AF_INET, SOCK_DGRAM, 0 );
        if(( client_socket ) < 0 )
        {
            std::cout << "Socket wasn't created";
        }
        server_len = sizeof(server_4);
        server = (struct sockaddr*) &server_4;
    }
    else {
        std::cout << "Using IPv6" << std::endl; 
        server_6.sin6_family = AF_INET6;
        server_6.sin6_port = htons( server_port );

        if( inet_pton( AF_INET6, server_ip, & server_6.sin6_addr ) <= 0 )
        {
            std::cout << "inet_pton didn't convert IP";
        }
    
        client_socket = socket( AF_INET6, SOCK_DGRAM, 0 );
        if(( client_socket ) < 0 )
        {
            std::cout << "Socket wasn't created";
        }
        server_len = sizeof(server_6);
        server = (struct sockaddr*) &server_6;
    }
}

Socket::~Socket(){
    shutdown(client_socket, SHUT_RDWR);
}

void Socket::Bind(){
    if( bind( client_socket, server, server_len ) < 0 )
    {
        std::cout << "Socket wasn't binded";
    }
}

void Socket::Send(std::string msg){
    strncpy( buffer, msg.c_str(), sizeof(buffer));
    if(sendto(client_socket, buffer, strlen(buffer), 0, server, server_len ) < 0 )
        {
            std::cout << "Couldn't send message to server";
        }
}

std::string Socket::Receive(){
    memset(buffer, 0, sizeof(buffer));
    if( recvfrom(client_socket, buffer, sizeof(buffer), 0, server, &server_len ) < 0 )
        {   
            std::cout << "Couldn't receive message from server";
        }
    std::string msg(buffer);
    std::cout << "Received message of length " << msg.length() << std::endl;
    return msg;
}
