#include "lib/SocketUDP.h"
#include "lib/SocketTCP.h"
#include "lib/Host.h"
#include "lib/Utils.h"
#include <iostream>
#include <vector>
#include "lib/Exit.h"
#include <thread>
#include <pthread.h>

void listener(Host* serv){
    std::variant<std::string, SimpleStruct> msg;
    while (true){
        try{
            msg = serv->Receive();
        } catch (const std::exception& e){
            std::cout << e.what() << std::endl;
        }

        if(std::get_if<std::string>(&msg)){ 
            std::cout << "Received string message: " << std::get<std::string>(msg) << std::endl;
        }
        if(std::get_if<SimpleStruct>(&msg)){ 
            std::cout << "Received struct message: " << std::get<SimpleStruct>(msg).a << " " << unsigned(std::get<SimpleStruct>(msg).b) << " " << unsigned(std::get<SimpleStruct>(msg).c) << std::endl;
        }
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
    Host* serv; 
    try{
        sockint = new SocketUDP(ip, port, true);
        // sockint = new SocketTCP(ip, port, true);
        serv = new Host(sockint);
    } catch (const std::exception& e){
        std::cout << e.what() << std::endl;
    }

    Exit e;
    std::thread listenerth(listener, serv);
    std::thread exitth(&Exit::exit, &e);

    exitth.join();
    listenerth.detach();

    delete serv;
    delete sockint;

}

