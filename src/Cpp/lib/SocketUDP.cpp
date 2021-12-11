#include "SocketUDP.h"

SocketUDP::SocketUDP(std::string ip, int port,  bool is_serv): sock(ip,port,is_serv,true){
    if(is_serv){
        sock.Bind();
    }
}

void SocketUDP::Send(std::vector<char> msg){
    std::vector<std::vector<char>> splited_msg = Utils::splitData(msg, MAX_PACKET_SIZE-4);
    for(uint8_t i = 0; i < splited_msg.size(); i++)
    {
        Utils::printVector(splited_msg[i]);
        PacketHeader ph = {htons(splited_msg[i].size()), static_cast<uint8_t>(splited_msg.size()), i};
        sock.Send(Utils::addHeader(Utils::serializeStruct<PacketHeader>(ph), splited_msg[i]));
    }
}

std::vector<char> SocketUDP::Receive(){
    std::vector<char> result, rec;
    PacketHeader ph;
    do{
        rec = sock.Receive();
        Utils::printVector(rec);
        auto [hd, msg] = Utils::divideHeader(4, rec);
        //Utils::printVector(msg);
        ph = Utils::deserializeStruct<PacketHeader>(hd);
        result.insert(result.end(), msg.begin(), msg.end());
    } while(ph.max_packet-ph.curr_packet>1);
    return result;
}

std::vector<std::vector<char>> SocketUDP::Poll(){
    std::vector<std::vector<char>> result;
    result.push_back(Receive());
    return result;
}



