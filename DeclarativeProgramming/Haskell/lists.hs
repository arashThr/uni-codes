sumOfSq :: Int -> Int
sumOfSq n = sum [x*x | x<-[1..n]]

myRep :: Int -> a -> [a]
myRep n a = [a | x <- [1..n]]

pyths :: Int -> [(Int, Int, Int)]
pyths n = [(x, y, z) | x<-[1..n], y<-[x..n], z<-[y..n], x^2 + y^2 == z^2]

factors n = [x | x<-[1..n], mod n x == 0]
perfects n = [x | x<-[1..n], (sum (factors x)) - x == x]

nested = [ [(x,y)|y<-[4,5,6]] | x<-[1,2,3]]

myFind x xs = [v | (k, v) <- xs, k == x]
pos n ns = myFind n (zip ns [0..l])
    where l = length ns - 1

scalarProd :: [Int] -> [Int] -> Int
scalarProd a b = sum [m * n | (m, n)<-zip a b]

evens :: [a] -> [a]
evens [] = []
evens (x:xs) = x : odds xs
odds :: [a] -> [a]
odds [] = []
odds (_:xs) = evens xs

expon _ 0 = 1
expon 1 _ = 1
expon n p = n * expon n (p - 1)

myAnd [] = True
myAnd (True:xs) = and xs
myAnd (False:_) = False

myConc [] = []
myConc (x:xs) = x ++ myConc xs

myRecRep 0 _ = []
myRecRep n x = x : myRecRep (n-1) x

-- It can be made more percise
nth 1 (x:xs) = x
nth n (_:xs) = nth (n-1) xs

myElem a xs = or [x==a | x<-xs]


halve ns = (take n ns, drop n ns)
    where n = div (length ns) 2

merge [] l = l
merge l [] = l
merge (k:l) (m:n)
    | k <= m = k : merge l (m:n)
    | k > m = m : merge (k:l) n

mSort [] = []
mSort [x] = [x]
mSort l = merge (mSort f) (mSort s)
    where (f, s) = halve l

rightLen = foldr (\ _ n -> n + 1) 0
leftLen = foldl (\ n _ -> n + 1) 0

head' :: [Int] -> [Char]
head' [] = error "Error !"
head' xs@(x:_) = "Head of " ++ show xs ++ " is " ++ show x

checkBmi :: Int -> Int -> String
checkBmi w h
    | res > 10 = "You die"
    | res > 5 = "You may die"
    | otherwise = "You live"
    where res = w * h

calcBmis :: (RealFloat a) => [(a, a)] -> [a]  
calcBmis xs = [bmi w h | (w, h) <- xs]  
    where bmi weight height = weight / height ^ (2::Int)

