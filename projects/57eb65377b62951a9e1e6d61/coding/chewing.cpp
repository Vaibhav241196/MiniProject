#include<stdio.h>
#include<algorithm>
using namespace std;

//long long binarysearch(long long[],long long,long long,long long);
//long long quicksort(long long[],long long[],long long,long long,long long);
int main()
{
    long long n,k,total=0;
    scanf("%lld%lld",&n,&k);
  //  long long *record = new long long[n];           ----------------------------
    long long *gums = new long long[n];
    for(long long i=0;i<n;++i)
    {
        scanf("%lld",&gums[i]);
        if(gums[i]>=k)
        {
            --i;
            --n;
        }
    //    record[i]=0;                -----------------------------------------------
    }
    sort(gums,gums+n);
   // record[0] = 1;
   // total = quicksort(gums,record,0,n,k);
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
        //j = binarysearch(gums,i+1,n,k-1-gums[i]);
       // for(long long j=n-1;j>=i+1;--j)
        //{
            if(j!=0)
                total = total+j-i;
            else 
                break;
            //else
              //  ++total;
        //}
    }
    printf("%lld",total);
    
    return 0; 
}

/*long long binarysearch(long long a[],long long initial,long long n,long long x)
{
	long long low=initial,high=n,mid;
	while(low<=high)
	{
		mid=(low+high)/2;
		if((a[mid]<=x)&&(a[mid+1]>x||mid==n-1))
		{
			j = mid;
			break;
		}
		else if(x>a[mid])
			low=mid+1;
		else if(x<a[mid])
			high=mid-1;
	}
}*/

/*long long quicksort(long long t[],long long r[],long long a,long long b,long long k)		//the matrix is from a to b-1
{
    static long long total = 0;
	long long i=a+1,j=b-1;
	r[a] = 1;
	//struct student temp;
		while(t[a]+t[i]<k&&i<=b-1)
		    {			//equal to sign should come
			    ++i;
			    ++total;
			}
	    if(a+1<b&&r[a+1]!=1)
		    quicksort(t,r,a+1,b,k);
		if(i<b&&r[i]!=1)
		    quicksort(t,r,i,b,k);
		return total;
		//quicksort(t,j+1,b);
}*/
