main :: IO()
main = print "Hello world !"
mysum [] = 0
mysum (x:xs) = x + mysum xs

double x = x + x
{-
 - Quadruple
 -}
quad x = double ( double x )

-- Factorial function
factorial n = product [1..n]
avg n = div (sum n) (length n)

a = b + c where
    b = 1
    c = 2
c = a * 2

n = a `div` length xs where
    a = 10
    xs = [1,2,3,4]

myInit [x] = []
myInit (x:xs) = [x] ++ myInit xs

myAdd :: Int -> Int -> Int
myAdd x y = x + y

myInc = myAdd 1

second xs = head ( tail xs )
pair :: Int -> Int -> (Int, Int)
pair x y = (x, y)
swap (a, b) = (b, a)
--isPalindrom :: Integral a => [a] -> Bool
isPalindrom xs = reverse xs == xs
twice f x = f ( f x )

incPat :: Int -> Int -> Int
incPat 1 1 = 1 + 1
incPat a b = a + b

halve :: [Int] -> ([Int],[Int])
--halve ns = (ns, ns)
halve ns = (take (f ns) ns, drop (f ns) ns)
    where f ns = div (length ns) 2

tailPat [] = []
tailPat (x:xs) = xs

tailCond xs = if length xs == 0
    then []
    else tail xs

tailGaurd xs
    | xs == [] = []
    | otherwise = tail xs

conj1 a b = if and [a == b, a == True]
    then True
    else False

conj2 a b = if a
    then b
    else False

mult x y z = x * y *z

factors n = [x | x<-[1..n], mod n x == 0]
isPrime n = factors n == [1, n]
primes n = [x | x <- [1..n], isPrime x]


pairs xs = zip xs (tail xs)
sorted :: Ord a => [a] -> Bool
sorted xs = and [x <= y | (x, y) <- pairs xs]

posPair ns num = [ y | (x, y) <- zip ns [0..l], x == num]
    where l = length ns - 1

