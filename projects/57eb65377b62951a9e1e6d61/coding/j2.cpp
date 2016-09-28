#include<iostream>
#include<cmath>
using namespace std;

void myfunc(long);
long nextprime(long);
int main()
{
    int t;  
    cin>>t;
    long *num = new long[t];
    for(int i = 0;i<t;++i)
        cin>>num[i];
    for(int i = 0;i<t;++i)
        myfunc(num[i]);
    
}
void myfunc(long a)
{

    cout<<"Hello\n   ";
    int factor[1000];
    for(int  i =0;i<1000;++i)
        factor[i] = 1;
    int j = 0;
    long i = 2;
    while(a!=1)
    {
        if(a%i==0)
        {
            a = a/i;
            factor[j] = i;
            ++j;
        }
        else
        {
            i = nextprime(i);
            cout<<i;
        }
    }
    for(int  i =0;i<1000;++i)
        if(factor[i]!=1)
            cout<<"\t"<<factor[i];
    return;
}

long nextprime(long old)
{
    for(long i = old+1;i<288+old;++i)
    {
        for(long j = 2;j<=i;++j)
        {
            if(i%j==0)
                break;
            if(j==i)
                return i;
        }
    }
    return 0;
}
