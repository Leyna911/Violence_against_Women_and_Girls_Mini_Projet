import React from "react"
import { ComposableMap, Geographies, Geography } from "react-simple-maps"


const geoUrl ="../Assets/custom.geo.json"

const Map = () => {

  return (
    <ComposableMap>
      <Geographies geography={geoUrl}>
        {({ geographies }) =>
          geographies.map((geo) => (
            <Geography key={geo.rsmKey} geography={geo} />
          ))
        }
      </Geographies>
    </ComposableMap>
  )
}

export default Map
