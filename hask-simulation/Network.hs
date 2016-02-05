module Network (
   Network,
   Nodes,
   Edges,
   updateNode
) where

import qualified Data.Map as Mapper

type Id = Int
newtype Node a = Node { getNode :: a }
newtype Nodes a = Nodes { getNodes :: Mapper.Map Id (Node a) }
newtype Edges = Edges { getEdges :: Mapper.Map Id [Id] }

newtype Network a = Network { getNetwork :: (Nodes a, Edges) }

nearestNeighbors :: Network a -> Id -> Maybe [Id]
nearestNeighbors (Network (Nodes nodes, Edges edges)) id = Mapper.lookup id edges

createNode :: Network a -> Id -> Node a -> Network a
createNode (Network (Nodes nodes, edges)) id node = Network (Nodes $ Mapper.insert id node nodes, edges)

readNode :: Network a -> Id -> Maybe (Node a)
readNode (Network (Nodes nodes, _)) id = Mapper.lookup id nodes

updateNode :: Network a -> Id -> Node a -> Network a
updateNode (Network (Nodes nodes, edges)) id node = Network (Nodes $ Mapper.insert id node nodes', edges)
    where nodes' = Mapper.filterWithKey (\k a -> k == id) nodes

deleteNode :: Network a -> Id -> Network a
deleteNode = undefined
