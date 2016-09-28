#include<iostream>
using namespace std;

int main()
{
    long N,Q,input;
    cin>>N>>Q;
    //long *input = new long[N];
    long *output = new long[Q];
    long min=999999999,max=0;
    for(long i = 0;i<N;++i)
    {
        cin>>input;
        if(min>input)
            min = input;
        if(max<input)
            max = input;
    }
    for(long i = 0;i<Q;++i)
        cin>>output[i];
    for(long i = 0;i<Q;++i)
    {
        if(output[i]>=min&&output[i]<=max)
            cout<<"YES"<<endl;
        else
            cout<<"NO"<<endl;    
    }
    
        
    return 0;
}
