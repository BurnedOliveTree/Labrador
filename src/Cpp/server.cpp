#include "lib/SocketUDP.h"
#include "lib/SocketTCP.h"
#include "lib/Server.h"
#include <iostream>
#include <vector>
#include "lib/Exit.h"
#include <thread>
#include <pthread.h>

void listener(Server* serv){
    std::vector<char> vecmsg;
    std::string msg;
    while (true){
        try{
            vecmsg  = serv->Receive();
            msg = std::string(vecmsg.begin(), vecmsg.end());
        } catch (const std::exception& e){
        std::cout << e.what() << std::endl;
        }
        std::cout << "Received message: " << msg << std::endl;
    }
}

int main(int argc, char* argv[])
{
    std::string ip = "127.0.0.1";
    int port = 2137;
    if(argc > 2){
        ip = argv[1];
        port = atoi(argv[2]);
    }
    SocketInterface* sockint;
    Server* serv; 
    try{
        // sockint = new SocketUDP(ip, port, true);
        sockint = new SocketTCP(ip, port, true);
        serv = new Server(sockint);
    } catch (const std::exception& e){
        std::cout << e.what() << std::endl;
    }

    Exit e;
    std::thread listenerth(listener, serv);
    std::thread exitth(&Exit::exit, &e);

   exitth.join();
   listenerth.detach();
}

