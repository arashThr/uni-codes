module Types where

import qualified Modules.Helper as Aux

insertionSort :: [Int] -> [Int]
insertionSort = Aux.insSort

-- Type signature ?
--s r = show Aux.baseCircle

data Person = Person
    { name :: String
    , age :: Int
    } deriving (Show, Read, Eq)

arash :: Person
arash = Person { name ="Arash", age = 23 }

data Day = Monday | Tuesday | Wednesday | Thursday | Friday | Saturday | Sunday
    deriving (Eq, Show, Read, Ord, Enum, Bounded)

infixr 5 :-:
data List a = Empty | a :-: (List a) deriving (Show, Read, Eq, Ord)

infixr 5 .++
(.++) :: List a -> List a -> List a
Empty .++ ys = ys
((:-:) x xs) .++ ys = x :-: (xs .++ ys)


data Tree a = EmptyTree | Node a (Tree a) (Tree a) deriving (Read, Eq)

singleton :: a -> Tree a  
singleton x = Node x EmptyTree EmptyTree  

treeInsert :: (Ord a) => a -> Tree a -> Tree a  
treeInsert x EmptyTree = singleton x
treeInsert x (Node a left right)   
    | x == a = Node x left right  
    | x < a  = Node a (treeInsert x left) right  
    | x > a  = Node a left (treeInsert x right)  
treeInsert _ _ = EmptyTree

treeElem :: (Ord a ) => a -> Tree a -> Bool
treeElem _ EmptyTree = False
treeElem x (Node a left right)
    | x == a = True
    | x < a = treeElem x left
    | x > a = treeElem x right
treeElem _ _ = False

class MyEq a where
    (==:) :: a -> a -> Bool
    (/=:) :: a -> a -> Bool
    x ==: y = not ( x /=: y )
    x /=: y = not ( x ==: y )

instance Show a => Show (Tree a) where
    show (EmptyTree) = "Empty"
    show (Node x _ _) = "Root is " ++ show x


class YesNo a where
    yesNo :: a -> Bool

instance Functor Tree where
    fmap _ EmptyTree = EmptyTree
    fmap f (Node x l r) = Node (f x) (fmap f l) (fmap f r)

