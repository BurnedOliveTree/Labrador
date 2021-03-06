#include "lib/Utils.h"

int main(){

    std::string msg = "hello";
    Utils::ex_struct es;
    es.a = htons(300);
    es.b = 3;
    es.c = 2;
    uint8_t test = 8;
    std::cout << "Size of struct: "<< sizeof(es) << " Values: "<< es.a << " " << es.b << " " << es.c << std::endl;
    std::cout << "Uint8_t " << unsigned(test) <<std::endl;

    std::vector<char> vec = Utils::serializeString(msg);
    Utils::printVector(vec);
    std::vector<char> es_vec = Utils::addHeader(es,vec);
    Utils::printVector(es_vec);
    auto [es1, vec1] = Utils::divideHeader(4, es_vec);
    Utils::printVector(es1);
    Utils::printVector(vec1);

    std::vector<char> ser_es = Utils::serializeStruct<Utils::ex_struct>(es);
    Utils::printVector(ser_es);

    Utils::ex_struct es_des = Utils::deserializeStruct<Utils::ex_struct>(ser_es);
    std::cout << ntohs(es_des.a) << std::endl;

    auto zwyciestwo = Utils::deserializeString(vec1);
    std::cout << zwyciestwo << std::endl;

    msg = "ab";//cdefghijklmnopqrstuwyz0";
    std::vector<char> vec2 = Utils::serializeString(msg);
    Utils::printVector(vec2);
    std::vector<std::vector<char>> splited = Utils::splitData(vec2, 4);
    for(std::vector<std::vector<char>>::iterator it = splited.begin(); it!=splited.end(); it++)
    {
        Utils::printVector(*it);
    }
}