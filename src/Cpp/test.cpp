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

    std::vector<char> vec(msg.begin(), msg.end());
    Utils::printVector(vec);
    std::vector<char> es_vec = Utils::addHeader(es,vec);
    Utils::printVector(es_vec);
    auto [es1, vec1] = Utils::divideHeader(4, es_vec);
    Utils::printVector(es1);
    Utils::printVector(vec1);

    std::vector<char> ser_es = Utils::serializeStruct<Utils::ex_struct>(es);
    Utils::printVector(ser_es);

    auto es_des = Utils::deserializeStruct<Utils::ex_struct>(ser_es);
    std::cout << ntohs(es_des.a) << std::endl;




}