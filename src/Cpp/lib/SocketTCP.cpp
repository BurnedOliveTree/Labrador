#include "SocketTCP.h"
#include <fcntl.h>

SocketTCP::SocketTCP(std::string ip, int port,  bool is_serv): sock(ip,port,is_serv,false){
    if(is_serv){
        sock.Bind();
        sock.Listen();
    }
    else{
        sock.Connect();
    }
}

void SocketTCP::Send(std::vector<char> msg){
    std::vector<std::vector<char>> splited_msg = Utils::splitData(msg, MAX_PACKET_SIZE-4);
    for(uint8_t i = 0; i < splited_msg.size(); i++)
    {
        Utils::printVector(splited_msg[i]);
        PacketHeader ph = {htons(splited_msg[i].size()), static_cast<uint8_t>(splited_msg.size()), i};
        sock.Write(Utils::addHeader(Utils::serializeStruct<PacketHeader>(ph), splited_msg[i]));
    }
}


std::vector<char> SocketTCP::Receive(){
    std::vector<char> result, rec;
    PacketHeader ph;
    do{
        std::vector<char> hd = sock.Read(4);
        Utils::printVector(hd);
        ph = Utils::deserializeStruct<PacketHeader>(hd);
        std::vector<char> msg = sock.Read(ntohs(ph.length));
        Utils::printVector(msg);
        result.insert(result.end(), msg.begin(), msg.end());
    } while(ph.max_packet-ph.curr_packet>1);
    return result;
    // PacketHeader ph = Utils::deserializeStruct<PacketHeader>(sock.Read(sizeof(PacketHeader)));
    // return sock.Read(ntohs(ph.length));
}

std::vector<std::vector<char>> SocketTCP::ReceiveAll(){
    std::vector<std::vector<char>> result;
    std::cout << "Waiting on Poll... \n";
    int rc = poll(sock.fds, sock.nfds, sock.timeout);
    if(rc < 0){
        throw std::runtime_error("Poll error");
    }
    if(rc == 0){
        throw std::runtime_error("Timeout error");
    }
    sock.current_size = sock.nfds;
    for (int i = 0; i < sock.current_size; i++)
    {
        if(sock.fds[i].revents == 0){
            continue;
        }
        if(sock.fds[i].revents != POLLIN)
        {
            throw std::runtime_error("One of poll sockets is bad.");
        }
        if (sock.fds[i].fd == sock.sock)
        {
            do
            {
            sock.msgsock = accept(sock.sock, NULL, NULL);
            if (sock.msgsock >= 0)
            {
                std::cout << "  New incoming connection "<< sock.msgsock << std::endl;
                sock.fds[sock.nfds].fd = sock.msgsock;
                sock.fds[sock.nfds].events = POLLIN;
                sock.nfds++;
            }
            } while(sock.msgsock != -1);
        } else {
            if (sock.fds[i].fd >= 0){
                // if(fcntl(sock.fds[i].fd, F_GETFL) & O_NONBLOCK) {
                // // socket is non-blocking
                // }
                std::cout << "Reading from "<< sock.fds[i].fd << std::endl;
                std::vector<char> m = ReceiveSpecific(i);
                result.push_back(m);
            }
        }
    }
    // result.push_back(Receive());
    return result;
}

std::vector<char> SocketTCP::ReceiveSpecific(int which_one){
    std::vector<char> result, rec;
    PacketHeader ph;
    do{
        std::vector<char> hd = sock.Read(4, which_one);
        Utils::printVector(hd);
        ph = Utils::deserializeStruct<PacketHeader>(hd);
        std::vector<char> msg = sock.Read(ntohs(ph.length), which_one);
        Utils::printVector(msg);
        result.insert(result.end(), msg.begin(), msg.end());
    } while(ph.max_packet-ph.curr_packet>1);
    return result;
}