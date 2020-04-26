import React, { useEffect, useRef, useState } from "react";
import styled from "styled-components";

const convertTonumber = (percentage, number) =>{
  return parseInt(parseInt(percentage)*number/100);
}
const DashboardTest = (props) => {
  const defaultState = {};
  const references = useRef(Array.from({length: props.objects.length}, () => React.createRef()));
  props.objects.forEach((item, i) => {
    defaultState[`item${i}`] = false;
  });
  const [show, doShow] = useState(defaultState);
  const [dimensions, setDimensions] = useState({
    height: window.innerHeight,
    width: window.innerWidth
  })

  useEffect(() => {
    const topPos = element => element.getBoundingClientRect().top;
    const divPos = {};
    references.current.forEach((item, i) => {
      divPos[`item${i}`] = topPos(item.current);
    });

    const onScroll = () => {
      const scrollPos = window.scrollY + window.innerHeight;
      for (const [key, value] of Object.entries(divPos)) {
        if(value < scrollPos){
          doShow(state => ({ ...state, [key]: true }));
          break;
        }
      }
    };
    const onResize = () => {
      setDimensions({
        height: window.innerHeight,
        width: window.innerWidth
      });
    };
    window.addEventListener("scroll", onScroll);
    window.addEventListener("resize",onResize);
    return () => {
      window.removeEventListener("scroll", onScroll);
      window.removeEventListener("resize", onResize);
    }
  }, []);
  return (
    <>
      <Wrapper>
        <Header
          width = {convertTonumber(props.width,dimensions.width) }
          height = {convertTonumber(props.height,dimensions.height) }
        />
        {
          props.objects.map((item,i) => {
            return (
              <Div
                animate = {show[`item${props.objects.length - (i + 1)}`]}
                ref = {references.current[`${props.objects.length - (i + 1)}`]}
                key = {i}
                width = {convertTonumber(props.width,dimensions.width) }
                height = {convertTonumber(props.height,dimensions.height) }
              >
                {item}
              </Div>
            )
          })
        }

      </Wrapper>
    </>
  );
};

const Header = styled.div`
  height: ${({ height }) => height}px;
  width: ${({ width }) => width}px;
  background-color: red;
  margin: 20px;
`;
const Div = styled.div`
  height: ${({ height }) => height}px;
  width: ${({ width }) => width}px;
  background-color: red;
  transform: translateX(${({ animate }) => (animate ? "0" : "-100vw")});
  transition: transform 2s;
  margin: 20px;
`;

const Wrapper = styled.div`
  margin: 10vh;
  display: flex;
  flex-flow: column;
  align-items: center;
`;

export default DashboardTest;
