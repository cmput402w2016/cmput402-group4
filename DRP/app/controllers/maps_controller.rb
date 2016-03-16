class MapsController < ApplicationController
  def index
    @segment = Segment.all
    @hash = Gmaps4rails.build_markers(@segment) do |segment, marker|
      marker.lat segment.startlat
      marker.lng segment.startlong
    end
  end
end
