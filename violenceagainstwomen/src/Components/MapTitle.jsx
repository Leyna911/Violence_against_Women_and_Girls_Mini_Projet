import React from 'react'
import Map from './map'


const MapTitle = () => {
  return (
    <div className='flex flex-col items-center justify-center ' >
        <div className='flex flex-col justify-center items-center text-center capitalize'>
            <h1 className='mb-4 text-3xl font-extrabold text-gray-900 dark:text-[#332929] md:text-5xl lg:text-6xl'>This <span className="text-transparent bg-clip-text bg-gradient-to-r to-[#E30000] from-[#332929]">Map </span>represents the world map</h1>
            <p className="mb-4 text-[24px] w-[1000px] font-normal text-[#312d2d]  dark:text-[#312d2d]">Choose a country and get the frequent Itemsets and metrics of the machine learning <span className="text-transparent bg-clip-text bg-gradient-to-r to-[#E30000] from-[#332929] font-bold">association algorithm. </span></p>
        </div>
        <Map/>
    </div>
  )
}

export default MapTitle
