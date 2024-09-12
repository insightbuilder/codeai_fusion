#### **Step-by-Step Intuition to Sorting Lists in Python for New Coders**

Knowledge of basic sorting algorithms are crucial for many medium and advanced problems solving. In this article we will review the algorithms in the following format

```flowchart
st=>start: "Read the Python code of algorithm"
op1=>operation: "Extract the intuitions from code"
op2=>operation: "Type out the code & execute"
op3=>operation: "Comment out the code" 
end=>end: "Get ready for next Algorithm"

st->op1->op2->op3->end
```

Key Idea is to **remember the intuitions** of an algorithm and then first code that when solving the problem

#### Four Sorting Algorithms:

- Bubble Sort

- Insertion Sort

- Quick Sort

- Merge Sort

#### Intuitions & Implementation of Bubble Sort:

1) Loops over the entire list twice
   
   ```python
   def bubble_sort(in_list: List[int]):
       # print(in_list)
       # get length of list
       n = len(in_list)
       # use i to loop over the list till end
       for idx in range(n):
           # use j to loop over and leave last element
           for jdx in range(n - i - 1):
   ```

2) 2nd loop leaves the last element, from where the actual sorting / bubbling starts to occur

3) swap the element if next element is smaller than current
   
   ```python
    # code indentations are not maintained here
    # check if adjacent value is bigger than curr value
    if in_list[j] > in_list[j + 1]:
    # swap them
       in_list[j], in_list[j + 1] = in_list[j + 1], in_list[j]
    
    return in_list
   ```

###### Notes on Bubble sort:

- Easiest sort to understand & visualise the flow of changes that occurs

- Inefficient when it comes to space and time complexity, as many tasks are repeated
