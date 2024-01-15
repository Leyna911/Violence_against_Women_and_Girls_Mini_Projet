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
    const [lift, setLift] =useState([])
    const [confidence,setConfidence] = useState([])
    
   
    

    const handleClickCountry = async (country) => {
      
      try {
        const response = await axios.post('http://127.0.0.1:8000/predict', {
        Country: country,
      });
      
        
        setFrequentItemsets(response.data.frequent_itemsets);
        setSupport(Array.from(response.data.support))
        setSelectedCountry(country)
        setConfidence(Array.from(response.data.confidence))
        setLift(Array.from(response.data.lift))

        
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
    <div>
    {frequentItemsets.length > 4 && (
  <div>
    <div className="mt-4 p-4 border-[2px] border-[#332929] rounded-md">
      <h2 className="my-4 text-xl font-extrabold dark:text-[#332929] md:text-xl lg:text-2xl w-[]">
        Frequent Itemsets with its respective support, confidence, and lift values.
      </h2>
      <ul className="max-w-md mt-d divide-y">
        {frequentItemsets
          .filter((itemset, index) => {
            return (
              itemset.length > 3 &&
              parseFloat(support[index]) > 0.016 &&
              parseFloat(confidence[index]) > 0.5
            );
          })
          .map((itemset, index) => (
            <li
              key={index}
              className={`pb-3 mb-1 sm:pb-4 ${
                index % 2 === 0 ? 'bg-[#c52b2b]' : 'bg-[#b6b6b6]'
              } rounded p-4`}
            >
              {itemset
                .filter(item => item !== selectedCountry)
                .join(', ')}
              {" - "}
              Support: {support[index]} - Confidence: {confidence[index]} - Lift: {lift[index]}
            </li>
          ))}
      </ul>
    </div>
  </div>
)}

</div>





    </div>
  )
}

export default Map
