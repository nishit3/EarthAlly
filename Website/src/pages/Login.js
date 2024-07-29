import { useCallback, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Login.css";

const Login = () => {
  const navigate = useNavigate();
  const [currentSlide, setCurrentSlide] = useState(0);
  const totalSlides = 4; 

  const onGroupContainerClick = useCallback(() => {
    navigate("/homepage");
  }, [navigate]);

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentSlide((prevSlide) => (prevSlide + 1) % totalSlides);
    }, 1000); 
    return () => clearInterval(interval);
  }, [totalSlides]);

  return (
    <div className="login">
      <div className="carousel">
        <div className="carousel-inner" style={{ transform: `translateX(-${currentSlide * 100}%)` }}>
          <img className="carousel-image" alt="" src="/image-5@2x.png" />
          <img className="carousel-image" alt="" src="/image-6@2x.png" />
          <img className="carousel-image" alt="" src="/image-7@2x.png" />
          <img className="carousel-image" alt="" src="/image-8@2x.png" />
         
          
         
        </div>
      </div>

      <img className="image-9-icon1" alt="" src="/image-91@2x.png" />
      <div className="earthally1">EarthAlly</div>
      <div className="protecting-our-planet">
        Protecting our planet, one step at a time.
      </div>
      <div className="login1">Login</div>
      <div className="group-parent">
        <div className="rectangle-parent1">
          <div className="password">
            <input
              type="password"
              className="rectangle-parent1"
              placeholder="Password"
            />
          </div>
          <img className="frame-icon" alt="" src="/frame.svg" />
        </div>
        <div className="username">
          <input
            type="text"
            className="rectangle-parent2"
            placeholder="Username"
          />
        </div>
        <img className="frame-icon1" alt="" src="/frame1.svg" />
        <div className="rectangle-parent3" onClick={onGroupContainerClick}>
          <div className="group-child4" />
          <b className="login2" onClick={onGroupContainerClick}>
            Login
          </b>
        </div>
      </div>
    </div>
  );
};

export default Login;









