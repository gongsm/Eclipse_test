package Algorithm_test;

public class insertsort_test {
	
	/*堆排序*/
	/*假定左右树都是最大堆*/
	public static void max_heapfy(int[] arr,int i,int length){
		int largest = i;
		int l = 2*i;
		int r = 2*i+1;
		if((l<=length)&&(arr[l-1]>arr[i-1])){
			largest = l;
		}
		if((r<=length)&&(arr[r-1]>arr[largest-1])){
			largest = r;
		}
		if(largest!=i){
			int temp = arr[i-1];
			arr[i-1] = arr[largest-1];
			arr[largest-1] = temp;
			max_heapfy(arr,largest,length);
		}
	}
	/*创建最大堆*/
	public static void build_max_heap(int[] arr){
		int i;
		for(i = arr.length/2;i>0;i--){
			max_heapfy(arr,i,arr.length);
		}
	}
	/*堆排序*/
	public static int[] heapsort(int[] arr){
		int temp;
		int length = arr.length;
		build_max_heap(arr);
		for(int i = arr.length;i>1;i--){
			temp = arr[0];
			arr[0] = arr[i-1];
			arr[i-1] = temp;
			length--;
			max_heapfy(arr, 1, length);
		}
		return arr;
	}
	/*合并排序*/
	public static void merge(int[] arr,int p,int q,int r){
		int[] L;
		int[] R;
		int i,j;
		int n1 = q-p+1;
		int n2 = r-q;
		L = new int[n1+1];
		R = new int[n2+1];
		for( i=0;i<n1;i++)
			L[i] = arr[p+i-1];
		for( j=0;j<n2;j++)
			R[j] = arr[q+j];
		L[n1] = 65536;
		R[n2] = 65536;
		i = 0;
		j = 0;
		for(int k = p-1;k<r;k++){
			if(L[i]<=R[j]){
				arr[k] = L[i];
				i = i+1;
			}
			else{
				arr[k] = R[j];
				j = j+1;
			}
		}
	}
	public static int[] mergesort(int[] arr,int p,int r){
		int q;
		if(p<r){
			q = (p+r)/2;
			mergesort(arr,p,q);
			mergesort(arr,q+1,r);
			merge(arr,p,q,r);
		}
		return arr;
	}
	/*选择排序*/
	public static int[] selectsort(int[] arr){
		int min;
		int temp;
		if(arr==null||arr.length<2)
			return arr;
		for(int i = 0;i<arr.length-1;i++){
			temp = arr[i];
			min = i;
			for(int j = i+1;j<arr.length;j++){
				if(arr[j]<arr[min]){
					min = j;
				}
			}
			arr[i] = arr[min];
			arr[min] = temp;
		}
		return arr;
	}
	/*插入排序*/
	public static int[] insertsort(int[] arr){
		int temp;
		int i,j;
		if(arr==null||arr.length<2)
			return arr;
		for( i=1;i<arr.length;i++){
			temp = arr[i];
			for(j=i;j>0;j--){
				if(arr[j]<arr[j-1]){
					arr[j] = arr[j-1];
				}
				else
					break;
			}
			arr[j] = temp;
			
		}
		return arr;
	}
	/*冒泡排序*/
    public static int[] bubblesort(int[] arr){
    	int i,j;
    	int temp;
    	if(arr==null||arr.length<2)
			return arr;
    	for(i=0;i<arr.length;i++){
    		for(j=arr.length-1;j>i;j--){
    			if(arr[j]<arr[j-1]){
    				temp = arr[j];
    				arr[j] = arr[j-1];
    				arr[j-1] =temp;
    			}
    		}
    	}
    	return arr;
    }
    
    /*快速排序*/
    public static int[] quicksort(int[] arr,int left, int right){
    	
    	if(left >= right){
    		return arr;
    	}
    	int key = arr[left];
    	int start = left;
    	int end = right;
    	
    	while(start<end){
    		while(end>start&&arr[end]>=key){
    			end--;
    		}
    		arr[start] = arr[end];
    		while(end>start&&arr[start]<=key){
    			start++;
    		}
    		arr[end] = arr[start];
    	}
    	
    	arr[start] = key;
    	quicksort(arr,left,start-1);
    	quicksort(arr,start+1,right);
    	
    	return arr;
    }
    /*计数排序 非比较排序 线性时间排序*/
    public static int[] numsort(int[] arr,int k){
    	int[] result = new int[arr.length];
    	int[] num = new int[k+1];
    	int i;
    	for( i = 0;i<=k;i++){
    		num[i] = 0;
    	}
    	
    	for( i = 0;i<arr.length;i++){
    		num[arr[i]] +=1;
    	}
    	
    	for( i = 1;i<=k;i++){
    		num[i] = num[i]+num[i-1];
    	}
    	
    	for(i = arr.length-1;i>=0;i--){
    		result[num[arr[i]]-1] = arr[i]; 
    		num[arr[i]]--;
    	}
    	
    	
    	return result;
    }
    /*基数  排序，非比较排序*/
    public static int[] bucketSort(int[] arr,int bitnum){
    	
    	int[][] temp = new int[10][arr.length];
    	int[] order = new int[10];
    	int n = 1;
    	int m = 0;
    	int k = 0;
    	while(m < bitnum){
	    	for(int i =0;i<arr.length;i++){
	    		int lsd = (arr[i]/n)%10;
	    		temp[lsd][order[lsd]] = arr[i];
	    		order[lsd]++;
	    	}
	    	for(int i=0;i<10;i++){
	    		if(order[i]!=0){
	    			for(int j = 0;j < order[i];j++){
	    				arr[k] = temp[i][j];
	    				k++;
	    			}
	    		}
	    		order[i] = 0;
	    	}
	    	k = 0;
	    	n *=10;
	    	m++;
    	}
    	
    	
    	return arr;
    }
    
    
    /*最佳方法。。寻找第二小的数*/
	public static void main(String[] args) {
		// TODO Auto-generated method stub
          int[] arr = {1,4,2,3,15,25,6,4,10};
          int[] result;
         // result = mergesort(arr,1,9);
      //    result = bubblesort(arr);
       //   result = heapsort(arr);
        //  result = quicksort(arr,0,arr.length-1);
       //   result = numsort(arr,25);
          result = bucketSort(arr,2);
          System.out.println(result[1]);
	}

}
