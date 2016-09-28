#include<stdio.h>
#include<algorithm>
using namespace std;

int main()
{
    long long n,k,total=0;
    scanf("%lld%lld",&n,&k);
    long long *gums = new long long[n];
    for(long long i=0;i<n;++i)
    {
        scanf("%lld",&gums[i]);
        if(gums[i]>=k)
        {
            --i;
            --n;
        }
    }
   sort(gums,gums+n);
   long long j,low,high,mid,x;
    for(long long i=0;i<n;++i)
    {
        j = 0;
        low=i+1,high=n;
        x = k-1-gums[i];
	    while(low<=high)
	    {
		    mid=(low+high)/2;
		    if((gums[mid]<=x)&&(gums[mid+1]>x||mid==n-1))
		    {
			    j = mid;
			    break;
		    }
		    else if(x>gums[mid])
			    low=mid+1;
		    else if(x<gums[mid])
			    high=mid-1;
	    }
        if(j!=0)
            total = total+j-i;
        else 
            break;
    }
    printf("%lld",total);
    
    return 0; 
}
