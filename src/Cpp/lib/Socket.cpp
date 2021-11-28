#include "Socket.h"

Socket::Socket(std::string ip, int port, bool is_serv,bool is_UDP){
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
        if(is_UDP){
            sock = socket( AF_INET, SOCK_DGRAM, 0 );
        } else {
            sock = socket( AF_INET, SOCK_STREAM, 0 );
        }
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

void Socket::Send(std::vector<char> msg){
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
    int bsize = msg.size();
    std::cout << "SEND ROZMIAR: "<< bsize << std::endl;
    std::cout << "SEND 1stCHar: "<< msg.data()[0] << std::endl;
    if(sendto(sock, msg.data(), bsize, 0, dst, dst_len ) < 0)
        {
            throw std::runtime_error("Couldn't send message to server");
        }
}

std::vector<char> Socket::Receive(){
    std::vector<char> buffer(max_buffer_size);
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
    int result = recvfrom(sock, buffer.data(), buffer.size(), 0, dst, dst_len);
    if( result < 0 )
        {   
            throw std::runtime_error("Couldn't receive message from server");
        }
    buffer.resize(result);
    std::cout << "RECEIVE 1stCHar: "<< buffer.data()[0] << std::endl;
    return buffer;
}
