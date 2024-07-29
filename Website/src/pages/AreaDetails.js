import { useEffect, useState, useCallback } from "react";
import { useParams } from "react-router-dom";
import "./AreaDetails.css";

const AreaDetails = () => {
  const { areaUID } = useParams();
  const [areaData, setAreaData] = useState(null);
  const [cameraUIDs, setCameraUIDs] = useState([]);
  const [showDropdown, setShowDropdown] = useState(false);
  const [selectedCameraUID, setSelectedCameraUID] = useState("");

  const fetchAreaData = async () => {
    try {
      const response = await fetch(`https://7l9qpd8im3.execute-api.ap-south-1.amazonaws.com/prod/get-specific-area-data?areaUID=${areaUID}`);
      const data = await response.json();
      setAreaData(data);
      const cams = Object.keys(data.cam_modules);
      setCameraUIDs(cams);
      if (cams.length === 1) {
        setSelectedCameraUID(cams[0]);
      }
    } catch (error) {
      console.error("Error fetching area details:", error);
    }
  };

  useEffect(() => {
    fetchAreaData();
    const interval = setInterval(() => {
      fetchAreaData();
    }, 5000);

    return () => clearInterval(interval);
  }, [areaUID]);

  const onSatelliteViewClick = useCallback(() => {
    const url = `https://7l9qpd8im3.execute-api.ap-south-1.amazonaws.com/prod/get-area-satellite-image?areaUID=${areaUID}`;
    window.open(url, '_blank');
  }, [areaUID]);

  const onLiveCameraViewClick = useCallback(() => {
    if (cameraUIDs.length === 1) {
      const url = `https://7l9qpd8im3.execute-api.ap-south-1.amazonaws.com/prod/get-street-cam-image?camUID=${cameraUIDs[0]}`;
      window.open(url, '_blank');
    } else if (cameraUIDs.length > 1) {
      setShowDropdown(true);
    }
  }, [cameraUIDs]);

  const handleCameraChange = (event) => {
    const camUID = event.target.value;
    setSelectedCameraUID(camUID);
    const url = `https://7l9qpd8im3.execute-api.ap-south-1.amazonaws.com/prod/get-street-cam-image?camUID=${camUID}`;
    window.open(url, '_blank');
    setShowDropdown(false);
  };

  if (!areaData) return <div>Loading...</div>;

  const significantPollutant = areaData.aqi_modules ? Object.entries(areaData.aqi_modules).reduce((prev, [key, value]) => {
    const highestPollutant = Object.keys(value).reduce((maxKey, key) => (value[key] > (value[maxKey] || 0) ? key : maxKey), 'AQI');
    return value[highestPollutant] > (prev.value || 0) ? { pollutant: highestPollutant, value: value[highestPollutant], address: value.address } : prev;
  }, { pollutant: 'AQI', value: 0, address: '' }) : null;

  return (
    <div className="surat1">
      <div className="header">
        <img className="logo" alt="Logo" src="/image-9@2x.png" />
        <div className="title">EarthAlly</div>
      </div>
      <div className="top-left-image">
        <img src="/4249429.png" alt="Top Left" />
      </div>
      <h1 className="area-name">{areaData.details.name}</h1>
    
      <div className="dashboard">
        <div className="card card1">
          <div className="card-content">
            <h2>Area Details</h2>
            <p>Name: {areaData.details.name}</p>
            <p>Address: {areaData.details.address}</p>
          </div>
        </div>

        <div className="card card6 pollutant">
          <div className="card-content">
            <h2>Weather details</h2>
            
              <div className="module">
                <p>Weather condition: {areaData.weather_condition}</p>
                <p>Wind Speed: {areaData.wind_speed} Km/hr</p>
              </div>
          </div>
        </div>

        
        <div className="card card3">
          <div className="card-content">
            <h2>Water Modules</h2>
            {Object.entries(areaData.water_modules).map(([key, value]) => (
              <div key={key} className="module">
                <p>Address: {value.address}</p>
                <p>pH: {value.pH}</p>
                <p>Turbidity: {value.turbidity}</p>
                <p>TDS: {value.TDS}</p>
              </div>
            ))}
          </div>
        </div>
        <div className="card card4">
          <div className="card-content">
            <h2>Air Quality Modules</h2>
            {Object.entries(areaData.aqi_modules).map(([key, value]) => (
              <div key={key} className="module">
                <p>Address: {value.address}</p>
                <p>Temperature: {value.temp}°C</p>
                <p>Humidity: {value.humd}%</p>
                <p>AQI: {value.AQI} </p>
                <p>PM2.5: {value["PM2.5"].toFixed(2)} µg/mg3</p>
                <p>PM10: {value.PM10.toFixed(2)} µg/mg3</p>
                <p>NO2: {value.NO2.toFixed(2)} µg/mg3</p>
                <p>SO2: {value.SO2.toFixed(2)} µg/mg3</p>
                <p>O3: {value.O3.toFixed(2)} µg/mg3</p>
                <p>CO: {value.CO.toFixed(2)} mg/m3</p>
                <p>NH3: {value.NH3.toFixed(2)} µg/mg3</p>
                <p>Significant Pollutant: {value.significant_pollutant}</p>
              </div>
            ))}
          </div>
        </div>
        <div className="card card5 forecast">
          <div className="card-content">
            <h2>Forecasted AQI</h2>
            {Object.entries(areaData.aqi_modules).map(([key, value]) => (
            <div className="module">
              <p>AQI: {value.aqi_forecast}</p>
            </div>
            ))}
          </div>
        </div>
        
        <div className="card card2">
          <div className="card-content">
            <h2>Soil Modules</h2>
            {Object.entries(areaData.soil_modules).map(([key, value]) => (
              <div key={key} className="module">
                <p>Address: {value.address}</p>
                <p>Moisture: {value.moisture}%</p>
              </div>
            ))}
          </div>
        </div>


      </div>
      <div className="satellite-view-container">
        <button className="satellite-view-btn" onClick={onSatelliteViewClick}>Satellite View</button>
        <button className="street-view-btn" onClick={onLiveCameraViewClick}>Street View</button>
        {showDropdown && (
          <div className="dropdown-container">
            <select value={selectedCameraUID} onChange={handleCameraChange}>
              <option value="">Select a camera</option>
              {cameraUIDs.map(camUID => (
                <option key={camUID} value={camUID}>{camUID}</option>
              ))}
            </select>
          </div>
        )}
      </div>
    </div>
  );
};

export default AreaDetails;
