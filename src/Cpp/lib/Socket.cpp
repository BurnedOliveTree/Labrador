#include "Socket.h"

Socket::Socket(std::string ip, int port, bool is_serv){
    is_server = is_serv;
    socket_ip = ip;
    socket_port = port;
    if (std::string(ip).find('.') != std::string::npos){
        desc_4.sin_family = AF_INET;
        desc_4.sin_port = htons( socket_port );

        if( inet_pton( AF_INET, socket_ip.c_str(), & desc_4.sin_addr ) <= 0 )
        {
            throw std::runtime_error("inet_pton didn't convert IP");
        }
    
        sock = socket( AF_INET, SOCK_DGRAM, 0 );
        if(( sock ) < 0 )
        {
            throw std::runtime_error("Socket wasn't created");
        }
        socket_len = sizeof(desc_4);
        self_addr = (struct sockaddr*) &desc_4;
    }
    else {
        desc_6.sin6_family = AF_INET6;
        desc_6.sin6_port = htons( socket_port );

        if( inet_pton( AF_INET6, socket_ip.c_str(), & desc_6.sin6_addr ) <= 0 )
        {
            throw std::runtime_error("inet_pton didn't convert IP");
        }
    
        sock = socket( AF_INET6, SOCK_DGRAM, 0 );
        if(( sock ) < 0 )
        {
            throw std::runtime_error("Socket wasn't created");
        }
        socket_len = sizeof(desc_6);
        self_addr = (struct sockaddr*) &desc_6;
    }
}

Socket::~Socket(){
    shutdown(sock, SHUT_RDWR);
}

void Socket::Bind(){
    if( bind( sock, self_addr, socket_len ) < 0 )
    {
        throw std::runtime_error("Socket wasn't binded");
    }
}

void Socket::Send(const char* buff, int bsize){
    buffer = new char[4+bsize];
    int16_t buff_len = bsize;
    int8_t max_packet = 0, num_packet = 0;
    memcpy(buffer, &buff_len, 2);
    memcpy(buffer+2, &max_packet, 1);
    memcpy(buffer+3, &num_packet, 1);
    memcpy(buffer+4, buff, bsize);

    struct sockaddr* dst;
    socklen_t dst_len;
    if(is_server){
        dst = &dest_addr;
        dst_len = dest_len;
    }
    else{
        dst = self_addr;
        dst_len = socket_len;
    }
    if(sendto(sock, (void *) buff, buff_len+4, 0, dst, dst_len ) < 0 )
        {
            throw std::runtime_error("Couldn't send message to server");
        }
    delete[] buffer;
}

std::string Socket::Receive(){
    buffer = new char[4082];
    struct sockaddr* dst;
    socklen_t* dst_len;
    if(is_server){
        dst = &dest_addr;
        dst_len = &dest_len;
    }
    else{
        dst = self_addr;
        dst_len = &socket_len;
    }
    if( recvfrom(sock, buffer, sizeof(buffer), 0, dst, dst_len) < 0 )
        {   
            throw std::runtime_error("Couldn't receive message from server");
        }
    std::string msg(buffer);
    std::cout << "Received message: " << msg << std::endl;
    delete[] buffer;
    return msg;
}
