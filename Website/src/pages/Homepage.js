import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Homepage.css";

const Homepage = () => {
  const navigate = useNavigate();
  const [areas, setAreas] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [alerts, setAlerts] = useState([]);
  const [showAlerts, setShowAlerts] = useState(false);

  useEffect(() => {
    const fetchAreas = async () => {
      try {
        const response = await fetch("https://7l9qpd8im3.execute-api.ap-south-1.amazonaws.com/prod/get-areas-basic-information");
        const data = await response.json();
        if (data.areasBasicInformation && Array.isArray(data.areasBasicInformation)) {
          setAreas(data.areasBasicInformation);
        } else {
          console.error("Expected an array but received:", data.areasBasicInformation);
        }
      } catch (error) {
        console.error("Error fetching areas:", error);
      }
    };

    const fetchAlerts = async () => {
      try {
        const response = await fetch("https://7l9qpd8im3.execute-api.ap-south-1.amazonaws.com/prod/get-alerts");
        const data = await response.json();

        const sortedAlerts = (data.alerts || []).sort((a, b) => {
          const dateA = new Date(a.DateTime.split(' ')[0].split('-').reverse().join('-') + 'T' + a.DateTime.split(' ')[1]);
          const dateB = new Date(b.DateTime.split(' ')[0].split('-').reverse().join('-') + 'T' + b.DateTime.split(' ')[1]);
          return dateB - dateA;
        });

        setAlerts(sortedAlerts);
      } catch (error) {
        console.error("Error fetching alerts:", error);
      }
    };

    fetchAreas();
    fetchAlerts();

    const areasInterval = setInterval(fetchAreas, 5000);
    const alertsInterval = setInterval(fetchAlerts, 5000);

    return () => {
      clearInterval(areasInterval);
      clearInterval(alertsInterval);
    };
  }, []);

  const onAreaClick = (areaUID) => {
    navigate(`/area/${areaUID}`);
  };

  const onSatelliteViewClick = (e, areaUID) => {
    e.stopPropagation();
    const url = `https://7l9qpd8im3.execute-api.ap-south-1.amazonaws.com/prod/get-area-satellite-image?areaUID=${areaUID}`;
    const link = document.createElement('a');
    link.href = url;
    link.target = '_blank';
    link.click();
  };

  const toggleAlerts = () => {
    setShowAlerts(!showAlerts);
  };

  const filteredAreas = areas.filter(area => 
    area.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="homepage">
      <div className="image-9-parent">
        <img className="image-9-icon" alt="" src="/image-9@2x.png" />
        <div className="earthally">EarthAlly</div>
      </div>
      <div className="top-left-imagee">
        <img src="/4249429.png" alt="Top Left" />
      </div>
      <div className="modules-data-areawise">Area</div>
      <div className="search-area">
        <input
          type="text"
          className="homepage-item"
          placeholder="Search area..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
        <div className="notification-container">
          <img className="notification-icon" src="/Untitled design.png" alt="Notifications" onClick={toggleAlerts} />
          {alerts.length > 0 && <span className="notification-count">{alerts.length}</span>}
          {showAlerts && (
            <div className="notification-dropdown">
              {alerts.length > 0 ? (
                alerts.map((alert) => (
                  <div key={alert.alertUID} className="notification-item">
                    <p>{alert.Message}</p>
                    <p className="date">{new Date(alert.DateTime.split(' ')[0].split('-').reverse().join('-') + 'T' + alert.DateTime.split(' ')[1]).toLocaleString()}</p>
                  </div>
                ))
              ) : (
                <div className="notification-item">No alerts available</div>
              )}
            </div>
          )}
        </div>
      </div>
      <img className="vector-icon" alt="" src="/vector.svg" />
      <div className="container">
        {filteredAreas.length > 0 ? (
          filteredAreas.map((area) => (
            <div key={area.areaUID} className="rectangle-div" onClick={() => onAreaClick(area.areaUID)}>
              <div>{area.name}</div>
              <button className="satellite-view-button" onClick={(e) => onSatelliteViewClick(e, area.areaUID)}> Satellite View</button>
            </div>
          ))
        ) : (
          <div>No areas found.</div>
        )}
      </div>
    </div>
  );
};

export default Homepage;
