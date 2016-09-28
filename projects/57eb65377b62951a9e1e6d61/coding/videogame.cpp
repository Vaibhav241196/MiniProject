#include<stdio.h>
using namespace std;

int main()
{
    long n,h,*stack;
    int dp,stack_no=0,loaded = 0;
    scanf("%ld%ld",&n,&h);
    stack = new long[n];
    for(long i = 0;i<n;++i)
        scanf("%ld",&stack[i]);
    do{
    scanf("%d",&dp);
    switch(dp)
    {
        case 1: if(stack_no!=0)
                --stack_no;
                break;
        case 2: if(stack_no!=n-1)
                ++stack_no;
                break;
        case 3: if(loaded==0&&stack[stack_no]!=0)
                {
                    loaded = 1;
                    --stack[stack_no];
                }
                break;
        case 4: if(loaded==1&&stack[stack_no]!=h)
                {
                    loaded = 0;
                    ++stack[stack_no];
                }
                break;
        default:break;
    }
    
    }while(dp!=0);
    for(long i = 0;i<n;++i)
        printf("%ld ",stack[i]);
    return 0;
}
