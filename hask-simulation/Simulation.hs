module Simulation (
) where

import qualified Data.Map as Mapper

type Id = Int
newtype Node a = Node { getNode :: a }
newtype Nodes a = Nodes { getNodes :: Mapper.Map Id (Node a) }
newtype Edges = Edges { getEdges :: Mapper.Map Id [Id] }

newtype Network a = Network { getNetwork :: (Nodes a, Edges) }

nearestNeighbors :: Network a -> Id -> [Id]
nearestNeighbors = undefined

updateNode :: Network a -> Id -> Node a -> Network a
updateNode = undefined
