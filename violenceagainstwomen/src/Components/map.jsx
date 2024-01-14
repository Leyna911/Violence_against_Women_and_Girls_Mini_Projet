import React, { useState,useEffect } from "react"
import { ComposableMap, Geographies, Geography, Marker, Annotation, ZoomableGroup } from "react-simple-maps"
import axios from "axios"

const markers = [
    {
        markerOffset: -10,
        name: "Algiers",
        coordinates:[3.0588, 36.7538]
    }
]

const geoUrl = "https://raw.githubusercontent.com/Leyna911/Violence_against_Women_and_Girls_Mini_Projet/master/violenceagainstwomen/src/Assets/custom.geo.json"



const Map = () => {
    const [content, setContent] = useState("");
    const [hoveredCountry, setHoveredCountry] =useState("")

    const [selectedCountry, setSelectedCountry] = useState(null)
    const [frequentItemsets, setFrequentItemsets] = useState([])
    const [support, setSupport] = useState([])
   
   
    

    const handleClickCountry = async (country) => {
      
      try {
        const response = await axios.post('http://127.0.0.1:8000/predict', {
        Country: country,
      });
      
        
        setFrequentItemsets(response.data.frequent_itemsets);
        setSupport(Array.from(response.data.support))
        setSelectedCountry(country)

        
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

  return (
    <div>
    <div className="w-[1000px] border-double border-4 ">
       
       {content && (
        <div className="absolute  p-2 rounded shadow" style={{ top: "20px", left: "20px" }}>
          {content}
        </div>
      )}

        <ComposableMap data-tip="">
            <ZoomableGroup zoom={1}>
                {" "}
                <Geographies geography={geoUrl} >
                    {({ geographies }) =>
                    geographies.map((geo) => (
                        <Geography
                        key={geo.rsmKey}
                        geography={geo}
                        fill="#cccccc"
                        stroke="#808080"
                        onMouseEnter={() => {
                          const countryName = geo.properties.name; 
                          setContent(`${countryName}`);
                          setHoveredCountry(geo.id); 
                        }}
                        onMouseLeave={() => {
                          setContent("");
                          setHoveredCountry(null);
                        }}
                        onClick={()=> handleClickCountry(geo.properties.name)}
                        className={hoveredCountry === geo.id ? "hover:fill-[#E30000] cursor-pointer" : ""}
                       
                      />
                      
                    ))
                    }
                </Geographies>
                {
                    markers.map(({name, coordinates, markerOffset}) => {
                        return(
                            <Marker key={name} coordinates={coordinates}> 
                                <circle r={5} fill="#332929" stroke="#e9e9e9"  strokeWidth={2} className=""/>
                                <text textAnchor="middle" y={markerOffset}  className="fill-[#332929] ">
                                    {name}
                                </text>
                            </Marker>
                        )
                        
                    })
                }
                
            </ZoomableGroup>
            
        </ComposableMap>
        
    </div>
    {frequentItemsets.length > 4 && (
  <div>
    <h2>Frequent Itemsets</h2>
    <ul>
      {frequentItemsets
        .filter((itemset, index) => {
          console.log('Itemset:', itemset);
          console.log('Support:', support[index]);
          return itemset.length > 3 && parseFloat(support[index]) > 0.083;
        })
        .map((itemset, index) => (
          <li key={index}>
            {itemset
              .filter(item => item !== selectedCountry)
              .join(', ')}
            {" - "}
            Support: {support[index]}
          </li>
        ))}
    </ul>
  </div>
)}





    </div>
  )
}

export default Map
