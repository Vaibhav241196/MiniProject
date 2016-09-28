#include<stdio.h>
#include<cmath>

using namespace std;
long long store[10000];
long long max_dollar(long long a)
{

    if(a<10000)
        if(store[a]!=-1)
            return store[a];
    else 
    {
        long long temp1,temp2,temp3,max;
        temp1 = max_dollar(floor(a/2));
        temp2 = max_dollar(floor(a/3));
        temp3 = max_dollar(floor(a/4));
        if(temp1<floor(a/2))
            temp1 = floor(a/2);
        if(temp2<floor(a/3))
            temp2 = floor(a/3);
        if(temp3<floor(a/4))
            temp3 = floor(a/4);
        if(a>temp1+temp2+temp3)
            max = a;
        else
            max = temp1+temp2+temp3;
        if(a<=10000)
        {
            store[a] = max;
            //printf("%lld\t",store[a]);
        }        
        return max;
    }
}
int main()
{
    int i=0,t;
    //scanf("%d",&t);
    //t = 3  ;
    long long input,*output;
    output  = new long long[10];
    for(long long i=0;i < 10000;++i)
        store[i] = -1;
    store[0] = 0;
    store[1] = 1;
    store[2] = 2;
    store[3] = 3;
    store[4] = 4;
    store[5] = 5;
    store[6] = 6;
    store[7] = 7;
    store[8] = 8;
    store[9] = 9;
    store[10] = 10;
    while(scanf("%lld",&input))   ///////////////////////////////////////////////////////////////////////////
    {
        output[t] = max_dollar(input);
        ++t;
    }                                               
    for(int i=0;i<t;++i)
        printf("%lld\n",output[i]);
    return 0;
}
