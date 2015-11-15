#############################
Generating integer partitions
#############################

:date: 2014-05-26
:tags: Python, Integer partitions, combinatorial generation 
:category: Combinatorics 
:summary: Efficient algorithms to generate all integer partitions in Python. 

The purpose of this page is to give an informal presentation of the algorithms
I developed for my PhD thesis and subsequently turned into a research 
`article <http://arxiv.org/abs/0909.2331>`__. The basic gist of this
work is that we can generate integer partitions much more effectively if we
encode them as ascending compositions rather than the conventional descending
compositions. As it turns out, it's much easier to generate ascending
compositions.  I'm not going to argue this point here, since it's something
I've done at great length elsewhere; instead, lets just take a quick overview
of the main points and look at the algorithms themselves.

**********************
Ascending Compositions
**********************

An integer partition
is an expressions of a positive integer *n* as an 
unordered collection of positive integers. 
A composition, on the other hand, is an expresssion 
of *n* as an ordered collection of positive integers.
For example, 
1 + 1 + 2, 
1 + 2 + 1
and
2 + 1 + 1
all represent the same partition 
of 4. Then, ascending compositions are the compositions
of *n* where all the parts are in ascending (non decreasing) order. For example,
the ascending compositions of 5 are::

    1 +  1 +  1 +  1 +  1 
    1 +  1 +  1 +  2 
    1 +  1 +  3 
    1 +  2 +  2 
    1 +  4 
    2 +  3 
    5 

Generating ascending compositions is one way to get partitions: generating
all ascending compositions is equivalent to generating all partitions. For 
historical reasons, partition generation algorithms have nearly all generated
descending compositions (see 
`Wikipedia <http://en.wikipedia.org/wiki/Partition_(number_theory)>`__), 
`Mathworld <http://mathworld.wolfram.com/Partition.html>`__ or 
Ruskey's `Combinatorial Object Server
<http://theory.cs.uvic.ca/inf/nump/NumPartition.html>`__, for example).
There are definite advantages, however, to working with ascending compositions 
instead.

*******************
Iterative Algorithm
*******************

Lets take a look at one algorithm to generate all ascending compositions.
This algorithm is written as a Python 
`generator <http://www.python.org/dev/peps/pep-0255>`__, which is a very neat way 
of writing combinatorial generation algorithms.

.. code-block:: python

    def rule_asc(n):
        a = [0 for i in range(n + 1)]
        k = 1
        a[1] = n
        while k != 0:
            x = a[k - 1] + 1
            y = a[k] - 1
            k -= 1
            while x <= y:
                a[k] = x
                y -= x
                k += 1
            a[k] = x + y
            yield a[:k + 1]

Although this algorithm is very simple, it is also very efficient. It is
*Constant Amortised Time*, which means that the average computation per
partition that is output is constant. 

We can prove this fairly easily by looking at the two while loops and the
variable k. Since the **yield** operator is called exactly once for every
iteration of the outer while loop, we know that it must iterate exactly *p(n)*
times (where *p(n)* is the number of partitions of *n* --- see `Mathworld
<http://mathworld.wolfram.com/PartitionFunctionP.html>`__ or Sloane's sequence
`A000041 <http://www.research.att.com/~njas/sequences/A000041>`__ for details
and properties).  Therefore, we know that there must be exactly *p(n)*
decrement operations on k (since k -= 1 is only called in the outer loop).
Then, since k is initially 1 and the algorithm terminates when k is 0, we know
that there must be *p(n)* - 1 increment operations on k.  Since the only
increment operations occur in the inner while loop, we know that this loop gets
executed exactly *p(n)* - 1 times, and so the total running time of the
algorithm is proportional to *p(n)*. In other words, the algorithm is
constant amortised time.


************************
Most Efficient Algorithm 
************************

If it's speed you're looking for, here is the most efficient known algorithm to
generate all partitions of a positive integer. 

.. code-block:: python

    def accel_asc(n):
        a = [0 for i in range(n + 1)]
        k = 1
        y = n - 1
        while k != 0:
            x = a[k - 1] + 1
            k -= 1
            while 2 * x <= y:
                a[k] = x
                y -= x
                k += 1
            l = k + 1
            while x <= y:
                a[k] = x
                a[l] = y
                yield a[:k + 2]
                x += 1
                y -= 1
            a[k] = x + y
            y = x + y - 1
            yield a[:k + 1]


This algorithm is a modification of the algorithm above. It gains its
extra efficiency by using some structure of the set of ascending compositions
to make many transitions more efficient. Consider, for example, the following
of partitions of 10::

    1 + 1 + 2 + 6 
    1 + 1 + 3 + 5
    1 + 1 + 4 + 4 

These transitions can be made very efficiently, since all we need to do is to 
add one to the second last part and subtract one from the last part. The algorithm
above takes advantage of this, and it is the most efficient known algorithm to
generate partitions (it has been 
`shown <http://arxiv.org/abs/0909.2331>`__
to be more efficient than Zoghbi and Stojmenovic's excellent 
`ZS1 algorithm <http://www.site.uottawa.ca/~ivan/F49-int-part.pdf>`__.)


