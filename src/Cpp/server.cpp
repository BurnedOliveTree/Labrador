#include "lib/SocketUDP.h"
#include "lib/SocketTCP.h"
#include "lib/Host.h"
#include "lib/Utils.h"
#include <iostream>
#include <vector>
#include "lib/Exit.h"
#include <thread>
#include <pthread.h>
#include <chrono>
#include <thread>


void listener(Host* serv){
    // std::variant<std::string, SimpleStruct> msg;
    std::vector<std::variant<std::string, SimpleStruct>> msg;
    int how_many_msgs = 5;
    while(true){
        try{
            msg = serv->ReceiveAll();
        } catch (const std::exception& e){
            std::cout << e.what() << std::endl;
        }

        // if(std::get_if<std::string>(&msg)){ 
        //     std::cout << "Received string message: " << std::get<std::string>(msg) << std::endl;
        // }
        // if(std::get_if<SimpleStruct>(&msg)){ 
        //     std::cout << "Received struct message: " << std::get<SimpleStruct>(msg).a << " " << unsigned(std::get<SimpleStruct>(msg).b) << " " << unsigned(std::get<SimpleStruct>(msg).c) << std::endl;
        // }
        for(int i = 0 ; i != msg.size(); i++){   
            if(std::get_if<std::string>(&(msg[i]))){ 
                std::cout << "Received string message: " << std::get<std::string>(msg[i]) << std::endl;
            }
            if(std::get_if<SimpleStruct>(&(msg[i]))){ 
                std::cout << "Received struct message: " << std::get<SimpleStruct>(msg[i]).a << " " << unsigned(std::get<SimpleStruct>(msg[i]).b) << " " << unsigned(std::get<SimpleStruct>(msg[i]).c) << std::endl;
            }
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
        // sockint = new SocketUDP(ip, port, true);
        sockint = new SocketTCP(ip, port, true);
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

