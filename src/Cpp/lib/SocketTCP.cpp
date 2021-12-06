#include "SocketTCP.h"

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
    for(int i = 0; i < splited_msg.size(); i++)
    {
        Utils::printVector(splited_msg[i]);
        PacketHeader ph = {htons(splited_msg[i].size()), splited_msg.size(), i};
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
