class MapsController < ApplicationController

  def index
  end


  def calcroute
    #empty the global nodes array every time a new request is sent.
    nodes = []
    # Get paths from ajax call
    paths = JSON.parse(params[:paths])
    i = 0
    # For each set of nodes, find corresponding nodes in the db, create a list for each path.
    while i < paths.length
      nodearray = []
      unless paths[i] == nil
        j = 0
        while j < paths[i].length
          # Get a geohash for each node
          geohash = GeoHash.encode(paths[i][j]['lat'], paths[i][j]['lng'])
          # Get the closest matching node
          k = 3
          trimmedhash = geohash[0,geohash.length-k]
          while Node.where("geohash LIKE (?)", "#{trimmedhash}%").empty?
            k+=1
            trimmedhash = geohash[0,geohash.length-k]
          end
          #add the node to the array of nodes for this path
          nodearray.append(osmNode = Node.where("geohash LIKE (?)", "#{trimmedhash}%").first)
          j+=1
        end
        # add each array of nodes to the 2d array
        nodes.append(nodearray)
      end
      i+=1
    end

    # Need to find the ways associated with each node and sum the cost up.
    routeCost = []
    for i in 0..2
      routeCost[i] = 0
      unless nodes[i].nil?
        nodes[i].each do |node|
          way = Way.where("nodes @> ARRAY[?]::bigint[]", node.id)
          unless way.empty?
            unless way.first.cost.nil?
              routeCost[i] += way.first.cost
            end
          end
        end
      end
    end
    #The index of the best route
    #gon.bestroute = routeCost.index(routeCost.min)
    best = routeCost.index(routeCost.min)
    render :json => {:routeindex => best}
  end

end
