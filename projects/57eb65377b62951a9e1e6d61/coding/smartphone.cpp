#include<stdio.h>
#include<algorithm>
using namespace std;

int main()
{
    long n;
    long long max = 0,sum; 
    scanf("%ld",&n);
    long long *budget = new long long[n];
    for(long i = 0;i<n;++i)
        scanf("%lld",&budget[i]);
    sort(budget,budget+n);
    for(long i = 0;i<n;++i)
    {
        sum = budget[i]*(n-i);
        if(max<sum)
            max = sum;
    }
    printf("%lld",max);
    return 0;
}
