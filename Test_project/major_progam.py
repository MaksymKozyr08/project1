from input_data import first_number
from testing import factorial
import time

def culculation(n:int,k:int)->int:
    if k<0 or k>n:
        return 0
    return factorial(n)//(factorial(k)*factorial(n-k))

def benchmark(n:int,k:int):
    start_point=time.perf_counter()
    result=culculation(n,k)
    end_point=time.perf_counter()
    final_time=(end_point-start_point)*1000
    return result, final_time
if __name__=="__main__":
    n,k=first_number()
    print(benchmark(n,k))